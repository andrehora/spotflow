import inspect
import trace
from happyflow.utils import get_obj_value, line_has_explicit_return, find_full_name, check_is_generator_function
from happyflow.flow_state import StateResult, EntityTraceResult, ArgState, ReturnState, ExceptionState, TraceResult
from happyflow.target import TargetEntity


class Collector:

    def __init__(self):
        self.trace_result = TraceResult()
        self.target_entity_names = None

        self.last_frame_line = {}
        self.target_entities_cache = {}
        self.frame_cache = {}

    def get_arg_states(self, frame):
        states = []

        argvalues = inspect.getargvalues(frame)
        for arg in argvalues.args:
            value = get_obj_value(argvalues.locals[arg])

            arg_state = ArgState(arg, value, frame.f_lineno)
            states.append(arg_state)

        if argvalues.varargs:
            value = get_obj_value(argvalues.locals[argvalues.varargs])
            arg_state = ArgState(argvalues.varargs, value, frame.f_lineno)
            states.append(arg_state)

        if argvalues.keywords:
            value = get_obj_value(argvalues.locals[argvalues.keywords])
            arg_state = ArgState(argvalues.keywords, value, frame.f_lineno)
            states.append(arg_state)

        return states

    def ensure_target_entity(self, current_entity_name, target_entity, frame, event):
        if not isinstance(target_entity, str):
            return target_entity

        if not current_entity_name.startswith(target_entity):
            return None

        # if event == 'call':
        #     print(event, current_entity_name, target_entity)

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

        if key in self.frame_cache:
            return self.frame_cache[key]

        entity = self._find_func_or_method(frame, event)

        if not entity:
            return None

        self.frame_cache[key] = self._find_func_or_method(frame, event)
        return self.frame_cache[key]

    def _find_func_or_method(self, frame, event):
        try:
            entity_name = frame.f_code.co_name

            if entity_name in frame.f_globals:
                func_or_method = frame.f_globals[entity_name]
                return check_is_generator_function(func_or_method)

            if 'self' in frame.f_locals:
                obj = frame.f_locals['self']
                members = dict(inspect.getmembers(obj, inspect.ismethod))
                if entity_name in members:
                    func_or_method = members[entity_name]
                    return check_is_generator_function(func_or_method)
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

    def is_valid(self, frame):

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

    def global_trace(self, frame, event, arg):

        if event in ('call', 'line', 'return', 'exception'):

            self.collect_flow_and_state(frame, event, arg)

            filename = frame.f_globals.get('__file__', None)
            if filename:
                modulename = trace._modname(filename)
                if modulename is not None:
                    ignore_it = trace._Ignore().names(filename, modulename)
                    if not ignore_it:
                        return self.global_trace
            else:
                return None

    def collect_flow_and_state(self, frame, event, arg):

        if not self.is_valid(frame):
            return

        current_entity_name = self.get_full_entity_name(frame, event)

        if current_entity_name:
            for target_entity_name in self.target_entity_names:

                target_entity = self.ensure_target_entity(current_entity_name, target_entity_name, frame, event)

                if target_entity and current_entity_name == target_entity.full_name:

                    if current_entity_name not in self.last_frame_line:
                        self.last_frame_line[current_entity_name] = -1

                    if event == 'call':
                        if current_entity_name not in self.trace_result:
                            self.trace_result[current_entity_name] = EntityTraceResult(target_entity)

                        run_lines = []
                        state_result = StateResult()
                        state_result.arg_states = self.get_arg_states(frame)
                        callers = self.find_callers(frame)

                        entity_result = self.trace_result[current_entity_name]
                        entity_result.add(run_lines, state_result, callers)

                    elif event in ('line', 'return', 'exception'):
                        if current_entity_name in self.trace_result:

                            entity_result = self.trace_result[current_entity_name]

                            if entity_result.flows:

                                flow = entity_result.get_last_flow()
                                current_run_lines = flow.run_lines
                                current_state_result = flow.state_result

                                lineno = frame.f_lineno
                                if event == 'line':
                                    current_run_lines.append(lineno)
                                elif event == 'return':
                                    has_return = line_has_explicit_return(frame)
                                    current_state_result.return_state = ReturnState(get_obj_value(arg), lineno, has_return)
                                elif event == 'exception':
                                    current_state_result.exception_state = ExceptionState(arg, lineno)

                                if current_state_result:
                                    argvalues = inspect.getargvalues(frame)
                                    for arg in argvalues.locals:
                                        value = get_obj_value(argvalues.locals[arg])
                                        current_state_result.add(name=arg, value=value, line=lineno,
                                                          inline=self.last_frame_line[current_entity_name])
                                self.last_frame_line[current_entity_name] = lineno

        return self.collect_flow_and_state
