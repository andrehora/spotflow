import unittest
from happyflow.sut_model import SUT, SUTFunction, SUTMethod, SUTClass
from happyflow.loader import SUTLoader, TestLoader
from happyflow.runner import TestRunner
from happyflow.utils import find_python_files
from happyflow import sut_tracer


class TestTestLoader(unittest.TestCase):

    @unittest.skip
    def test_count_all_tests(self):
        tests = TestLoader().find_tests('stub_test')
        self.assertEqual(len(tests), 11)

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
        sut = SUT()
        sut.start_line = 10
        sut.end_line = 20

        self.assertEqual(sut.loc(), 10)


class TestCompositeFlows(unittest.TestCase):

    def test_run_simple_if(self):
        trace_result = TestRunner.trace('stub_test.TestSimpleFlow.test_simple_if_true')
        sut = SUTLoader.find_sut('stub_sut.SimpleFlow.simple_if')
        flow_result = sut.composite_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [4, 5])
        self.assertEqual(flow_result.sut_name, 'simple_if')
        self.assertIn('test_simple_if_true', flow_result.test_names)

        trace_result = TestRunner.trace('stub_test.TestSimpleFlow.test_simple_if_false')
        sut = SUTLoader.find_sut('stub_sut.SimpleFlow.simple_if')
        flow_result = sut.composite_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [4])
        self.assertEqual(flow_result.sut_name, 'simple_if')
        self.assertIn('test_simple_if_false', flow_result.test_names)

    def test_run_simple_if_else(self):
        trace_result = TestRunner.trace('stub_test.TestSimpleFlow.test_simple_if_else_true_and_false')
        sut = SUTLoader.find_sut('stub_sut.SimpleFlow.simple_if_else')
        flow_result = sut.composite_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [8, 9, 11])
        self.assertEqual(flow_result.sut_name, 'simple_if_else')
        self.assertIn('test_simple_if_else_true_and_false', flow_result.test_names)

        trace_result = TestRunner.trace('stub_test.TestSimpleFlow.test_simple_if_else_true')
        sut = SUTLoader.find_sut('stub_sut.SimpleFlow.simple_if_else')
        flow_result = sut.composite_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [8, 9])
        self.assertEqual(flow_result.sut_name, 'simple_if_else')
        self.assertIn('test_simple_if_else_true', flow_result.test_names)

        trace_result = TestRunner.trace('stub_test.TestSimpleFlow.test_simple_if_else_false')
        sut = SUTLoader.find_sut('stub_sut.SimpleFlow.simple_if_else')
        flow_result = sut.composite_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [8, 11])
        self.assertEqual(flow_result.sut_name, 'simple_if_else')
        self.assertIn('test_simple_if_else_false', flow_result.test_names)

        trace_result = TestRunner.trace('stub_test.TestSimpleFlow')
        sut = SUTLoader.find_sut('stub_sut.SimpleFlow.simple_if_else')
        flow_result = sut.composite_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 3)
        self.assertEqual(flow_result.sut_name, 'simple_if_else')
        self.assertIn('test_simple_if_else_true', flow_result.test_names)
        self.assertIn('test_simple_if_else_false', flow_result.test_names)
        self.assertIn('test_simple_if_else_true_and_false', flow_result.test_names)

    def test_run_loop(self):
        trace_result = TestRunner.trace('stub_test.TestSimpleFlow.test_loop')
        sut = SUTLoader.find_sut('stub_sut.SimpleFlow.loop')
        flow_result = sut.composite_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [14, 15, 16])
        self.assertEqual(flow_result.sut_name, 'loop')
        self.assertIn('test_loop', flow_result.test_names)

    def test_run_try(self):
        trace_result = TestRunner.trace('stub_test.TestSimpleFlow.test_try_success')
        sut = SUTLoader.find_sut('stub_sut.SimpleFlow.try_success')
        flow_result = sut.composite_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [19, 20])
        self.assertEqual(flow_result.sut_name, 'try_success')
        self.assertIn('test_try_success', flow_result.test_names)

    def test_run_try_fail(self):
        trace_result = TestRunner.trace('stub_test.TestSimpleFlow.test_try_fail')
        sut = SUTLoader.find_sut('stub_sut.SimpleFlow.try_fail')
        flow_result = sut.composite_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [25, 26, 27, 28])
        self.assertEqual(flow_result.sut_name, 'try_fail')
        self.assertIn('test_try_fail', flow_result.test_names)

    def test_run_all(self):
        trace_result = TestRunner.trace('stub_test.TestSimpleFlow')
        sut = SUTLoader.find_sut('stub_sut.SimpleFlow')
        flow_result = sut.composite_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 8)
        self.assertEqual(len(flow_result.flows), 8)
        self.assertEqual(flow_result.sut_name, 'SimpleFlow')
        self.assertIn('test_simple_if_true', flow_result.test_names)
        self.assertIn('test_simple_if_false', flow_result.test_names)
        self.assertIn('test_simple_if_else_true', flow_result.test_names)
        self.assertIn('test_simple_if_else_false', flow_result.test_names)
        self.assertIn('test_simple_if_else_true_and_false', flow_result.test_names)
        self.assertIn('test_loop', flow_result.test_names)
        self.assertIn('test_try_success', flow_result.test_names)
        self.assertIn('test_try_fail', flow_result.test_names)


    def test_single_call_to_sut(self):
        trace_result = TestRunner.trace('stub_test.TestComplexFlow.test_single_call_to_sut_bom_dia')
        sut = SUTLoader.find_sut('stub_sut.ComplexFlow.hello')
        flow_result = sut.composite_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [35, 39])
        self.assertEqual(flow_result.sut_name, 'hello')
        self.assertIn('test_single_call_to_sut_bom_dia', flow_result.test_names)

        trace_result = TestRunner.trace('stub_test.TestComplexFlow.test_single_call_to_sut_boa_tarde')
        sut = SUTLoader.find_sut('stub_sut.ComplexFlow.hello')
        flow_result = sut.composite_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [35, 36, 38])
        self.assertEqual(flow_result.sut_name, 'hello')
        self.assertIn('test_single_call_to_sut_boa_tarde', flow_result.test_names)

        trace_result = TestRunner.trace('stub_test.TestComplexFlow.test_single_call_to_sut_boa_noite')
        sut = SUTLoader.find_sut('stub_sut.ComplexFlow.hello')
        flow_result = sut.composite_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [35, 36, 37])
        self.assertEqual(flow_result.sut_name, 'hello')
        self.assertIn('test_single_call_to_sut_boa_noite', flow_result.test_names)

    def test_multiple_call_to_sut(self):
        trace_result = TestRunner.trace('stub_test.TestComplexFlow.test_multiple_call_to_sut')
        sut = SUTLoader.find_sut('stub_sut.ComplexFlow.hello')
        flow_result = sut.composite_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [35, 36, 37, 38, 39])
        self.assertEqual(flow_result.sut_name, 'hello')
        self.assertIn('test_multiple_call_to_sut', flow_result.test_names)


class TestBaseFlows(unittest.TestCase):

    def test_run_simple_if(self):
        sut_tracer.SUT_NAME = 'stub_sut.SimpleFlow.simple_if'
        trace_result = TestRunner.trace('stub_test.TestSimpleFlow.test_simple_if_true')
        sut = SUTLoader.find_sut(sut_tracer.SUT_NAME)
        flow_result = sut.atomic_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [4, 5])
        self.assertEqual(flow_result.sut_name, 'simple_if')
        self.assertIn('test_simple_if_true', flow_result.test_names)

        trace_result = TestRunner.trace('stub_test.TestSimpleFlow.test_simple_if_false')
        sut = SUTLoader.find_sut(sut_tracer.SUT_NAME)
        flow_result = sut.atomic_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [4])
        self.assertEqual(flow_result.sut_name, 'simple_if')
        self.assertIn('test_simple_if_false', flow_result.test_names)

    def test_run_simple_if_else(self):
        sut_tracer.SUT_NAME = 'stub_sut.SimpleFlow.simple_if_else'
        trace_result = TestRunner.trace('stub_test.TestSimpleFlow.test_simple_if_else_true_and_false')
        sut = SUTLoader.find_sut(sut_tracer.SUT_NAME)
        flow_result = sut.atomic_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 2)
        self.assertIn([8, 9], flow_result.flows)
        self.assertIn([8, 11], flow_result.flows)
        self.assertEqual(flow_result.sut_name, 'simple_if_else')
        self.assertIn('test_simple_if_else_true_and_false', flow_result.test_names)

        trace_result = TestRunner.trace('stub_test.TestSimpleFlow.test_simple_if_else_true')
        sut = SUTLoader.find_sut(sut_tracer.SUT_NAME)
        flow_result = sut.atomic_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [8, 9])
        self.assertEqual(flow_result.sut_name, 'simple_if_else')
        self.assertIn('test_simple_if_else_true', flow_result.test_names)

        trace_result = TestRunner.trace('stub_test.TestSimpleFlow.test_simple_if_else_false')
        sut = SUTLoader.find_sut(sut_tracer.SUT_NAME)
        flow_result = sut.atomic_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [8, 11])
        self.assertEqual(flow_result.sut_name, 'simple_if_else')
        self.assertIn('test_simple_if_else_false', flow_result.test_names)

        trace_result = TestRunner.trace('stub_test.TestSimpleFlow')
        sut = SUTLoader.find_sut(sut_tracer.SUT_NAME)
        flow_result = sut.atomic_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 4)
        self.assertIn([8, 9], flow_result.flows)
        self.assertIn([8, 11], flow_result.flows)
        self.assertEqual(flow_result.sut_name, 'simple_if_else')
        self.assertIn('test_simple_if_else_true', flow_result.test_names)
        self.assertIn('test_simple_if_else_false', flow_result.test_names)
        self.assertIn('test_simple_if_else_true_and_false', flow_result.test_names)

    def test_run_loop(self):
        sut_tracer.SUT_NAME = 'stub_sut.SimpleFlow.loop'
        trace_result = TestRunner.trace('stub_test.TestSimpleFlow.test_loop')
        sut = SUTLoader.find_sut(sut_tracer.SUT_NAME)
        flow_result = sut.atomic_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [14, 15, 16, 15, 16, 15])
        self.assertEqual(flow_result.flows[0].distinct_lines(), [14, 15, 16])
        self.assertEqual(flow_result.sut_name, 'loop')
        self.assertIn('test_loop', flow_result.test_names)

    def test_run_try(self):
        sut_tracer.SUT_NAME = 'stub_sut.SimpleFlow.try_success'
        trace_result = TestRunner.trace('stub_test.TestSimpleFlow.test_try_success')
        sut = SUTLoader.find_sut(sut_tracer.SUT_NAME)
        flow_result = sut.atomic_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [19, 20])
        self.assertEqual(flow_result.sut_name, 'try_success')
        self.assertIn('test_try_success', flow_result.test_names)

    def test_run_try_fail(self):
        sut_tracer.SUT_NAME = 'stub_sut.SimpleFlow.try_fail'
        trace_result = TestRunner.trace('stub_test.TestSimpleFlow.test_try_fail')
        sut = SUTLoader.find_sut(sut_tracer.SUT_NAME)
        flow_result = sut.atomic_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [25, 26, 27, 28])
        self.assertEqual(flow_result.sut_name, 'try_fail')
        self.assertIn('test_try_fail', flow_result.test_names)

    def test_run_all(self):
        trace_result = TestRunner.trace('stub_test.TestSimpleFlow')
        sut = SUTLoader.find_sut('stub_sut.SimpleFlow')
        flow_result = sut.atomic_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 10)
        self.assertEqual(len(flow_result.flows), 10)
        self.assertEqual(flow_result.sut_name, 'SimpleFlow')
        self.assertIn('test_simple_if_true', flow_result.test_names)
        self.assertIn('test_simple_if_false', flow_result.test_names)
        self.assertIn('test_simple_if_else_true', flow_result.test_names)
        self.assertIn('test_simple_if_else_false', flow_result.test_names)
        self.assertIn('test_simple_if_else_true_and_false', flow_result.test_names)
        self.assertIn('test_loop', flow_result.test_names)
        self.assertIn('test_try_success', flow_result.test_names)
        self.assertIn('test_try_fail', flow_result.test_names)

    def test_single_call_to_sut(self):
        sut_tracer.SUT_NAME = 'stub_sut.ComplexFlow.hello'
        trace_result = TestRunner.trace('stub_test.TestComplexFlow.test_single_call_to_sut_bom_dia')
        sut = SUTLoader.find_sut(sut_tracer.SUT_NAME)
        flow_result = sut.atomic_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [35, 39])
        self.assertEqual(flow_result.sut_name, 'hello')
        self.assertIn('test_single_call_to_sut_bom_dia', flow_result.test_names)

        trace_result = TestRunner.trace('stub_test.TestComplexFlow.test_single_call_to_sut_boa_tarde')
        sut = SUTLoader.find_sut(sut_tracer.SUT_NAME)
        flow_result = sut.atomic_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [35, 36, 38])
        self.assertEqual(flow_result.sut_name, 'hello')
        self.assertIn('test_single_call_to_sut_boa_tarde', flow_result.test_names)

        trace_result = TestRunner.trace('stub_test.TestComplexFlow.test_single_call_to_sut_boa_noite')
        sut = SUTLoader.find_sut(sut_tracer.SUT_NAME)
        flow_result = sut.atomic_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [35, 36, 37])
        self.assertEqual(flow_result.sut_name, 'hello')
        self.assertIn('test_single_call_to_sut_boa_noite', flow_result.test_names)

    def test_multiple_call_to_sut(self):
        sut_tracer.SUT_NAME = 'stub_sut.ComplexFlow.hello'
        trace_result = TestRunner.trace('stub_test.TestComplexFlow.test_multiple_call_to_sut')
        sut = SUTLoader.find_sut(sut_tracer.SUT_NAME)
        flow_result = sut.atomic_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 3)
        self.assertIn([35, 39], flow_result.flows)
        self.assertIn([35, 36, 38], flow_result.flows)
        self.assertIn([35, 36, 37], flow_result.flows)
        self.assertEqual(flow_result.sut_name, 'hello')
        self.assertIn('test_multiple_call_to_sut', flow_result.test_names)

    def test_sut_call_sut(self):
        sut_tracer.SUT_NAME = 'stub_sut'
        trace_result = TestRunner.trace('stub_test.TestComplexFlow.test_sut_call_sut')
        sut = SUTLoader.find_sut('stub_sut.ComplexFlow.func')
        flow_result = sut.atomic_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [42, 43, 44])
        self.assertEqual(flow_result.sut_name, 'func')
        self.assertIn('test_sut_call_sut', flow_result.test_names)

        sut = SUTLoader.find_sut('stub_sut.ComplexFlow.f1')
        flow_result = sut.atomic_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [47])
        self.assertEqual(flow_result.sut_name, 'f1')
        self.assertIn('test_sut_call_sut', flow_result.test_names)

        sut = SUTLoader.find_sut('stub_sut.ComplexFlow.f2')
        flow_result = sut.atomic_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [50])
        self.assertEqual(flow_result.sut_name, 'f2')
        self.assertIn('test_sut_call_sut', flow_result.test_names)

        sut = SUTLoader.find_sut('stub_sut.ComplexFlow.f3')
        flow_result = sut.atomic_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [53])
        self.assertEqual(flow_result.sut_name, 'f3')
        self.assertIn('test_sut_call_sut', flow_result.test_names)
