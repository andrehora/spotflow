import inspect
from spotflow.utils import obj_value, obj_type, find_full_name, is_method_or_func, get_module_names
from spotflow.model import CallState, MonitoredMethod, MonitoredProgram
from spotflow.info import MethodInfo
from spotflow.tracer import PyTracer


def get_next_mro_class(current_class):
    mro_classes = current_class.__mro__
    current_class_index = mro_classes.index(current_class)
    return mro_classes[current_class_index+1]


def get_frame_id(frame):
    # If we are dealing with comprehensions and generator expressions
    # then we should get the enclosing frame id, not the current one.
    # This is done to avoid novel flows being created to listcomp and genexpr...
    if is_comprehension(frame):
        return id(frame.f_back)
    return id(frame)


def is_comprehension(frame):
    return frame.f_code.co_name in ['<listcomp>', '<setcomp>', '<dictcomp>', '<genexpr>']


def method_has_super_call(frame):
    return '__class__' in frame.f_locals and 'super' in frame.f_code.co_names


def line_has_return(frame):
    return line_has_keyword(frame, 'return')


def line_has_yield(frame):
    return line_has_keyword(frame, 'yield')


def line_has_control_flow(frame):
    return line_has_keywords(frame, ['if', 'elif', 'while', 'for'])


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


class Collector:

    def __init__(self):
        self.monitored_program = MonitoredProgram()
        self.method_names = None
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
        self.funcs_cache = {}

        self.py_tracer = PyTracer(self)

    def start(self):
        self.init_target()
        self.py_tracer.start_tracer()

    def stop(self):
        self.py_tracer.stop_tracer()
        self.monitored_program._update_flows_and_info()

    def init_target(self):
        if self.method_names:
            pass
            # self.module_names = get_module_names(self.method_names)

    def is_valid_frame(self, frame):

        current_filename = frame.f_code.co_filename

        if current_filename.startswith('<') or frame.f_code.co_name == '<module>':
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

        # if self.module_names:
        #     for module_name in self.module_names:
        #         if module_name in current_filename:
        #             return True
        #     return False

        return True

    def find_call_stack(self, frame):
        call_stack = []
        call_stack.append(frame.f_code.co_name)
        while 'test_' not in frame.f_code.co_name:
            if not frame.f_back:
                break
            frame = frame.f_back
            full_name = self.get_full_entity_name(frame)
            if full_name:
                call_stack.append(full_name)
            else:
                break
        call_stack.reverse()
        return tuple(call_stack)

    def get_full_entity_name(self, frame):

        func_or_method = self.ensure_func_or_method(frame)

        if func_or_method:
            return find_full_name(func_or_method)

        return None

    def ensure_target_method(self, frame, current_entity_name, method_name):

        # Handle special cases in which 'method' is already a method or function object
        if is_method_or_func(method_name):
            if current_entity_name in self.target_methods_cache:
                return self.target_methods_cache[current_entity_name]
            entity = MethodInfo.build(method_name)
            self.target_methods_cache[current_entity_name] = entity
            return entity

        if method_name and not current_entity_name.startswith(method_name) and \
                not current_entity_name.endswith(method_name):
            return None

        if current_entity_name in self.target_methods_cache:
            return self.target_methods_cache[current_entity_name]

        func_or_method = self.ensure_func_or_method(frame)
        if not func_or_method:
            return None
        entity = MethodInfo.build(func_or_method)
        if not entity:
            return None

        self.target_methods_cache[current_entity_name] = entity
        return entity

    def ensure_func_or_method(self, frame):

        filename = frame.f_code.co_filename
        lineno = frame.f_lineno
        entity_name = frame.f_code.co_name
        if is_comprehension(frame):
            entity_name = frame.f_back.f_code.co_name
        key = filename, lineno, entity_name

        if key in self.frame_cache:
            return self.frame_cache[key]

        func_or_method = self.get_func_or_method(frame)
        if not func_or_method or inspect.isbuiltin(func_or_method) or not is_method_or_func(func_or_method):
            return None

        self.frame_cache[key] = func_or_method
        return self.frame_cache[key]

    def get_func_or_method(self, frame):
        try:
            entity_name = frame.f_code.co_name

            # Method
            if 'self' in frame.f_locals:
                # In methods with super, use the free variable, __class__, not self
                if method_has_super_call(frame):
                    obj_class = frame.f_locals['__class__']
                # In methods without super but that was called by super (ie, the back frame has super),
                # get the next mro class to discover the actual class
                elif method_has_super_call(frame.f_back):
                    f_back = frame.f_back
                    obj_class = get_next_mro_class(f_back.f_locals['__class__'])
                # The most common case: simply get self class
                else:
                    obj_class = frame.f_locals['self'].__class__
                method = getattr(obj_class, entity_name, None)
                return method

            if 'cls' in frame.f_locals:
                obj_class = frame.f_locals['cls']
                method = getattr(obj_class, entity_name, None)
                return method

            # Function
            if entity_name in frame.f_globals:
                func = frame.f_globals[entity_name]
                return func

            # Local function
            local_func = self.find_local_func(entity_name, frame.f_back.f_locals)
            if local_func:
                return local_func

            local_func = self.find_local_func(entity_name, frame.f_locals)
            if local_func:
                return local_func

        except Exception as e:
            return None

    def find_local_func(self, entity_name, local_elements):
        # 1st: check the back locals
        if entity_name in local_elements:
            func = local_elements[entity_name]
            if inspect.isfunction(func) and entity_name == func.__name__:
                if '<locals>' in func.__qualname__:
                    return func

        # 2nd: check the back local values
        for func in local_elements.values():
            if inspect.isfunction(func) and entity_name == func.__name__:
                if '<locals>' in func.__qualname__:
                    return func

        # 3rd: check the back self, if any
        if 'self' in local_elements:
            obj = local_elements['self']
            obj_funcs = dict(inspect.getmembers(obj, predicate=inspect.isfunction))
            if entity_name in obj_funcs:
                func = obj_funcs[entity_name]
                if '<locals>' in func.__qualname__:
                    return func

        return None

    def update_method_info(self, method_info, frame, event):
        lineno = frame.f_lineno

        if event == 'line' and line_has_control_flow(frame):
            method_info.control_flow_lines.add(lineno)

        if event == 'return':
            if line_has_return(frame):
                method_info.return_lines.add(lineno)
            elif line_has_yield(frame):
                method_info.yield_lines.add(lineno)

        if event == 'exception':
            method_info.exception_lines.add(lineno)

    def monitor_event(self, frame, event, arg):

        if not self.is_valid_frame(frame):
            return

        current_method_name = self.get_full_entity_name(frame)

        if current_method_name:
            if self.method_names:
                for method_name in self.method_names:
                    self.monitor_method(frame, event, arg, current_method_name, method_name)
            elif self.method_names is None:
                self.monitor_method(frame, event, arg, current_method_name)

    def monitor_method(self, frame, event, arg, current_method_name, method_name=None):

        method_info = self.ensure_target_method(frame, current_method_name, method_name)

        if method_info and current_method_name == method_info.full_name:
            self.update_method_info(method_info, frame, event)

            if current_method_name not in self.last_frame_lineno:
                self.last_frame_lineno[current_method_name] = -1

            # Tip from Coverage.py
            # The call event is really a "start frame" event, and happens for
            # function calls and re-entering generators.  The f_lasti field is
            # -1 for calls, and a real offset for generators.  Use < 0 as the
            # line number for calls, and the real line number for generators.
            if event == 'call' and getattr(frame, 'f_lasti', -1) < 0 and not is_comprehension(frame):
                if current_method_name not in self.monitored_program:
                    self.monitored_program[current_method_name] = MonitoredMethod(method_info)

                call_state = CallState()
                callers = self.find_call_stack(frame)

                if self.collect_arg_states:
                    call_state._save_arg_states(inspect.getargvalues(frame), frame.f_lineno)

                frame_id = get_frame_id(frame)
                monitored_method = self.monitored_program[current_method_name]
                monitored_method._add_call(call_state, callers, frame_id)

            # Event is line, return, exception or call for re-entering generators
            else:
                lineno = frame.f_lineno
                if current_method_name in self.monitored_program:
                    monitored_method = self.monitored_program[current_method_name]
                    if monitored_method.calls:
                        frame_id = get_frame_id(frame)
                        method_call = monitored_method._get_call_from_id(frame_id)
                        if method_call:

                            current_call_state = method_call.call_state
                            if event == 'line':
                                method_call._add_run_line(lineno)
                                monitored_method._add_run_line(lineno)

                            elif event == 'return':
                                if self.collect_return_states and line_has_return(frame):
                                    current_call_state._save_return_state(obj_value(arg), obj_type(arg), lineno)
                                elif self.collect_yield_states and line_has_yield(frame):
                                    current_call_state._save_yield_state(obj_value(arg), obj_type(arg), lineno)

                            elif event == 'exception':
                                if self.collect_exception_states:
                                    exception_name = arg[0].__name__
                                    exception_type = obj_type(arg[0])
                                    current_call_state._save_exception_state(exception_name, exception_type, lineno)

                            if self.collect_var_states and current_call_state:
                                argvalues = inspect.getargvalues(frame)
                                inline = self.last_frame_lineno[current_method_name]
                                current_call_state._save_var_states(argvalues, lineno, inline)

                self.last_frame_lineno[current_method_name] = lineno
