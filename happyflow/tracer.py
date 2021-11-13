import trace
from happyflow.test_loader import UnittestLoader, PytestLoader
from happyflow.collector import Collector


class TraceRunner:

    def __init__(self):
        self.trace_collector = Collector()
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
