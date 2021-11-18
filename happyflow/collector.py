import inspect
from happyflow.utils import obj_value, line_has_explicit_return, find_full_name, line_has_yield
from happyflow.flow_state import StateResult, EntityTraceResult, ArgState, ReturnState, YieldState, ExceptionState, TraceResult
from happyflow.target import TargetEntity
from happyflow.tracer import PyTracer


class Collector:

    def __init__(self):
        self.trace_result = TraceResult()
        self.target_entity_names = None

        self.last_frame_line = {}
        self.target_entities_cache = {}
        self.frame_cache = {}

        self.py_tracer = PyTracer(self)

    def start(self):
        self.py_tracer.start_tracer()

    def stop(self):
        self.py_tracer.stop_tracer()

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

    def ensure_target_entity(self, current_entity_name, target_entity, frame, event):
        if not isinstance(target_entity, str):
            return target_entity

        if not current_entity_name.startswith(target_entity):
            return None

        if current_entity_name in self.target_entities_cache:
            return self.target_entities_cache[current_entity_name]

        func_or_method = self.ensure_func_or_method(frame, event)

        entity = TargetEntity.build_from_func(func_or_method)
        if not entity or not entity.is_target():
            return None

        self.target_entities_cache[current_entity_name] = entity
        return entity

    def ensure_func_or_method(self, frame, event):
        filename = frame.f_code.co_filename
        lineno = frame.f_lineno
        key = filename, lineno
        # key = id(frame)

        if key in self.frame_cache:
            return self.frame_cache[key]

        entity = self._get_func_or_method(frame, event)
        if not entity:
            return None

        self.frame_cache[key] = self._get_func_or_method(frame, event)
        return self.frame_cache[key]

    def _get_func_or_method(self, frame, event):
        try:
            entity_name = frame.f_code.co_name

            if entity_name in frame.f_globals:
                func_or_method = frame.f_globals[entity_name]
                # return check_is_generator_function(func_or_method)
                return func_or_method

            if 'self' in frame.f_locals:
                obj = frame.f_locals['self']
                members = dict(inspect.getmembers(obj, inspect.ismethod))
                if entity_name in members:
                    func_or_method = members[entity_name]
                    # return check_is_generator_function(func_or_method)
                    return func_or_method
        except Exception as e:
            return None

    def get_full_entity_name(self, frame, event):

        func_or_method = self.ensure_func_or_method(frame, event)

        if func_or_method:
            return find_full_name(func_or_method)

        return None

    def find_callers(self, frame):
        callers = []
        callers.append(frame.f_code.co_name)
        while 'test' not in frame.f_code.co_name:
            frame = frame.f_back
            callers.append(frame.f_code.co_name)
        callers.reverse()
        return tuple(callers)

    def is_valid_frame(self, frame):

        if not self.target_entity_names:
            return False

        # example: <module>, <genexpr>, <listcomp>
        if frame.f_code.co_name.startswith('<'):
            return False

        for target_entity_name in self.target_entity_names:
            if isinstance(target_entity_name, str):
                module_name = target_entity_name.split('.')[0]
                if module_name not in frame.f_code.co_filename:
                    return False
        return True

    # def global_trace(self, frame, event, arg):
    #
    #     if event in ('call', 'line', 'return', 'exception'):
    #
    #         self.collect_flow_and_state(frame, event, arg)
    #
    #         filename = frame.f_globals.get('__file__', None)
    #         if filename:
    #             modulename = trace._modname(filename)
    #             if modulename is not None:
    #                 ignore_it = trace._Ignore().names(filename, modulename)
    #                 if not ignore_it:
    #                     return self.global_trace
    #         else:
    #             return None

    def collect_flow_and_state(self, frame, event, arg):

        if not self.is_valid_frame(frame):
            return

        current_entity_name = self.get_full_entity_name(frame, event)
        # print(current_entity_name, frame.f_lineno, event, id(frame))

        if current_entity_name:
            for target_entity_name in self.target_entity_names:

                target_entity = self.ensure_target_entity(current_entity_name, target_entity_name, frame, event)
                if target_entity and current_entity_name == target_entity.full_name:

                    if current_entity_name not in self.last_frame_line:
                        self.last_frame_line[current_entity_name] = -1

                    # Tip from Coverage.py :)
                    # The call event is really a "start frame" event, and happens for
                    # function calls and re-entering generators.  The f_lasti field is
                    # -1 for calls, and a real offset for generators.  Use <0 as the
                    # line number for calls, and the real line number for generators.
                    if event == 'call' and getattr(frame, 'f_lasti', -1) < 0:

                        if current_entity_name not in self.trace_result:
                            self.trace_result[current_entity_name] = EntityTraceResult(target_entity)

                        run_lines = []
                        state_result = StateResult()
                        state_result.arg_states = self.get_arg_states(frame)
                        callers = self.find_callers(frame)

                        entity_result = self.trace_result[current_entity_name]
                        entity_result.add(run_lines, state_result, callers, id(frame))

                    # Event is line, return, exception or call for re-entering generators
                    else:
                        lineno = frame.f_lineno
                        if current_entity_name in self.trace_result:
                            entity_result = self.trace_result[current_entity_name]
                            if entity_result.flows:

                                # flow = entity_result.get_last_flow()
                                flow = entity_result.get_flow_from_id(id(frame))
                                if flow:
                                    current_run_lines = flow.run_lines
                                    current_state_result = flow.state_result

                                    if event == 'line':
                                        current_run_lines.append(lineno)

                                    elif event == 'return':

                                        if line_has_explicit_return(frame):
                                            current_state_result.add_return_state(obj_value(arg), lineno)

                                        elif line_has_yield(frame):
                                            current_state_result.add_yield_state(obj_value(arg), lineno)

                                    elif event == 'exception':
                                        current_state_result.exception_state = ExceptionState(arg, lineno)

                                    if current_state_result:
                                        argvalues = inspect.getargvalues(frame)
                                        for arg in argvalues.locals:
                                            value = obj_value(argvalues.locals[arg])
                                            current_state_result.add_var_state(name=arg, value=value, lineno=lineno,
                                                                     inline=self.last_frame_line[current_entity_name])
                        self.last_frame_line[current_entity_name] = lineno
        return self.collect_flow_and_state
