import inspect
from happyflow.utils import obj_value, line_has_explicit_return, find_full_name, line_has_yield
from happyflow.flow import StateHistory, EntityFlowContainer, ArgState, ExceptionState, FlowResult
from happyflow.target import TargetEntity
from happyflow.tracer import PyTracer


class Collector:

    IGNORE_FILES = ['site-packages', 'unittest', 'pytest']
    # IGNORE_FILES = []

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

    def check_tests_started(self, filename):

        if self.tests_started:
            return True

        if 'test_' in filename:
            self.tests_started = True
            return True
        return False

    def init_ignore(self):
        if not self.ignore_files:
            self.ignore_files = self.IGNORE_FILES

    def get_arg_states(self, frame):
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
        if self.is_comprehension(frame):
            name = frame.f_back.f_code.co_name

        key = filename, lineno, name

        if key in self.frame_cache:
            return self.frame_cache[key]

        entity = self._get_func_or_method(frame)
        if not entity:
            return None

        self.frame_cache[key] = self._get_func_or_method(frame)
        return self.frame_cache[key]

    def _get_func_or_method(self, frame):
        try:
            entity_name = frame.f_code.co_name

            # Function
            if entity_name in frame.f_globals:
                func_or_method = frame.f_globals[entity_name]
                return func_or_method

            # Local function or method
            if entity_name in frame.f_back.f_locals:
                func_or_method = frame.f_back.f_locals[entity_name]
                return func_or_method

            # Method
            if 'self' in frame.f_locals:
                obj = frame.f_locals['self']
                members = dict(inspect.getmembers(obj, inspect.ismethod))
                if entity_name in members:
                    func_or_method = members[entity_name]
                    return func_or_method

        except Exception as e:
            return None

    def get_full_entity_name(self, frame):

        func_or_method = self.ensure_func_or_method(frame)

        if func_or_method:
            return find_full_name(func_or_method)

        return None

    def find_callers(self, frame):
        callers = []
        callers.append(frame.f_code.co_name)
        while 'test' not in frame.f_code.co_name:
            if not frame.f_back:
                break
            frame = frame.f_back
            callers.append(frame.f_code.co_name)
        callers.reverse()
        return tuple(callers)

    def get_frame_id(self, frame):
        # If we are dealing with comprehensions and generator expressions
        # then we should get the enclosing frame id, not the current one.
        # This is done to avoid novel flows being created to listcomp and genexpr...
        if self.is_comprehension(frame):
            return id(frame.f_back)
        return id(frame)

    def is_comprehension(self, frame):
        return frame.f_code.co_name in ['<listcomp>', '<setcomp>', '<dictcomp>', '<genexpr>']

    def is_valid_frame(self, frame):

        if frame.f_code.co_filename.startswith('<'):
            return False

        for ignore in self.ignore_files:
            if ignore in frame.f_code.co_filename:
                return False

        if self.try_all_possible_targets:
            return self.check_tests_started(frame.f_code.co_filename)

        for target_entity_name in self.target_entity_names:
            if isinstance(target_entity_name, str):
                module_name = target_entity_name.split('.')[0]
                if module_name not in frame.f_code.co_filename:
                    return False
        return True

    def collect_flow(self, frame, event, arg):

        if not self.is_valid_frame(frame):
            return

        current_entity_name = self.get_full_entity_name(frame)

        if current_entity_name:
            for target_entity_name in self.target_entity_names:

                # print(current_entity_name, event, frame.f_lineno, frame.f_code.co_name, id(frame))
                # print(event == 'call' and getattr(frame, 'f_lasti', -1) < 0)

                target_entity = self.ensure_target_entity(current_entity_name, target_entity_name, frame)

                if target_entity and current_entity_name == target_entity.full_name:
                    if current_entity_name not in self.last_frame_line:
                        self.last_frame_line[current_entity_name] = -1

                    # Tip from Coverage.py :)
                    # The call event is really a "start frame" event, and happens for
                    # function calls and re-entering generators.  The f_lasti field is
                    # -1 for calls, and a real offset for generators.  Use < 0 as the
                    # line number for calls, and the real line number for generators.
                    if event == 'call' and getattr(frame, 'f_lasti', -1) < 0 and not self.is_comprehension(frame):

                        if current_entity_name not in self.trace_result:
                            self.trace_result[current_entity_name] = EntityFlowContainer(target_entity)

                        run_lines = []
                        state_history = StateHistory()
                        state_history.arg_states = self.get_arg_states(frame)
                        callers = self.find_callers(frame)

                        entity_result = self.trace_result[current_entity_name]

                        frame_id = self.get_frame_id(frame)
                        entity_result.add_flow(run_lines, state_history, callers, frame_id)

                    # Event is line, return, exception or call for re-entering generators
                    else:
                        lineno = frame.f_lineno
                        if current_entity_name in self.trace_result:
                            entity_result = self.trace_result[current_entity_name]
                            if entity_result.flows:

                                frame_id = self.get_frame_id(frame,)
                                flow = entity_result.get_flow_from_id(frame_id)
                                if flow:
                                    current_run_lines = flow.run_lines
                                    current_state_history = flow.state_history

                                    if event == 'line':
                                        current_run_lines.append(lineno)

                                    elif event == 'return':

                                        if line_has_explicit_return(frame):
                                            current_state_history.add_return_state(obj_value(arg), lineno)

                                        elif line_has_yield(frame):
                                            current_state_history.add_yield_state(obj_value(arg), lineno)

                                    elif event == 'exception':
                                        current_state_history.exception_state = ExceptionState(arg, lineno)

                                    if current_state_history:
                                        argvalues = inspect.getargvalues(frame)
                                        for arg in argvalues.locals:
                                            value = obj_value(argvalues.locals[arg])
                                            current_state_history.add_var_state(name=arg, value=value, lineno=lineno,
                                                                     inline=self.last_frame_line[current_entity_name])

                        self.last_frame_line[current_entity_name] = lineno
        return self.collect_flow
