import trace
from happyflow.loader import UnittestFramework, TestLoader
from happyflow.sut_model import SUTFlowResult
from happyflow import sut_tracer


class TestRunner:

    def __init__(self, testing_framework_class=UnittestFramework, project_folder=''):
        self.testing_framework_class = testing_framework_class
        self.project_folder = project_folder
        self.result = TestResult()
        self.sut_full_name = None

    def run(self, tests):
        for test in tests:
            func_trace = self.run_test(test)
            self.result.add(func_trace)
        self.result.compute_sut_and_tests()

    def run_test(self, test):
        testing_framework = self.testing_framework_class()
        func = testing_framework.run_test(test)
        test_name = testing_framework.get_test_name(test)

        tracer = sut_tracer.Trace2(count=1, trace=1, countfuncs=0, countcallers=0,
                                   test_name=test_name, sut_full_name=self.sut_full_name)

        try:
            tracer.runfunc(func)
            print('ok', test)
        except:
            print('fail', test)

        result = tracer.results()
        return TestTrace(test_name, result.counts, self.project_folder)


    @staticmethod
    def trace(pattern='test*.py', sut_full_name=None):
        tests = TestLoader().find_tests(pattern)
        runner = TestRunner()
        runner.sut_full_name = sut_full_name
        runner.run(tests)
        return runner.result


class TestResult:

    def __init__(self):
        self.traces = []
        self.sut_and_tests = {}

        sut_tracer.clean_inspection()
        self.all_sut_flows = sut_tracer.all_sut_flows

    def add(self, trace):
        self.traces.append(trace)

    def compute_sut_and_tests(self):
        for trace in self.traces:
            for sut in trace.run_funcs:
                self.sut_and_tests[sut] = self.sut_and_tests.get(sut, [])
                self.sut_and_tests[sut].append(trace.test_name)

    def global_sut_flows(self, sut):
        if not sut:
            return None

        result = SUTFlowResult(sut)
        for trace in self.traces:
            run_files_and_lines = trace.run_files_and_lines
            if sut.filename in run_files_and_lines:
                lines = run_files_and_lines[sut.filename]
                sut_flow = sut.intersection(lines)
                if len(sut_flow) > 0:
                    result.add(trace.test_name, sut_flow)
        return result

    def local_sut_flows(self, sut):
        if not sut:
            return None
        result = SUTFlowResult(sut)
        target_sut_full_name = sut.full_name()

        for candidate_sut_full_name in self.all_sut_flows:
            if candidate_sut_full_name.startswith(target_sut_full_name):
                target_flows = self.all_sut_flows[candidate_sut_full_name]
                for test_name, sut_flow, state_result in target_flows:
                    if len(sut_flow) > 0:
                        result.add(test_name, sut_flow, state_result)
        return result


class TestTrace:

    def __init__(self, test_name, counts, project_folder=''):
        self.test_name = test_name
        self.counts = counts

        self.run_files_and_lines = self.find_run_files_and_lines(project_folder)
        self.run_funcs = []
        # self.update_counts_with_executable_line()

    def find_run_files_and_lines(self, project_folder):
        result = {}
        for event in self.counts:
            filename = event[0]
            line_number = event[1]
            if project_folder in filename:
                result[filename] = result.get(filename, [])
                result[filename].append(line_number)
        return result

    def update_counts_with_executable_line(self):
        for filename in self.run_files_and_lines:
            executable_lines = trace._find_executable_linenos(filename)
            for exec_line in executable_lines:
                key = (filename, exec_line)
                self.counts[key] = self.counts.get(key, 0)

    def get_counts(self, filename, line_number):
        return self.counts.get((filename, line_number), -1)

    def annotate_file(self, filename):
        with open(filename) as f:
            content = f.readlines()
            line_number = 0
            for line_code in content:
                line_number += 1
                exec_count = self.get_counts(filename, line_number)
                print(line_number, exec_count, line_code.rstrip())
