import ast
import trace
from happyflow import trace2
import unittest
import os
from happyflow import trace_inspect


def open_file(filename):
    try:
        # print(filename)
        with open(filename, 'r', encoding="utf-8") as f:
            return f.read()
    except:
        return None


def find_python_files(dir='.'):
    python_files = []
    for r, d, f in os.walk(dir):
        for file in f:
            if file.endswith('.py'):
                abs_dir = os.path.join(os.getcwd(), r, file)
                # if 'test' not in abs_dir:
                python_files.append(os.path.abspath(abs_dir))
    return python_files


def find_module_name(filename):
    return filename.split('/')[-1].split('.')[0]


class PyTestFramework:
    pass


class UnittestFramework:

    def find_tests(self, pattern):

        loader = unittest.TestLoader()
        # suite = loader.discover('.', pattern)
        suite = loader.loadTestsFromName(pattern)

        return self._find_test_methods(suite)

    def _find_test_methods(self, suite):

        def find(suite, test_methods):
            if issubclass(suite.__class__, unittest.TestCase):
                test_methods.append(suite)
                return
            for test in suite._tests:
                find(test, test_methods)

        test_methods = []
        find(suite, test_methods)
        return test_methods

    def run_test(self, test):
        runner = unittest.TextTestRunner()

        def run():
            runner.run(test)

        return run

    def get_test_name(self, test):
        return test._testMethodName


class TestLoader:

    def __init__(self, testing_framework='unittest'):
        self.tests = []
        self.testing_framework_class = UnittestFramework

        if testing_framework == 'pytest':
            self.testing_framework_class = PyTestFramework

    def find_tests(self, pattern='test*.py'):
        self.tests = self.testing_framework_class().find_tests(pattern)
        return self.tests


class TestRunner:

    def __init__(self, testing_framework_class=UnittestFramework, project_folder=''):
        self.testing_framework_class = testing_framework_class
        self.project_folder = project_folder
        self.result = TraceResult()

    def run(self, tests):
        for test in tests:
            func_trace = self.run_test(test)
            self.result.add(func_trace)
        self.result.compute_sut_and_tests()

    def run_test(self, test):
        testing_framework = self.testing_framework_class()
        func = testing_framework.run_test(test)
        test_name = testing_framework.get_test_name(test)

        tracer = trace2.Trace2(count=1, trace=1, countfuncs=0, countcallers=0, test_name=test_name)

        # try:
        tracer.runfunc(func)
        print('ok', test)
        # except:
        print('fail', test)

        result = tracer.results()
        return TestTrace(test_name, result.counts, self.project_folder)


    @staticmethod
    def trace(pattern='test*.py'):
        tests = TestLoader().find_tests(pattern)
        runner = TestRunner()
        runner.run(tests)
        return runner.result


class TraceResult:

    def __init__(self):
        self.traces = []
        self.sut_and_tests = {}

        trace_inspect.clean_inspection()
        self.all_sut_flows = trace_inspect.all_sut_flows

    def add(self, trace):
        self.traces.append(trace)

    def compute_sut_and_tests(self):
        for trace in self.traces:
            for sut in trace.run_funcs:
                self.sut_and_tests[sut] = self.sut_and_tests.get(sut, [])
                self.sut_and_tests[sut].append(trace.test_name)

    def composite_sut_flows(self, sut):
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

    def base_sut_flows(self, sut):
        if not sut:
            return None

        result = SUTFlowResult(sut)
        sut_fullname = sut.full_name()

        if sut_fullname in self.all_sut_flows:
            target_flows = self.all_sut_flows[sut_fullname]
            for test_name, sut_flow, state_result in target_flows:
                if len(sut_flow) > 0:
                    result.add(test_name, sut_flow, state_result)
        return result


class SUTFlowResult:

    def __init__(self, sut):
        self.sut = sut
        self.sut_name = sut.name
        self.test_names = []
        self.flows = []

    def add(self, test_name, flow, state_result=None):
        self.test_names.append(test_name)
        flow = SUTFlow(test_name, flow, state_result)
        self.flows.append(flow)

    def number_of_tests(self):
        return len(self.test_names)


class SUTFlow:

    def __init__(self, test_name, run_lines, state_result=None):
        self.test_name = test_name
        self.run_lines = run_lines
        self.state_result = state_result

    def __eq__(self, other):
        return other == self.run_lines

    def distinct_lines(self):
        return sorted(list(set(self.run_lines)))


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


class SUTVisitor(ast.NodeVisitor):

    def __init__(self, sut, module_name, filename):
        self.sut = sut
        self.module_name = module_name
        self.filename = filename

    def visit_Module(self, node):
        for element in node.body:
            if isinstance(element, ast.FunctionDef):
                self.visit_function(element)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_ClassDef(self, node):
        clazz = self.sut.add_class(self.module_name, node.name, node.lineno, node.end_lineno, self.filename)
        for element in node.body:
            if isinstance(element, ast.FunctionDef):
                self.visit_method(element, clazz)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_function(self, node):
        self.sut.add_function(self.module_name, node.name, node.lineno, node.end_lineno, self.filename)

    def visit_method(self, node, clazz):
        self.sut.add_method(self.module_name, node.name, node.lineno, node.end_lineno, clazz, self.filename)


class SUTLoader:

    def __init__(self, dir='.'):
        self.dir = dir
        self.sut_container = SUTContainer()

    def load_sut(self):
        python_files = find_python_files(self.dir)
        for filename in python_files:
            module_code = open_file(filename)
            if module_code:
                module_node = ast.parse(module_code)
                module_name = find_module_name(filename)

                visitor = SUTVisitor(self.sut_container, module_name, filename)
                visitor.visit(module_node)

    @staticmethod
    def find_sut(sut_name, dir='.'):
        loader = SUTLoader(dir)
        loader.load_sut()
        return loader.sut_container.get(sut_name)


class SUTContainer:

    def __init__(self):
        self.suts = []
        self.suts_map = {}

    def full_name(self):
        return 'SUTContainer'

    def __str__(self):
        return f'suts: {len(self.suts)}'

    def get(self, sut_name):
        return self.suts_map[sut_name]

    def add_class(self, module_name, class_name, start_line, end_line, filename):
        c = SUTClass(module_name, class_name)
        c.start_line = start_line
        c.end_line = end_line
        c.filename = filename
        self.suts.append(c)
        self.suts_map[str(c)] = c
        return c

    def add_method(self, module_name, method_name, start_line, end_line, clazz, filename):
        m = SUTMethod(module_name, method_name, clazz)
        m.start_line = start_line
        m.end_line = end_line
        m.filename = filename
        clazz.add_method(m)
        self.suts_map[str(m)] = m
        return m

    def add_function(self, module_name, function_name, start_line, end_line, filename):
        f = SUTFunction(module_name, function_name)
        f.start_line = start_line
        f.end_line = end_line
        f.filename = filename
        self.suts.append(f)
        self.suts_map[str(f)] = f
        return f

    def run(self, result):
        for sut in self.suts:
            sut.run(result)


class SUT:
    start_line = 0
    end_line = 0
    filename = ''

    def composite_flows(self, trace_result):
        return trace_result.composite_sut_flows(self)

    def base_flows(self, trace_result):
        return trace_result.base_sut_flows(self)

    def executable_lines(self):
        executable_lines = trace._find_executable_linenos(self.filename)
        return self.intersection(executable_lines)[1:]

    def intersection(self, other_lines):
        my_lines = range(self.start_line, self.end_line + 1)
        return sorted(list(set(my_lines).intersection(other_lines)))

    def loc(self):
        return self.end_line - self.start_line

    def full_name(self):
        pass

    def summary(self):
        return f'{self.full_name()} (lines: {self.start_line}-{self.end_line})'

    def __str__(self):
        return self.full_name()


class SUTClass(SUT):

    def __init__(self, module_name, name, filename=''):
        self.module_name = module_name
        self.name = name
        self.filename = filename
        self.methods = []

    def add_method(self, method):
        self.methods.append(method)

    def run(self, result):
        for method in self.methods:
            method.run(result)

    def full_name(self):
        return f'{self.module_name}.{self.name}'


class SUTMethod(SUT):

    def __init__(self, module_name, name, clazz, filename=''):
        self.module_name = module_name
        self.name = name
        self.clazz = clazz
        self.filename = filename

    def run(self, result):
        pass

    def full_name(self):
        return f'{self.module_name}.{self.clazz.name}.{self.name}'


class SUTFunction(SUT):

    def __init__(self, module_name, name, filename=''):
        self.module_name = module_name
        self.name = name
        self.filename = filename

    def run(self, result):
        pass

    def full_name(self):
        return f'{self.module_name}.{self.name}'


