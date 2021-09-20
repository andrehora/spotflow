import copy
import trace
from happyflow.utils import *
from happyflow.flow_state import StateResult, FlowResult, VarState
from happyflow.test_loader import UnittestLoader


class TraceRunner:

    def __init__(self):
        self.trace_result = TraceResult()
        self.trace_collector = TraceCollector()

        self.target_entities = None
        self.get_source_entity_name_wrapper = None
        self.run_source_entity_wrapper = None

    def run(self, source_entities):
        if type(source_entities) is not list:
            source_entities = [source_entities]

        for source_entity in source_entities:
            basic_trace = self._run_func(source_entity)
            self.trace_result.add_trace(basic_trace)

        self.trace_result.local_traces = self.trace_collector.local_traces

    def _run_func(self, func):

        if self.get_source_entity_name_wrapper:
            source_entity_name = self.get_source_entity_name_wrapper(func)
        else:
            source_entity_name = func.__name__

        if self.run_source_entity_wrapper:
            func = self.run_source_entity_wrapper(func)

        self.trace_collector.source_entity_name = source_entity_name
        self.trace_collector.target_entities = self.target_entities

        tracer = Trace2(count=1, trace=1, countfuncs=0, countcallers=0, trace_collector=self.trace_collector)

        # try:
        tracer.runfunc(func)
            # print('ok', func_name)
        # except:
        #     print('fail', func_name)

        result = tracer.results()
        return TraceCount(source_entity_name, result.counts)

    @staticmethod
    def trace_tests(source_pattern='test*.py', target_entities=None):

        runner = TraceRunner()
        runner.target_entities = target_entities
        runner.get_source_entity_name_wrapper = UnittestLoader.get_test_name
        runner.run_source_entity_wrapper = UnittestLoader.run_test

        tests = UnittestLoader().find_tests(source_pattern)
        runner.run(tests)

        return runner.trace_result

    @staticmethod
    def trace_funcs(source_funcs, target_entities=None):

        runner = TraceRunner()
        runner.target_entities = target_entities
        runner.run(source_funcs)

        return runner.trace_result


class TraceResult:

    def __init__(self):
        self.global_traces = []
        # self.sut_and_tests = {}
        self.local_traces = []

    def add_trace(self, t):
        self.global_traces.append(t)

    # def compute_sut_and_tests(self):
    #     for trace in self.traces:
    #         for sut in trace.run_funcs:
    #             self.sut_and_tests[sut] = self.sut_and_tests.get(sut, [])
    #             self.sut_and_tests[sut].append(trace.test_name)

    def global_sut_flows(self, sut):
        if not sut:
            return None

        result = FlowResult(sut)

        for base_sut in sut:
            for global_trace in self.global_traces:
                run_files_and_lines = global_trace.run_files_and_lines
                if base_sut.filename in run_files_and_lines:
                    lines = run_files_and_lines[base_sut.filename]
                    sut_flow = base_sut.intersection(lines)
                    if len(sut_flow) > 0:
                        result.add(global_trace.test_name, sut_flow)
        return result

    def local_sut_flows(self, sut):
        if not sut:
            return None

        result = FlowResult(sut)

        for base_sut in sut:
            target_sut_full_name = base_sut.full_name()
            for candidate_sut_full_name in self.local_traces:
                if candidate_sut_full_name == target_sut_full_name:
                    target_flows = self.local_traces[candidate_sut_full_name]
                    for test_name, sut_flow, state_result in target_flows:
                        if len(sut_flow) > 0:
                            result.add(test_name, sut_flow, state_result)
        return result


class TraceCount:

    def __init__(self, test_name, counts):
        self.test_name = test_name
        self.counts = counts
        self.run_files_and_lines = self.find_run_files_and_lines()
        # self.run_funcs = []
        # self.update_counts_with_executable_line()

    def find_run_files_and_lines(self):
        result = {}
        for event in self.counts:
            filename = event[0]
            line_number = event[1]
            result[filename] = result.get(filename, [])
            result[filename].append(line_number)
        return result

    # def update_counts_with_executable_line(self):
    #     for filename in self.run_files_and_lines:
    #         executable_lines = trace._find_executable_linenos(filename)
    #         for exec_line in executable_lines:
    #             key = (filename, exec_line)
    #             self.counts[key] = self.counts.get(key, 0)
    #
    # def get_counts(self, filename, line_number):
    #     return self.counts.get((filename, line_number), -1)
    #
    # def annotate_file(self, filename):
    #     with open(filename) as f:
    #         content = f.readlines()
    #         line_number = 0
    #         for line_code in content:
    #             line_number += 1
    #             exec_count = self.get_counts(filename, line_number)
    #             print(line_number, exec_count, line_code.rstrip())


class Trace2(trace.Trace):

    def __init__(self, count=1, trace=1, countfuncs=0, countcallers=0,
                 ignoremods=(), ignoredirs=(), infile=None, outfile=None,
                 timing=False, trace_collector=None):

        super().__init__(count, trace, countfuncs, countcallers, ignoremods, ignoredirs, infile, outfile, timing)
        self.trace_collector = trace_collector

    def globaltrace_lt(self, frame, why, arg):

        if why == 'call':

            self.trace_collector.collect_flow_and_state(frame, why)

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

        if why == "line" or why == 'return':
            self.trace_collector.collect_flow_and_state(frame, why)

        if why == "line":
            filename = frame.f_code.co_filename
            lineno = frame.f_lineno
            key = filename, lineno
            self.counts[key] = self.counts.get(key, 0) + 1

        return self.localtrace


class TraceCollector:

    def __init__(self):
        self.source_entity_name = None
        self.target_entities = None
        self.local_traces = {}
        # self.all_sut_states = {}

    def _run_func(self, frame):

        def wrap_func(*args, **kwargs): pass
        wrap_func.__code__ = frame.f_code
        wrap_func.__globals__.update(frame.f_globals)
        # print(wrap_func.__dict__)

        args = self._func_arg_values(frame)
        return wrap_func(*args)

    def _func_arg_values(self, frame):
        args = []

        argvalues = inspect.getargvalues(frame)
        for arg in argvalues.args:
            args.append(copy.deepcopy(argvalues.locals[arg]))

        if argvalues.varargs:
            args.append(copy.deepcopy(argvalues.locals['varargs']))

        if argvalues.keywords:
            args.append(copy.deepcopy(argvalues.locals['keywords']))

        return tuple(args)

    def _func_arg_names_and_values(self, frame):
        states = []

        argvalues = inspect.getargvalues(frame)
        for arg in argvalues.args:
            arg_state = VarState(arg, argvalues.locals[arg], frame.f_lineno)
            states.append(arg_state)

        if argvalues.varargs:
            arg_state = VarState('varargs', argvalues.locals['varargs'], frame.f_lineno)
            states.append(arg_state)

        if argvalues.keywords:
            arg_state = VarState('keywords', argvalues.locals['keywords'], frame.f_lineno)
            states.append(arg_state)

        return states

    def collect_flow_and_state(self, frame, why):

        if not self.target_entities:
            return

        entity_name = find_full_entity_name(frame)

        for target_entity in self.target_entities:

            if entity_name and target_entity.full_name() and entity_name == target_entity.full_name():
                if entity_name not in self.local_traces:
                    self.local_traces[entity_name] = []

                if why == 'call':
                    sut_flows = self.local_traces[entity_name]
                    state = StateResult(entity_name)
                    sut_flows.append((self.source_entity_name, [], state))

                    # collect args and return value
                    args = self._func_arg_names_and_values(frame)
                    return_value = self._run_func(frame)
                    state.args = args
                    state.return_value = return_value

                if why == 'line' or why == 'return':
                    sut_flows = self.local_traces[entity_name]
                    # get the last flow and update it
                    test_name, last_flow, last_state_result = sut_flows[-1]

                    lineno = frame.f_lineno
                    if why == 'line':
                        last_flow.append(lineno)

                    if last_state_result:
                        argvalues = inspect.getargvalues(frame)
                        for argvalue in argvalues.locals:
                            value = copy.copy(argvalues.locals[argvalue])
                            last_state_result.add(name=argvalue, value=value, line=lineno)
