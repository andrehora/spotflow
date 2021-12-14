import inspect
import types
from happyflow.utils import obj_value, find_full_name
from happyflow.flow import CallState, TracedMethod, TracedSystem
from happyflow.info import MethodInfo
from happyflow.tracer import PyTracer


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


def line_has_keyword(frame, keyword):
    traceback = inspect.getframeinfo(frame)
    if traceback.code_context and len(traceback.code_context) >= 1:
        code_line = traceback.code_context[0].strip()
        return code_line.startswith(keyword)
    return False


def update_method_info(method_info, frame, event):
    if event == 'return':
        if line_has_return(frame):
            method_info.has_return = True
        elif line_has_yield(frame):
            method_info.has_yield = True
    elif event == 'exception':
        method_info.has_exception = True
    if method_has_super_call(frame):
        method_info.has_super = True


class Collector:

    IGNORE_FILES = ['site-packages', 'unittest', 'pytest']

    def __init__(self):
        self.traced_system = TracedSystem()
        self.method_names = None
        self.ignore_files = None

        self.last_frame_lineno = {}
        self.target_methods_cache = {}
        self.frame_cache = {}
        self.funcs_cache = {}

        self.py_tracer = PyTracer(self)

        # Flags used when target is not set
        self.try_all_possible_targets = False
        self.tests_started = False

    def start(self):
        self.init_target()
        self.init_ignore()
        self.py_tracer.start_tracer()

    def stop(self):
        self.py_tracer.stop_tracer()

    def init_target(self):
        if not self.method_names:
            self.try_all_possible_targets = True
            self.method_names = ['__ALL__']

    def init_ignore(self):
        if not self.ignore_files:
            self.ignore_files = self.IGNORE_FILES

    def collect_flow(self, frame, event, arg):

        if not self.is_valid_frame(frame):
            return

        current_method_name = self.get_full_entity_name(frame)

        # if not current_method_name and frame.f_code.co_name == '_iterencode':
        #     print(frame.f_code.co_name)

        # if frame.f_code.co_name == '_iterencode':
        #     print(event, id(frame), frame.f_lineno,  getattr(frame, 'f_lasti', -1), inspect.getframeinfo(frame).code_context)
            # print('==>Back', self.get_full_entity_name(frame.f_back), event, id(frame.f_back), frame.f_back.f_lineno, getattr(frame, 'f_lasti', -1), inspect.getframeinfo(frame.f_back).code_context)

        if current_method_name:
            for method_name in self.method_names:

                method_info = self.ensure_target_method(current_method_name, method_name, frame)

                if method_info and current_method_name == method_info.full_name:
                    update_method_info(method_info, frame, event)

                    if current_method_name not in self.last_frame_lineno:
                        self.last_frame_lineno[current_method_name] = -1

                    # Tip from Coverage.py
                    # The call event is really a "start frame" event, and happens for
                    # function calls and re-entering generators.  The f_lasti field is
                    # -1 for calls, and a real offset for generators.  Use < 0 as the
                    # line number for calls, and the real line number for generators.
                    if event == 'call' and getattr(frame, 'f_lasti', -1) < 0 and not is_comprehension(frame):
                        if current_method_name not in self.traced_system:
                            self.traced_system[current_method_name] = TracedMethod(method_info)

                        run_lines = []
                        call_state = CallState()
                        call_state.save_arg_states(inspect.getargvalues(frame), frame.f_lineno)
                        callers = self.find_call_stack(frame)
                        frame_id = get_frame_id(frame)

                        traced_method = self.traced_system[current_method_name]
                        traced_method.add_call(run_lines, call_state, callers, frame_id)

                    # Event is line, return, exception or call for re-entering generators
                    else:

                        lineno = frame.f_lineno
                        if current_method_name in self.traced_system:
                            traced_method = self.traced_system[current_method_name]
                            if traced_method.calls:
                                frame_id = get_frame_id(frame)
                                method_call = traced_method._get_call_from_id(frame_id)
                                if method_call:
                                    current_run_lines = method_call.run_lines
                                    current_call_state = method_call.call_state

                                    if event == 'line':
                                        current_run_lines.append(lineno)

                                    elif event == 'return':
                                        if line_has_return(frame):
                                            current_call_state.save_return_state(obj_value(arg), lineno)
                                        elif line_has_yield(frame):
                                            current_call_state.save_yield_state(obj_value(arg), lineno)

                                    elif event == 'exception':
                                        exception_name = arg[0].__name__
                                        current_call_state.save_exception_state(exception_name, lineno)

                                    if current_call_state:
                                        argvalues = inspect.getargvalues(frame)
                                        inline = self.last_frame_lineno[current_method_name]
                                        current_call_state.save_var_states(argvalues, lineno, inline)

                        self.last_frame_lineno[current_method_name] = lineno

    def is_valid_frame(self, frame):

        if frame.f_code.co_filename.startswith('<') or frame.f_code.co_name == '<module>':
            return False

        for ignore in self.ignore_files:
            if ignore in frame.f_code.co_filename:
                return False

        if self.try_all_possible_targets:
            return self.check_tests_started(frame)

        for method_name in self.method_names:
            if isinstance(method_name, str):
                module_name = method_name.split('.')[0]
                if module_name not in frame.f_code.co_filename:
                    return False
        return True

    def find_call_stack(self, frame):
        call_stack = []
        call_stack.append(frame.f_code.co_name)
        while 'test' not in frame.f_code.co_name:
            if not frame.f_back:
                break
            frame = frame.f_back
            full_name = self.get_full_entity_name(frame)
            call_stack.append(full_name)
        call_stack.reverse()
        return tuple(call_stack)

    def check_tests_started(self, frame):

        if self.tests_started:
            return True

        filename = frame.f_code.co_filename

        if 'test_' in filename:
            self.tests_started = True
            return True
        return False

    def get_full_entity_name(self, frame):

        func_or_method = self.ensure_func_or_method(frame)

        if func_or_method:
            return find_full_name(func_or_method)

        return None

    def ensure_target_method(self, current_entity_name, method_name, frame):

        if isinstance(method_name, types.FunctionType) or isinstance(method_name, types.MethodType):
            return MethodInfo.build(method_name)

        if not self.try_all_possible_targets:
            if not current_entity_name.startswith(method_name):
                return None

        if self.try_all_possible_targets:
            if 'test_' in current_entity_name:
                return None

        if current_entity_name in self.target_methods_cache:
            return self.target_methods_cache[current_entity_name]

        func_or_method = self.ensure_func_or_method(frame)
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

        entity = self.get_func_or_method(frame)
        if not entity:
            return None

        self.frame_cache[key] = entity
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

            # if entity_name == 'scan_once':
            # print(frame.f_code.co_name, frame.f_code.co_filename, inspect.getframeinfo(frame).code_context)
            # print(frame.f_locals)

        except Exception as e:
            print(e)
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

        # # 4th: check the generators
        # for gen in frame.f_back.f_locals.values():
        #     if inspect.isgenerator(gen):
        #         if entity_name == gen.__name__:
        #             gen_locals = inspect.getgeneratorlocals(gen)
        #             if entity_name in gen_locals:
        #                 func = gen_locals[entity_name]
        #                 if '<locals>' in func.__qualname__:
        #                     return func
