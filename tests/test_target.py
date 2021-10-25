import unittest
from happyflow.target_model import TargetEntity, TargetFunction, TargetMethod, TargetClass, TargetModule
from happyflow.target_loader import TargetEntityLoader
from happyflow.test_loader import UnittestLoader
from happyflow.tracer import TraceRunner


class TestTestLoader(unittest.TestCase):

    def test_count_test_case(self):
        tests = UnittestLoader().loadTestsFromName('tests.stub_test.TestSimpleFlow')
        self.assertEqual(len(tests), 8)

    def test_count_test_method(self):
        tests = UnittestLoader().loadTestsFromName('tests.stub_test.TestFoo.test_foo')
        self.assertEqual(len(tests), 1)


class TestTestRunner(unittest.TestCase):

    def test_run_test_case_shortcut(self):
        result = TraceRunner.trace_from_tests('tests.stub_test.TestSimpleFlow.test_simple_if_true')
        self.assertEqual(len(result.global_traces), 1)

    def test_run_test_suite_shortcut(self):
        result = TraceRunner.trace_from_tests('tests.stub_test.TestSimpleFlow')
        self.assertEqual(len(result.global_traces), 8)

    def test_run_test_case(self):
        runner = TraceRunner()
        runner.get_source_entity_name_wrapper = UnittestLoader.get_test_name
        runner.run_source_entity_wrapper = UnittestLoader.run_test

        tests = UnittestLoader().loadTestsFromName('tests.stub_test.TestSimpleFlow.test_simple_if_true')
        runner.run(tests)
        result = runner.trace_result

        self.assertEqual(len(result.global_traces), 1)

    def test_run_test_suite(self):
        runner = TraceRunner()
        runner.get_source_entity_name_wrapper = UnittestLoader.get_test_name
        runner.run_source_entity_wrapper = UnittestLoader.run_test

        tests = UnittestLoader().loadTestsFromName('tests.stub_test.TestSimpleFlow')
        runner.run(tests)
        result = runner.trace_result

        self.assertEqual(len(result.global_traces), 8)


class TestSUTLoader(unittest.TestCase):

    def test_find_module(self):
        target_sut = 'stub_sut'
        sut = TargetEntityLoader.find(target_sut, '.', 'stub_sut')

        self.assertEqual(sut.full_name(), target_sut)
        # self.assertEqual(len(sut.suts), 19)
        # self.assertEqual(len(sut.executable_lines()), 21)

    def test_find_class(self):
        target_sut = 'stub_sut.SimpleFlow'
        sut = TargetEntityLoader.find(target_sut, '.', 'stub_sut')

        self.assertEqual(sut.full_name(), target_sut)
        # self.assertEqual(sut.loc(), 27)
        # self.assertEqual(len(sut.executable_lines()), 21)

    def test_find_method(self):
        target_sut = 'stub_sut.SimpleFlow.simple_if'
        sut = TargetEntityLoader.find(target_sut, '.', 'stub_sut')

        self.assertEqual(sut.full_name(), target_sut)
        self.assertEqual(sut.loc(), 2)
        self.assertEqual(len(sut.executable_lines()), 2)

        target_sut = 'stub_sut.SimpleFlow.simple_if_else'
        sut = TargetEntityLoader.find(target_sut, '.', 'stub_sut')

        self.assertEqual(sut.full_name(), target_sut)
        self.assertEqual(sut.loc(), 4)
        self.assertEqual(len(sut.executable_lines()), 3)

        target_sut = 'stub_sut.SimpleFlow.loop'
        sut = TargetEntityLoader.find(target_sut, '.', 'stub_sut')

        self.assertEqual(sut.full_name(), target_sut)
        self.assertEqual(sut.loc(), 3)
        self.assertEqual(len(sut.executable_lines()), 3)

        target_sut = 'stub_sut.SimpleFlow.try_success'
        sut = TargetEntityLoader.find(target_sut, '.', 'stub_sut')

        self.assertEqual(sut.full_name(), target_sut)
        self.assertEqual(sut.loc(), 4)
        self.assertEqual(len(sut.executable_lines()), 4)

    def test_find_function(self):
        target_sut = 'stub_sut.function_with_3_lines'
        sut = TargetEntityLoader.find(target_sut, '.', 'stub_sut')

        self.assertEqual(sut.full_name(), target_sut)
        self.assertEqual(sut.loc(), 3)
        self.assertEqual(len(sut.executable_lines()), 3)


class TestSUT(unittest.TestCase):

    def test_module_full_name(self):
        c = TargetModule('m')
        self.assertEqual(c.full_name(), 'm')
        self.assertEqual(str(c), 'm')

    def test_class_full_name(self):
        c = TargetClass('m', 'c')
        self.assertEqual(c.full_name(), 'm.c')
        self.assertEqual(str(c), 'm.c')

    def test_function_full_name(self):
        f = TargetFunction('m', 'f')
        self.assertEqual(f.full_name(), 'm.f')
        self.assertEqual(str(f), 'm.f')

    def test_method_full_name(self):
        c = TargetClass('m', 'c')
        foo = TargetMethod('m', 'c', 'foo')

        self.assertEqual(c.full_name(), 'm.c')
        self.assertEqual(foo.full_name(), 'm.c.foo')

    def test_add_sut(self):
        module = TargetModule('m')
        c = TargetClass('m', 'c')
        m1 = TargetMethod('m', 'c', 'm1')
        m2 = TargetMethod('m', 'c', 'm2')
        f = TargetMethod('m', 'c', 'f')

        module.add_entity(m1)
        module.add_entity(m2)
        module.add_entity(f)
        c.add_entity(m1)
        c.add_entity(m2)

        self.assertEqual(len(module.target_entities), 3)
        self.assertEqual(len(c.target_entities), 2)
        self.assertEqual(module.full_name(), 'm')
        self.assertEqual(c.full_name(), 'm.c')
        self.assertEqual(m1.full_name(), 'm.c.m1')
        self.assertEqual(m2.full_name(), 'm.c.m2')

    def test_loc(self):
        sut = TargetEntity('.', '.')
        sut.start_line = 10
        sut.end_line = 20

        self.assertEqual(sut.loc(), 10)


if __name__ == '__main__':
    unittest.main()