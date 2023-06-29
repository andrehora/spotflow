import inspect
from spotflow.utils import obj_value, obj_type, get_full_name, is_method_or_func, get_module_names
from spotflow.model import CallState, MonitoredMethod, MonitoredProgram
from spotflow.info import MethodInfo
from spotflow.tracer import PyTracer


def get_line_key(frame):

    filename = frame.f_code.co_filename
    lineno = frame.f_lineno
    entity_name = frame.f_code.co_name
    if is_compr_or_genexpr(frame):
        entity_name = frame.f_back.f_code.co_name
    key = filename, lineno, entity_name
    return key


def get_next_mro_class(current_class):

    mro_classes = current_class.__mro__
    current_class_index = mro_classes.index(current_class)
    return mro_classes[current_class_index + 1]


def get_frame_id(frame):

    # If we are dealing with comprehensions and generator expressions
    # then we should get the enclosing frame id, not the current one.
    # This is done to avoid novel flows being created to listcomp and genexpr...
    if is_compr_or_genexpr(frame):
        return id(frame.f_back)
    return id(frame)


def is_compr_or_genexpr(frame):
    return frame.f_code.co_name in ["<listcomp>", "<setcomp>", "<dictcomp>", "<genexpr>"]


def method_has_super_call(frame):
    return "__class__" in frame.f_locals and "super" in frame.f_code.co_names


def line_has_return(frame):
    return line_has_keyword(frame, "return")


def line_has_yield(frame):
    return line_has_keyword(frame, "yield")


def line_has_control_flow(frame):
    return line_has_keywords(frame, ["if", "elif", "while", "for"])


def line_has_keyword(frame, keyword):

    traceback = inspect.getframeinfo(frame)
    if traceback.code_context and len(traceback.code_context) >= 1:
        code_line = traceback.code_context[0].strip()
        return code_line.startswith(keyword)
    return False


def line_has_keywords(frame, keywords):

    traceback = inspect.getframeinfo(frame)
    if traceback.code_context and len(traceback.code_context) >= 1:
        code_line = traceback.code_context[0].strip()
        for keyword in keywords:
            if code_line.startswith(keyword):
                return True
    return False


def update_method_info(method_info, frame, event):

    lineno = frame.f_lineno
    if lineno in method_info.other_lines or lineno in method_info.control_flow_lines:
        return

    if lineno in method_info.return_lines or lineno in method_info.yield_lines:
        return

    if lineno in method_info.exception_lines:
        return

    if event == "call":
        return

    if event == "line":
        if line_has_control_flow(frame):
            method_info.control_flow_lines.add(lineno)
        else:
            method_info.other_lines.add(lineno)

    elif event == "return":
        if line_has_return(frame):
            method_info.return_lines.add(lineno)
        elif line_has_yield(frame):
            method_info.yield_lines.add(lineno)

    elif event == "exception":
        method_info.exception_lines.add(lineno)


def find_local_func(entity_name, local_elements):

    # 1st: check the locals
    if entity_name in local_elements:
        func = local_elements[entity_name]
        if inspect.isfunction(func) and entity_name == func.__name__:
            if "<locals>" in func.__qualname__:
                return func

    # 2nd: check the local values
    for func in local_elements.values():
        if inspect.isfunction(func) and entity_name == func.__name__:
            if "<locals>" in func.__qualname__:
                return func

    # 3rd: check the self, if any
    if "self" in local_elements:
        obj = local_elements["self"]
        obj_funcs = dict(inspect.getmembers(obj, predicate=inspect.isfunction))
        if entity_name in obj_funcs:
            func = obj_funcs[entity_name]
            if "<locals>" in func.__qualname__:
                return func
    return None


def get_method_object(frame):

    try:
        method_name = frame.f_code.co_name

        # Method
        if "self" in frame.f_locals:

            # The most common case: simply get self class
            obj_class = frame.f_locals["self"].__class__

            # In methods without that was called by super (ie, the back frame has super),
            # get the next mro class to discover the actual class. Make sure it is part of the hierarchy
            if method_has_super_call(frame.f_back):
                f_back = frame.f_back
                back_class = f_back.f_locals["__class__"]
                if back_class in obj_class.__mro__:
                    obj_class = get_next_mro_class(back_class)
            
            method = inspect.getattr_static(obj_class, method_name, None)

            return method

        if "cls" in frame.f_locals:
            obj_class = frame.f_locals["cls"]
            method = inspect.getattr_static(obj_class, method_name, None)
            return method

        # Function
        if method_name in frame.f_globals:
            func = frame.f_globals[method_name]
            return func

        # Local function
        local_func = find_local_func(method_name, frame.f_back.f_locals)
        if local_func:
            return local_func

        local_func = find_local_func(method_name, frame.f_locals)
        if local_func:
            return local_func

    except Exception as e:
        return None


def is_valid_method_name(frame, current_method_name):
        
    if is_compr_or_genexpr(frame):
        return True

    method_name_from_frame = frame.f_code.co_name
    method_name_from_current = current_method_name.split('.')[-1]
    return method_name_from_frame == method_name_from_current


class Collector:

    def __init__(self):

        self.monitored_program = MonitoredProgram()
        self.target_method_full_names = None
        self.target_method_short_names = None
        self.file_names = None
        self.ignore_files = None
        self.module_names = None

        self.collect_arg_states = True
        self.collect_return_states = True
        self.collect_yield_states = True
        self.collect_exception_states = True
        self.collect_var_states = True

        self.last_frame_lineno = {}
        self.target_methods_cache = {}
        self.frame_cache = {}

        self.py_tracer = PyTracer(self)

    def start(self):
        self.init_target()
        self.py_tracer.start_tracer()

    def stop(self):
        self.py_tracer.stop_tracer()
        self.monitored_program._update_info()

    def init_target(self):
        if self.target_method_full_names and not self.target_method_short_names:
            self.module_names = get_module_names(self.target_method_full_names)

    def monitor_event(self, frame, event, arg):

        if not self.is_valid_frame(frame):
            return

        current_method_name = self.get_method_full_name(frame)
        if not current_method_name:
            return

        if not is_valid_method_name(frame, current_method_name):
            return

        if self.target_method_short_names:
            self.monitor_method(frame, event, arg, current_method_name)
            return

        if self.target_method_full_names:
            for target_method_full_name in self.target_method_full_names:
                self.monitor_method(frame, event, arg, current_method_name, target_method_full_name)
            return
        
        if self.target_method_full_names is None and self.target_method_short_names is None:
            self.monitor_method(frame, event, arg, current_method_name)

    def monitor_method(self, frame, event, arg, current_method_name, target_method=None):

        method_info = self.ensure_target_method_info(frame, current_method_name, target_method)

        if not method_info:
            return

        if current_method_name != method_info.full_name:
            return

        update_method_info(method_info, frame, event)

        if current_method_name not in self.last_frame_lineno:
            self.last_frame_lineno[current_method_name] = -1

        # Tip from Coverage.py
        # The call event is really a "start frame" event, and happens for
        # function calls and re-entering generators.  The f_lasti field is
        # -1 for calls, and a real offset for generators.  Use < 0 as the
        # line number for calls, and the real line number for generators.
        if (event == "call" and getattr(frame, "f_lasti", -1) < 0 and not is_compr_or_genexpr(frame)):
            if current_method_name not in self.monitored_program:
                self.monitored_program[current_method_name] = MonitoredMethod(method_info)

            call_state = CallState()
            callers = self.find_call_stack(frame)

            if self.collect_arg_states:
                call_state._save_arg_states(inspect.getargvalues(frame), frame.f_lineno)

            frame_id = get_frame_id(frame)
            monitored_method = self.monitored_program[current_method_name]
            monitored_method.add_call(call_state, callers, frame_id)

        # Event is line, return, exception or call for re-entering generators
        else:
            lineno = frame.f_lineno
            if current_method_name in self.monitored_program:

                monitored_method = self.monitored_program[current_method_name]
                if not monitored_method.calls:
                    return

                frame_id = get_frame_id(frame)
                method_call = monitored_method._get_call_from_id(frame_id)
                if not method_call:
                    return

                current_call_state = method_call.call_state
                if event == "line":
                    method_call._add_run_line(lineno)
                    monitored_method._add_run_line(lineno)

                elif event == "return":
                    if self.collect_return_states and line_has_return(frame):
                        current_call_state._save_return_state(obj_value(arg), obj_type(arg), lineno)
                    elif self.collect_yield_states and line_has_yield(frame):
                        current_call_state._save_yield_state(obj_value(arg), obj_type(arg), lineno)

                elif event == "exception":
                    if self.collect_exception_states:
                        exception_name = arg[0].__name__
                        exception_type = obj_type(arg[0])
                        current_call_state._save_exception_state(exception_name, exception_type, lineno)

                if self.collect_var_states and current_call_state:
                    argvalues = inspect.getargvalues(frame)
                    inline = self.last_frame_lineno[current_method_name]
                    current_call_state._save_var_states(argvalues, lineno, inline)

            self.last_frame_lineno[current_method_name] = lineno

    def is_valid_frame(self, frame):

        current_filename = frame.f_code.co_filename

        if current_filename.startswith("<") or frame.f_code.co_name == "<module>":
            return False

        if self.target_method_short_names:
            for method_name in self.target_method_short_names:
                if method_name == frame.f_code.co_name:
                    return True
            return False

        if self.ignore_files:
            for ignore in self.ignore_files:
                if ignore in current_filename:
                    return False

        if self.file_names:
            for filename in self.file_names:
                if filename in current_filename:
                    return True
                if frame.f_back:
                    back_filename = frame.f_back.f_code.co_filename
                    if filename in back_filename:
                        return True
            return False

        if self.module_names:
            for module_name in self.module_names:
                if module_name in current_filename:
                    return True
            return False

        return True

    def get_method_full_name(self, frame):

        method_obj = self.ensure_method_obj(frame)
        if method_obj:
            return get_full_name(method_obj)

        return None

    def ensure_method_obj(self, frame):

        key = get_line_key(frame)

        if key in self.frame_cache:
            return self.frame_cache[key]

        method_obj = get_method_object(frame)
        if (not method_obj or inspect.isbuiltin(method_obj) or not is_method_or_func(method_obj)):
            return None

        self.frame_cache[key] = method_obj
        return self.frame_cache[key]

    def ensure_target_method_info(self, frame, current_entity_name, target_method):

        # Handle the special case in which 'target_method' is already method/function object
        if is_method_or_func(target_method):
            if current_entity_name in self.target_methods_cache:
                return self.target_methods_cache[current_entity_name]
            method_info = MethodInfo.build(target_method)
            self.target_methods_cache[current_entity_name] = method_info
            return method_info

        # Handle the other cases...
        if target_method and not current_entity_name.startswith(target_method):
            return None

        if current_entity_name in self.target_methods_cache:
            return self.target_methods_cache[current_entity_name]

        method_obj = self.ensure_method_obj(frame)
        if not method_obj:
            return None
        method_info = MethodInfo.build(method_obj)
        if not method_info:
            return None

        self.target_methods_cache[current_entity_name] = method_info
        return method_info

    def find_call_stack(self, frame):

        call_stack = [frame.f_code.co_name]
        while frame.f_back:
            frame = frame.f_back
            full_name = self.get_method_full_name(frame)
            if full_name:
                call_stack.append(full_name)
            else:
                break
        call_stack.reverse()
        return tuple(call_stack)
