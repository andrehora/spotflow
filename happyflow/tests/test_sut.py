import unittest
from happyflow.sut_model import SUTSourceEntity, SUTFunction, SUTMethod, SUTClass, SUTModule
from happyflow.sut_loader import SUTLoader
from happyflow.test_loader import TestLoader
from happyflow.tracer import TraceRunner


class TestTestLoader(unittest.TestCase):

    def test_count_test_case(self):
        tests = TestLoader().find_tests('stub_test.TestSimpleFlow')
        self.assertEqual(len(tests), 8)

    def test_count_test_method(self):
        tests = TestLoader().find_tests('stub_test.TestFoo.test_foo')
        self.assertEqual(len(tests), 1)


class TestTestRunner(unittest.TestCase):

    def test_run_test_case(self):
        tests = TestLoader().find_tests('stub_test.TestSimpleFlow.test_simple_if_true')

        runner = TraceRunner()
        runner.run(tests)
        result = runner.trace_result

        self.assertEqual(len(result.global_traces), 1)

    def test_run_test_suite(self):
        tests = TestLoader().find_tests('stub_test.TestSimpleFlow')

        runner = TraceRunner()
        runner.run(tests)
        result = runner.trace_result

        self.assertEqual(len(result.global_traces), 8)

    def test_run_test_case_shortcut(self):
        result = TraceRunner.trace('stub_test.TestSimpleFlow.test_simple_if_true')
        self.assertEqual(len(result.global_traces), 1)

    def test_run_test_suite_shortcut(self):
        result = TraceRunner.trace('stub_test.TestSimpleFlow')
        self.assertEqual(len(result.global_traces), 8)


class TestSUTLoader(unittest.TestCase):

    def test_find_module(self):
        target_sut = 'stub_sut'
        sut = SUTLoader.find_sut(target_sut)

        self.assertEqual(sut.full_name(), target_sut)
        # self.assertEqual(len(sut.suts), 19)
        # self.assertEqual(len(sut.executable_lines()), 21)

    def test_find_class(self):
        target_sut = 'stub_sut.SimpleFlow'
        sut = SUTLoader.find_sut(target_sut)

        self.assertEqual(sut.full_name(), target_sut)
        # self.assertEqual(sut.loc(), 27)
        # self.assertEqual(len(sut.executable_lines()), 21)

    def test_find_method(self):
        target_sut = 'stub_sut.SimpleFlow.simple_if'
        sut = SUTLoader.find_sut(target_sut)

        self.assertEqual(sut.full_name(), target_sut)
        self.assertEqual(sut.loc(), 2)
        self.assertEqual(len(sut.executable_lines()), 2)

        target_sut = 'stub_sut.SimpleFlow.simple_if_else'
        sut = SUTLoader.find_sut(target_sut)

        self.assertEqual(sut.full_name(), target_sut)
        self.assertEqual(sut.loc(), 4)
        self.assertEqual(len(sut.executable_lines()), 3)

        target_sut = 'stub_sut.SimpleFlow.loop'
        sut = SUTLoader.find_sut(target_sut)

        self.assertEqual(sut.full_name(), target_sut)
        self.assertEqual(sut.loc(), 3)
        self.assertEqual(len(sut.executable_lines()), 3)

        target_sut = 'stub_sut.SimpleFlow.try_success'
        sut = SUTLoader.find_sut(target_sut)

        self.assertEqual(sut.full_name(), target_sut)
        self.assertEqual(sut.loc(), 4)
        self.assertEqual(len(sut.executable_lines()), 4)

    def test_find_function(self):
        target_sut = 'stub_sut.function_with_3_lines'
        sut = SUTLoader.find_sut(target_sut)

        self.assertEqual(sut.full_name(), target_sut)
        self.assertEqual(sut.loc(), 3)
        self.assertEqual(len(sut.executable_lines()), 3)


class TestSUT(unittest.TestCase):

    def test_module_full_name(self):
        c = SUTModule('m')
        self.assertEqual(c.full_name(), 'm')
        self.assertEqual(str(c), 'm')

    def test_class_full_name(self):
        c = SUTClass('m', 'c')
        self.assertEqual(c.full_name(), 'm.c')
        self.assertEqual(str(c), 'm.c')

    def test_function_full_name(self):
        f = SUTFunction('m', 'f')
        self.assertEqual(f.full_name(), 'm.f')
        self.assertEqual(str(f), 'm.f')

    def test_method_full_name(self):
        c = SUTClass('m', 'c')
        foo = SUTMethod('m', 'c', 'foo')

        self.assertEqual(c.full_name(), 'm.c')
        self.assertEqual(foo.full_name(), 'm.c.foo')

    def test_add_sut(self):
        module = SUTModule('m')
        c = SUTClass('m', 'c')
        m1 = SUTMethod('m', 'c', 'm1')
        m2 = SUTMethod('m', 'c', 'm2')
        f = SUTMethod('m', 'c', 'f')

        module.add_sut(m1)
        module.add_sut(m2)
        module.add_sut(f)
        c.add_sut(m1)
        c.add_sut(m2)

        self.assertEqual(len(module.suts), 3)
        self.assertEqual(len(c.suts), 2)
        self.assertEqual(module.full_name(), 'm')
        self.assertEqual(c.full_name(), 'm.c')
        self.assertEqual(m1.full_name(), 'm.c.m1')
        self.assertEqual(m2.full_name(), 'm.c.m2')

    def test_loc(self):
        sut = SUTSourceEntity('', '')
        sut.start_line = 10
        sut.end_line = 20

        self.assertEqual(sut.loc(), 10)