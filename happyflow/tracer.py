import trace
import inspect
import logging
from happyflow.utils import copy_or_type, find_full_entity_name, line_has_explicit_return, find_callers
from happyflow.flow_state import StateResult, RunResult, ArgState, ReturnState, ExceptionState
from happyflow.test_loader import UnittestLoader, PytestLoader
from happyflow.target_loader import TargetEntityLoader
from happyflow.target_model import TargetContainerEntity


class TraceRunner:

    def __init__(self):
        self.trace_collector = TraceCollector()
        self.run_results = self.trace_collector.run_results

        self.target_entities = None
        self.run_source_entity_wrapper = None

    def get_target_entities(self):
        container = TargetContainerEntity()
        for entity in self.trace_collector.target_entities_cache:
            container.add_entity(self.trace_collector.target_entities_cache[entity])
        return container

    def has_target_entities(self):
        return len(self.trace_collector.target_entities_cache) >= 1

    def run(self, source_entities):
        if type(source_entities) is not list:
            source_entities = [source_entities]

        for source_entity in source_entities:
            self.run_func(source_entity)

        # self.trace_data.traces = self.trace_collector.traces

    def run_func(self, func):

        if self.run_source_entity_wrapper:
            func = self.run_source_entity_wrapper(func)

        self.trace_collector.target_entities = self.target_entities

        try:
            tracer = Trace2(count=1, trace=1, countfuncs=0, countcallers=0, trace_collector=self.trace_collector)
            tracer.runfunc(func)
        except Exception as e:
            logging.warning(f'Error run: {e}')


    @staticmethod
    def trace_from_tests(source_pattern='test*.py', target_entities=None):

        runner = TraceRunner()
        runner.target_entities = target_entities
        runner.run_source_entity_wrapper = UnittestLoader.run_test

        tests = UnittestLoader().loadTestsFromName(source_pattern)
        runner.run(tests)
        return runner.run_results

    @staticmethod
    def trace_from_test_class(test_class, target_entities=None):

        runner = TraceRunner()
        runner.target_entities = target_entities
        runner.run_source_entity_wrapper = UnittestLoader.run_test

        tests = UnittestLoader().loadTestsFromTestCase(test_class)
        runner.run(tests)

        if runner.has_target_entities():
            return runner.trace_data, runner.get_target_entities()

        return runner.trace_data

    @staticmethod
    def trace_from_test_module(module, target_entities=None):

        runner = TraceRunner()
        runner.target_entities = target_entities
        runner.run_source_entity_wrapper = UnittestLoader.run_test

        tests = UnittestLoader().loadTestsFromModule(module)
        runner.run(tests)

        if runner.has_target_entities():
            return runner.trace_data, runner.get_target_entities()

        return runner.trace_data

    @staticmethod
    def trace_from_pytest(pytests='.', target_entities=None):

        runner = TraceRunner()
        runner.target_entities = target_entities
        runner.get_source_entity_name_wrapper = PytestLoader.get_suite_name
        runner.run_source_entity_wrapper = PytestLoader.run_test

        runner.run(pytests)

        if runner.has_target_entities():
            return runner.trace_data, runner.get_target_entities()

        return runner.trace_data

    @staticmethod
    def trace_from_func(source_funcs, target_entities=None):

        runner = TraceRunner()
        runner.target_entities = target_entities
        runner.run(source_funcs)

        return runner.trace_data


class Trace2(trace.Trace):

    def __init__(self, count=1, trace=1, countfuncs=0, countcallers=0,
                 ignoremods=(), ignoredirs=(), infile=None, outfile=None,
                 timing=False, trace_collector=None):

        super().__init__(count, trace, countfuncs, countcallers, ignoremods, ignoredirs, infile, outfile, timing)
        self.trace_collector = trace_collector

    def globaltrace_lt(self, frame, why, arg):

        if why == 'call':

            self.trace_collector.collect_flow_and_state(frame, why, arg)

            filename = frame.f_globals.get('__file__', None)
            if filename:
                modulename = trace._modname(filename)
                if modulename is not None:
                    ignore_it = self.ignore.names(filename, modulename)
                    if not ignore_it:
                        return self.localtrace
            else:
                return None

    def localtrace_trace_and_count(self, frame, why, arg):

        if why in ('line', 'return', 'exception'):
            self.trace_collector.collect_flow_and_state(frame, why, arg)

        return self.localtrace


class TraceCollector:

    def __init__(self):
        self.run_results = []

        self.target_entities = None
        self.traces = {}
        self.last_frame_line = {}
        self.target_entities_cache = {}

    def find_arg_states(self, frame):
        states = []

        argvalues = inspect.getargvalues(frame)
        for arg in argvalues.args:
            value = copy_or_type(argvalues.locals[arg])
            arg_state = ArgState(arg, value, frame.f_lineno)
            states.append(arg_state)

        if argvalues.varargs:
            value = copy_or_type(argvalues.locals[argvalues.varargs])
            arg_state = ArgState(argvalues.varargs, value, frame.f_lineno)
            states.append(arg_state)

        if argvalues.keywords:
            value = copy_or_type(argvalues.locals[argvalues.keywords])
            arg_state = ArgState(argvalues.keywords, value, frame.f_lineno)
            states.append(arg_state)

        return states

    def ensure_target_entity(self, entity_name, target_entity, frame):
        if not entity_name.startswith(target_entity):
            return None

        if entity_name in self.target_entities_cache:
            return self.target_entities_cache[entity_name]

        entity = TargetEntityLoader.load_from_frame(frame)
        if not entity or not entity.is_target():
            return None

        self.target_entities_cache[entity_name] = entity
        return entity

    def collect_flow_and_state(self, frame, why, arg):

        if not self.target_entities:
            return

        entity_name = find_full_entity_name(frame)

        for target_entity in self.target_entities:
            if type(target_entity) is str:
                target_entity = self.ensure_target_entity(entity_name, target_entity, frame)

            if entity_name and target_entity and entity_name == target_entity.full_name():

                if entity_name not in self.traces:
                    run_result = RunResult(target_entity)
                    self.run_results.append(run_result)
                    self.traces[entity_name] = []

                if entity_name not in self.last_frame_line:
                    self.last_frame_line[entity_name] = -1

                if why == 'call':
                    # print(find_callers(frame))

                    flow_lines = []
                    state_result = StateResult(entity_name)
                    state_result.args = self.find_arg_states(frame)

                    run_result = self.run_results[-1]
                    run_result.add(flow_lines, state_result)

                    collector = self.traces[entity_name]
                    collector.append((flow_lines, state_result))

                # why in ('line', 'return', 'exception')
                else:
                    collector = self.traces[entity_name]
                    current_flow_lines, current_state = collector[-1]

                    lineno = frame.f_lineno
                    if why == 'line':
                        current_flow_lines.append(lineno)
                    elif why == 'return':
                        has_return = line_has_explicit_return(frame)
                        current_state.return_state = ReturnState(copy_or_type(arg), lineno, has_return)
                    else:
                        # why == 'exception':
                        current_state.exception_state = ExceptionState(arg, lineno)

                    if current_state:
                        argvalues = inspect.getargvalues(frame)
                        for arg in argvalues.locals:
                            value = copy_or_type(argvalues.locals[arg])
                            current_state.add(name=arg, value=value, line=lineno,
                                              inline=self.last_frame_line[entity_name])
                    self.last_frame_line[entity_name] = lineno
