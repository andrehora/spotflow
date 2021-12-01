import inspect
from happyflow.utils import obj_value, find_full_name
from happyflow.flow import StateHistory, EntityFlowContainer, ArgState, ExceptionState, FlowResult
from happyflow.target import TargetEntity
from happyflow.tracer import PyTracer


def get_arg_states(frame):
    try:
        states = []
        argvalues = inspect.getargvalues(frame)

        for arg in argvalues.args:
            value = obj_value(argvalues.locals[arg])
            arg_state = ArgState(arg, value, frame.f_lineno)
            states.append(arg_state)

        if argvalues.varargs:
            value = obj_value(argvalues.locals[argvalues.varargs])
            arg_state = ArgState(argvalues.varargs, value, frame.f_lineno)
            states.append(arg_state)

        if argvalues.keywords:
            value = obj_value(argvalues.locals[argvalues.keywords])
            arg_state = ArgState(argvalues.keywords, value, frame.f_lineno)
            states.append(arg_state)

        return states

    except Exception as e:
        raise


def get_next_mro_class(current_class):
    mro_classes = current_class.__mro__
    current_class_index = mro_classes.index(current_class)
    return mro_classes[current_class_index+1]


def find_callers(frame):
    callers = []
    callers.append(frame.f_code.co_name)
    while 'test' not in frame.f_code.co_name:
        if not frame.f_back:
            break
        frame = frame.f_back
        callers.append(frame.f_code.co_name)
    callers.reverse()
    return tuple(callers)


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


def line_has_keyword(frame, keyword):
    traceback = inspect.getframeinfo(frame)
    if traceback.code_context and len(traceback.code_context) >= 1:
        code_line = traceback.code_context[0].strip()
        return code_line.startswith(keyword)
    return False


def line_has_return(frame):
    return line_has_keyword(frame, 'return')


def line_has_yield(frame):
    return line_has_keyword(frame, 'yield')


class Collector:

    IGNORE_FILES = ['site-packages', 'unittest', 'pytest']

    def __init__(self):
        self.trace_result = FlowResult()
        self.target_entity_names = None
        self.ignore_files = None

        self.last_frame_line = {}
        self.target_entities_cache = {}
        self.frame_cache = {}

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
        if not self.target_entity_names:
            self.try_all_possible_targets = True
            self.target_entity_names = ['__ALL__']

    def init_ignore(self):
        if not self.ignore_files:
            self.ignore_files = self.IGNORE_FILES

    def collect_flow(self, frame, event, arg):

        if not self.is_valid_frame(frame):
            return

        current_entity_name = self.get_full_entity_name(frame)

        if current_entity_name:
            for target_entity_name in self.target_entity_names:

                target_entity = self.ensure_target_entity(current_entity_name, target_entity_name, frame)

                if target_entity and current_entity_name == target_entity.full_name:
                    if current_entity_name not in self.last_frame_line:
                        self.last_frame_line[current_entity_name] = -1

                    # Tip from Coverage.py
                    # The call event is really a "start frame" event, and happens for
                    # function calls and re-entering generators.  The f_lasti field is
                    # -1 for calls, and a real offset for generators.  Use < 0 as the
                    # line number for calls, and the real line number for generators.
                    if event == 'call' and getattr(frame, 'f_lasti', -1) < 0 and not is_comprehension(frame):
                        if current_entity_name not in self.trace_result:
                            self.trace_result[current_entity_name] = EntityFlowContainer(target_entity)

                        run_lines = []
                        state_history = StateHistory()
                        state_history.arg_states = get_arg_states(frame)
                        callers = find_callers(frame)
                        # callers = []

                        entity_result = self.trace_result[current_entity_name]

                        frame_id = get_frame_id(frame)
                        entity_result.add_flow(run_lines, state_history, callers, frame_id)

                    # Event is line, return, exception or call for re-entering generators
                    else:

                        lineno = frame.f_lineno
                        if current_entity_name in self.trace_result:
                            entity_result = self.trace_result[current_entity_name]
                            if entity_result.flows:

                                frame_id = get_frame_id(frame)
                                flow = entity_result.get_flow_from_id(frame_id)
                                if flow:
                                    current_run_lines = flow.run_lines
                                    current_state_history = flow.state_history

                                    if event == 'line':
                                        current_run_lines.append(lineno)

                                    elif event == 'return':

                                        if line_has_return(frame):
                                            current_state_history.add_return_state(obj_value(arg), lineno)

                                        elif line_has_yield(frame):
                                            current_state_history.add_yield_state(obj_value(arg), lineno)

                                    elif event == 'exception':
                                        current_state_history.exception_state = ExceptionState(obj_value(arg), lineno)

                                    # if current_state_history:
                                    #     argvalues = inspect.getargvalues(frame)
                                    #     for arg in argvalues.locals:
                                    #         value = obj_value(argvalues.locals[arg])
                                    #         current_state_history.add_var_state(name=arg, value=value, lineno=lineno,
                                    #                                  inline=self.last_frame_line[current_entity_name])

                        self.last_frame_line[current_entity_name] = lineno

    def is_valid_frame(self, frame):

        if frame.f_code.co_filename.startswith('<'):
            return False

        for ignore in self.ignore_files:
            if ignore in frame.f_code.co_filename:
                return False

        if self.try_all_possible_targets:
            return self.check_tests_started(frame)

        for target_entity_name in self.target_entity_names:
            if isinstance(target_entity_name, str):
                module_name = target_entity_name.split('.')[0]
                if module_name not in frame.f_code.co_filename:
                    return False
        return True

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

    def ensure_target_entity(self, current_entity_name, target_entity_name, frame):

        if not isinstance(target_entity_name, str):
            return target_entity_name

        if not self.try_all_possible_targets:
            if not current_entity_name.startswith(target_entity_name):
                return None

        if self.try_all_possible_targets:
            if 'test_' in current_entity_name:
                return None

        if current_entity_name in self.target_entities_cache:
            return self.target_entities_cache[current_entity_name]

        func_or_method = self.ensure_func_or_method(frame)
        entity = TargetEntity.build(func_or_method)
        if not entity:
            return None

        self.target_entities_cache[current_entity_name] = entity
        return entity

    def ensure_func_or_method(self, frame):

        filename = frame.f_code.co_filename
        lineno = frame.f_lineno
        name = frame.f_code.co_name
        if is_comprehension(frame):
            name = frame.f_back.f_code.co_name
        key = filename, lineno, name

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
                # print(frame.f_lineno, obj_class)
                method = getattr(obj_class, entity_name, None)
                # print('==> class', obj_class, method)
                return method

            # Function
            if entity_name in frame.f_globals:
                func = frame.f_globals[entity_name]
                return func

            # Local function or method
            if entity_name in frame.f_back.f_locals:
                func_or_method = frame.f_back.f_locals[entity_name]
                # Check if 'entity_name' is local in frame.f_back
                if '<locals>' in func_or_method.__qualname__ and \
                        frame.f_back.f_code.co_name in func_or_method.__qualname__:
                    return func_or_method

        except Exception as e:
            # print(e)
            return None
