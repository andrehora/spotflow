import copy
import trace
from happyflow.utils import *
from happyflow.sut_flow_state import SUTStateResult, SUTFlowResult
from happyflow.test_loader import UnittestFramework, TestLoader


class TraceRunner:

    def __init__(self, func_finder_and_runner=UnittestFramework()):
        self.func_finder_and_runner = func_finder_and_runner
        self.trace_result = TraceResult()
        self.local_trace_collector = TraceCollector()
        self.sut = None

    def run(self, funcs):

        for f in funcs:
            basic_trace = self.run_func(f)
            self.trace_result.add_trace(basic_trace)

        self.trace_result.local_traces = self.local_trace_collector.local_traces

        # self.test_result.compute_sut_and_tests()

    def run_func(self, func_to_run):

        func_name = self.func_finder_and_runner.get_func_name(func_to_run)
        func = self.func_finder_and_runner.run_func(func_to_run)

        self.local_trace_collector.func_name = func_name
        self.local_trace_collector.sut = self.sut

        tracer = Trace2(count=1, trace=1, countfuncs=0, countcallers=0, trace_collector=self.local_trace_collector)

        # try:
        tracer.runfunc(func)
            # print('ok', func_name)
        # except:
        #     print('fail', func_name)

        result = tracer.results()
        return TraceCount(func_name, result.counts)

    @staticmethod
    def trace(pattern='test*.py', sut=None):
        tests = TestLoader().find_tests(pattern)
        runner = TraceRunner()
        runner.sut = sut
        runner.run(tests)
        return runner.trace_result


class TraceResult:

    def __init__(self):
        self.global_traces = []
        # self.sut_and_tests = {}
        self.local_traces = []

    def add_trace(self, trace):
        self.global_traces.append(trace)

    # def compute_sut_and_tests(self):
    #     for trace in self.traces:
    #         for sut in trace.run_funcs:
    #             self.sut_and_tests[sut] = self.sut_and_tests.get(sut, [])
    #             self.sut_and_tests[sut].append(trace.test_name)

    def global_sut_flows(self, sut):
        if not sut:
            return None

        result = SUTFlowResult(sut)

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

        result = SUTFlowResult(sut)

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
            code = frame.f_code

            self.trace_collector.collect_flow_and_state(frame, 'global', why)

            filename = frame.f_globals.get('__file__', None)
            if filename:
                # XXX _modname() doesn't work right for packages, so
                # the ignore support won't work right for packages
                modulename = trace._modname(filename)
                if modulename is not None:
                    ignore_it = self.ignore.names(filename, modulename)
                    if not ignore_it:
                        # if self.trace:
                        #     print((" --- modulename: %s, funcname: %s"
                        #            % (modulename, code.co_name)))
                        return self.localtrace
            else:
                return None

    def localtrace_trace_and_count(self, frame, why, arg):

        if why == "line" or why == 'return':

            # CHANGE
            self.trace_collector.collect_flow_and_state(frame, 'local', why)

        if why == "line":

            # record the file name and line number of every trace
            filename = frame.f_code.co_filename
            lineno = frame.f_lineno
            key = filename, lineno
            self.counts[key] = self.counts.get(key, 0) + 1

            # if self.start_time:
            #     print('%.2f' % (_time() - self.start_time), end=' ')
            # bname = os.path.basename(filename)
            # print("%s(%d): %s" % (bname, lineno,
            #                       linecache.getline(filename, lineno)), end='')
        return self.localtrace


class TraceCollector:

    def __init__(self):
        self.func_name = None
        self.sut = None
        self.local_traces = {}
        # self.all_sut_states = {}

    def collect_flow_and_state(self, frame, data_type, why):

        if not self.sut:
            return

        entity_name = find_full_func_name(frame)

        for base_sut in self.sut:

            if entity_name and base_sut.full_name() and entity_name == base_sut.full_name():
                if entity_name not in self.local_traces:
                    self.local_traces[entity_name] = []

                if data_type == 'global':
                    sut_flows = self.local_traces[entity_name]
                    state = SUTStateResult(entity_name)
                    sut_flows.append((self.func_name, [], state))

                if data_type == 'local':
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
