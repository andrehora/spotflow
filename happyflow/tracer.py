import trace
import inspect
import logging
from happyflow.utils import get_obj_value, line_has_explicit_return, find_full_name, check_is_generator_function
from happyflow.flow_state import StateResult, EntityTraceResult, ArgState, ReturnState, ExceptionState, TraceResult
from happyflow.test_loader import UnittestLoader, PytestLoader
from happyflow.target_model import TargetEntity


class TraceRunner:

    def __init__(self):
        self.trace_collector = TraceCollector()
        self.trace_result = self.trace_collector.trace_result

        self.target_entities = None
        self.run_source_entity = None

    def has_target_entities(self):
        return len(self.trace_collector.target_entities_cache) >= 1

    def run(self, source_entities):
        if type(source_entities) is not list:
            source_entities = [source_entities]

        for source_entity in source_entities:
            self.run_func(source_entity)

        # self.trace_data.traces = self.trace_collector.traces

    def run_func(self, func):

        if self.run_source_entity:
            func = self.run_source_entity(func)

        self.trace_collector.target_entity_names = self.target_entities

        # try:
        tracer = Trace2(count=1, trace=1, countfuncs=0, countcallers=0, trace_collector=self.trace_collector)
        tracer.runfunc(func)
        # func()
        # except Exception as e:
        #     logging.warning(f'Error run: {e}')


    @staticmethod
    def trace_from_tests(source_pattern='test*.py', target_entities=None):

        runner = TraceRunner()
        runner.target_entities = target_entities
        runner.run_source_entity = UnittestLoader.run_test

        tests = UnittestLoader().loadTestsFromName(source_pattern)
        runner.run(tests)
        return runner.trace_result

    @staticmethod
    def trace_from_test_class(test_class, target_entities=None):

        runner = TraceRunner()
        runner.target_entities = target_entities
        runner.run_source_entity = UnittestLoader.run_test

        tests = UnittestLoader().loadTestsFromTestCase(test_class)
        runner.run(tests)
        return runner.trace_result

    @staticmethod
    def trace_from_test_module(module, target_entities=None):

        runner = TraceRunner()
        runner.target_entities = target_entities
        runner.run_source_entity = UnittestLoader.run_test

        tests = UnittestLoader().loadTestsFromModule(module)
        runner.run(tests)
        return runner.trace_result

    @staticmethod
    def trace_from_pytest(pytests='.', target_entities=None):

        runner = TraceRunner()
        runner.target_entities = target_entities
        runner.run_source_entity = PytestLoader.run_test
        runner.run(pytests)

        return runner.trace_result

    @staticmethod
    def trace_from_func(source_funcs, target_entities=None):

        runner = TraceRunner()
        runner.target_entities = target_entities
        runner.run(source_funcs)

        return runner.trace_result


class Trace2(trace.Trace):

    def __init__(self, count=1, trace=1, countfuncs=0, countcallers=0,
                 ignoremods=(), ignoredirs=(), infile=None, outfile=None,
                 timing=False, trace_collector=None):

        super().__init__(count, trace, countfuncs, countcallers, ignoremods, ignoredirs, infile, outfile, timing)
        self.trace_collector = trace_collector

    def globaltrace_lt(self, frame, event, arg):

        if event == 'call':

            self.trace_collector.collect_flow_and_state(frame, event, arg)

            filename = frame.f_globals.get('__file__', None)
            if filename:
                modulename = trace._modname(filename)
                if modulename is not None:
                    ignore_it = self.ignore.names(filename, modulename)
                    if not ignore_it:
                        return self.localtrace
            else:
                return None

    def localtrace_trace_and_count(self, frame, event, arg):

        if event in ('line', 'return', 'exception'):
            self.trace_collector.collect_flow_and_state(frame, event, arg)

        return self.localtrace


class TraceCollector:

    def __init__(self):
        self.trace_result = TraceResult()
        self.target_entity_names = None

        self.last_frame_line = {}
        self.target_entities_cache = {}
        self.frame_cache = {}

    def find_arg_states(self, frame):
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

    def ensure_target_entity(self, current_entity_name, target_entity, frame):
        if not isinstance(target_entity, str):
            return target_entity

        if not current_entity_name.startswith(target_entity):
            return None

        if current_entity_name in self.target_entities_cache:
            return self.target_entities_cache[current_entity_name]

        func_or_method = self.ensure_func_or_method(frame)
        entity = TargetEntity.build_from_func(func_or_method)
        if not entity or not entity.is_target():
            return None

        self.target_entities_cache[current_entity_name] = entity
        return entity

    def ensure_func_or_method(self, frame):
        if frame.f_code.co_name in ['<listcomp>', '__next__', 'deepcopy', '_reconstruct']:
            return None

        filename = frame.f_code.co_filename
        # name = frame.f_code.co_name
        lineno = frame.f_lineno
        key = filename, lineno

        if key in self.frame_cache:
            return self.frame_cache[key]
        self.frame_cache[key] = self._find_func_or_method(frame)
        return self.frame_cache[key]

        # return self._find_func_or_method(frame)

    def _find_func_or_method(self, frame):
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

    def get_full_name(self, frame):
        func_or_method = self.ensure_func_or_method(frame)
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
        return callers

    def is_valid_collection(self, frame):

        if not self.target_entity_names:
            return False

        for target_entity_name in self.target_entity_names:
            if isinstance(target_entity_name, str):
                module_name = target_entity_name.split('.')[0]
                if module_name not in frame.f_code.co_filename:
                    return False
        return True

    def collect_flow_and_state(self, frame, event, arg):

        if not self.is_valid_collection(frame):
            return

        current_entity_name = self.get_full_name(frame)

        if current_entity_name:
            for target_entity_name in self.target_entity_names:
                target_entity = self.ensure_target_entity(current_entity_name, target_entity_name, frame)
                if target_entity and current_entity_name == target_entity.full_name:

                    if current_entity_name not in self.trace_result:
                        self.trace_result[current_entity_name] = EntityTraceResult(target_entity)

                    if current_entity_name not in self.last_frame_line:
                        self.last_frame_line[current_entity_name] = -1

                    if event == 'call':
                        # print(find_callers(frame))

                        flow_lines = []
                        state_result = StateResult(current_entity_name)
                        state_result.arg_states = self.find_arg_states(frame)

                        entity_result = self.trace_result[current_entity_name]
                        entity_result.add(flow_lines, state_result)

                    # event in ('line', 'return', 'exception')
                    else:
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
                            else:
                                # event == 'exception':
                                current_state_result.exception_state = ExceptionState(arg, lineno)

                            if current_state_result:
                                argvalues = inspect.getargvalues(frame)
                                for arg in argvalues.locals:
                                    value = get_obj_value(argvalues.locals[arg])
                                    current_state_result.add(name=arg, value=value, line=lineno,
                                                      inline=self.last_frame_line[current_entity_name])
                            self.last_frame_line[current_entity_name] = lineno
