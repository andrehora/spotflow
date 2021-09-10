import unittest
from happyflow.sut_model import SUTSourced, SUTFunction, SUTMethod, SUTClass
from happyflow.loader import SUTLoader, TestLoader
from happyflow.runner import TestRunner


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

        runner = TestRunner()
        runner.run(tests)
        result = runner.result

        self.assertEqual(len(result.traces), 1)

    def test_run_test_suite(self):
        tests = TestLoader().find_tests('stub_test.TestSimpleFlow')

        runner = TestRunner()
        runner.run(tests)
        result = runner.result

        self.assertEqual(len(result.traces), 8)

    def test_run_test_case_shortcut(self):
        result = TestRunner.trace('stub_test.TestSimpleFlow.test_simple_if_true')
        self.assertEqual(len(result.traces), 1)

    def test_run_test_suite_shortcut(self):
        result = TestRunner.trace('stub_test.TestSimpleFlow')
        self.assertEqual(len(result.traces), 8)


class TestSUTLoader(unittest.TestCase):

    def test_find_class(self):
        target_sut = 'stub_sut.SimpleFlow'
        sut = SUTLoader.find_sut(target_sut)

        self.assertEqual(sut.full_name(), target_sut)
        self.assertEqual(sut.loc(), 27)
        self.assertEqual(len(sut.executable_lines()), 21)

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

    def test_function_full_name(self):
        f = SUTFunction('m', 'f')
        self.assertEqual(f.full_name(), 'm.f')
        self.assertEqual(str(f), 'm.f')

    def test_class_full_name(self):
        c = SUTClass('m', 'c')
        self.assertEqual(c.full_name(), 'm.c')
        self.assertEqual(str(c), 'm.c')

    def test_method_full_name(self):
        c = SUTClass('m', 'c')
        foo = SUTMethod('m', 'foo', c)

        self.assertEqual(c.full_name(), 'm.c')
        self.assertEqual(foo.full_name(), 'm.c.foo')

    def test_add_method(self):
        c = SUTClass('m', 'c')
        m1 = SUTMethod('m', 'm1', c)
        m2 = SUTMethod('m', 'm1', c)

        c.add_method(m1)
        c.add_method(m2)

        self.assertEqual(len(c.methods), 2)
        self.assertEqual(c.full_name(), 'm.c')
        self.assertEqual(m1.full_name(), 'm.c.m1')
        self.assertEqual(m2.full_name(), 'm.c.m1')

    def test_loc(self):
        sut = SUTSourced()
        sut.start_line = 10
        sut.end_line = 20

        self.assertEqual(sut.loc(), 10)