import trace
import inspect
import logging
from happyflow.utils import str_or_type, find_full_entity_name, line_has_explicit_return, try_copy
from happyflow.flow_state import StateResult, RunResult, ArgState, ReturnState
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

        self.trace_collector.return_states = []
        self.trace_collector.source_entity_name = source_entity_name
        self.trace_collector.target_entities = self.target_entities


        try:
            tracer = Trace2(count=1, trace=1, countfuncs=0, countcallers=0, trace_collector=self.trace_collector)

            self.trace_collector.call_id = 0
            self.trace_collector.collect_return_state = False
            tracer.runfunc(func)

            result = tracer.results()
            return TraceCount(source_entity_name, result.counts)
        except Exception:
            logging.warning('Error run')


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
        self.local_traces = []

    def add_trace(self, t):
        self.global_traces.append(t)

    def global_sut_flows(self, sut):
        if not sut:
            return None

        result = RunResult(sut)

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

        results = []
        for base_sut in sut:
            result = RunResult(base_sut)
            target_sut_full_name = base_sut.full_name()
            for candidate_sut_full_name in self.local_traces:
                if candidate_sut_full_name == target_sut_full_name:
                    target_flows = self.local_traces[candidate_sut_full_name]
                    for test_name, sut_flow, state_result in target_flows:
                        if len(sut_flow) > 0:
                            result.add(test_name, sut_flow, state_result)
            results.append(result)
        # if len(results) == 1:
        #     return results[0]
        return results


class TraceCount:

    def __init__(self, test_name, counts):
        self.test_name = test_name
        self.counts = counts
        self.run_files_and_lines = self.find_run_files_and_lines()

    def find_run_files_and_lines(self):
        result = {}
        for event in self.counts:
            filename = event[0]
            line_number = event[1]
            result[filename] = result.get(filename, [])
            result[filename].append(line_number)
        return result


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

        if why == "line" or why == 'return':
            self.trace_collector.collect_flow_and_state(frame, why, arg)

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
        self.last_entity_line = {}

    def func_arg_states(self, frame):
        states = []

        argvalues = inspect.getargvalues(frame)
        for arg in argvalues.args:
            value = str_or_type(argvalues.locals[arg])
            arg_state = ArgState(arg, value, frame.f_lineno)
            states.append(arg_state)

        if argvalues.varargs:
            value = str_or_type(argvalues.locals[argvalues.varargs])
            arg_state = ArgState(argvalues.varargs, value, frame.f_lineno)
            states.append(arg_state)

        if argvalues.keywords:
            value = str_or_type(argvalues.locals[argvalues.keywords])
            arg_state = ArgState(argvalues.keywords, value, frame.f_lineno)
            states.append(arg_state)

        return states

    def collect_flow_and_state(self, frame, why, return_value):

        if not self.target_entities:
            return
        entity_name = find_full_entity_name(frame)

        for target_entity in self.target_entities:

            if entity_name and target_entity.full_name() and entity_name == target_entity.full_name():

                if entity_name not in self.local_traces:
                    self.local_traces[entity_name] = []

                if entity_name not in self.last_entity_line:
                    self.last_entity_line[entity_name] = -1

                if why == 'call':
                    target_entity_flow = self.local_traces[entity_name]
                    state = StateResult(entity_name)
                    target_entity_flow.append((self.source_entity_name, [], state))

                    # save arg states
                    state.args = self.func_arg_states(frame)

                if why == 'line' or why == 'return':
                    target_entity_flow = self.local_traces[entity_name]
                    # get the last flow and update it
                    source_entity_name, current_flow, current_state = target_entity_flow[-1]

                    lineno = frame.f_lineno
                    if why == 'line':
                        current_flow.append(lineno)
                    if why == 'return':
                        # save return states
                        has_return = line_has_explicit_return(frame)
                        current_state.return_state = ReturnState(str_or_type(return_value), lineno, has_return)

                    if current_state:
                        argvalues = inspect.getargvalues(frame)
                        for arg in argvalues.locals:
                            value = str_or_type(argvalues.locals[arg])
                            current_state.add(name=arg, value=value, line=lineno,
                                              inline=self.last_entity_line[entity_name])
                    self.last_entity_line[entity_name] = lineno

