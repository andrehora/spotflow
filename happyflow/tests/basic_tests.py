import unittest
from happyflow.sut_model import SUT, SUTFunction, SUTMethod, SUTClass
from happyflow.loader import SUTLoader, TestLoader
from happyflow.runner import TestRunner
from happyflow.utils import find_python_files
from happyflow import sut_tracer

# @unittest.skip
class TestUtil(unittest.TestCase):

    def test_find_python_file(self):
        files = find_python_files('.')
        for filename in files:
            self.assertTrue('/' in filename)
            self.assertTrue(filename.endswith('.py'))

# @unittest.skip
class TestTestLoader(unittest.TestCase):

    @unittest.skip
    def test_count_all_tests(self):
        tests = TestLoader().find_tests('stub_test')
        self.assertEqual(len(tests), 11)

    def test_count_test_case(self):
        tests = TestLoader().find_tests('stub_test.TestStubBasicFlow')
        self.assertEqual(len(tests), 8)

    def test_count_test_method(self):
        tests = TestLoader().find_tests('stub_test.TestFoo.test_foo')
        self.assertEqual(len(tests), 1)

# @unittest.skip
class TestTestRunner(unittest.TestCase):

    def test_run_test_case(self):
        tests = TestLoader().find_tests('stub_test.TestStubBasicFlow.test_simple_if_true')

        runner = TestRunner()
        runner.run(tests)
        result = runner.result

        self.assertEqual(len(result.traces), 1)

    def test_run_test_suite(self):
        tests = TestLoader().find_tests('stub_test.TestStubBasicFlow')

        runner = TestRunner()
        runner.run(tests)
        result = runner.result

        self.assertEqual(len(result.traces), 8)

    def test_run_test_case_shortcut(self):
        result = TestRunner.trace('stub_test.TestStubBasicFlow.test_simple_if_true')
        self.assertEqual(len(result.traces), 1)

    def test_run_test_suite_shortcut(self):
        result = TestRunner.trace('stub_test.TestStubBasicFlow')
        self.assertEqual(len(result.traces), 8)


# @unittest.skip
class TestSUTLoader(unittest.TestCase):

    def test_find_class(self):
        target_sut = 'stub_sut.StubBasicFlow'
        sut = SUTLoader.find_sut(target_sut)

        self.assertEqual(sut.full_name(), target_sut)
        self.assertEqual(sut.loc(), 27)
        self.assertEqual(len(sut.executable_lines()), 21)

    def test_find_method(self):
        target_sut = 'stub_sut.StubBasicFlow.simple_if'
        sut = SUTLoader.find_sut(target_sut)
        self.assertEqual(sut.full_name(), target_sut)
        self.assertEqual(sut.loc(), 2)
        self.assertEqual(len(sut.executable_lines()), 2)

        target_sut = 'stub_sut.StubBasicFlow.simple_if_else'
        sut = SUTLoader.find_sut(target_sut)
        self.assertEqual(sut.full_name(), target_sut)
        self.assertEqual(sut.loc(), 4)
        self.assertEqual(len(sut.executable_lines()), 3)

        target_sut = 'stub_sut.StubBasicFlow.loop'
        sut = SUTLoader.find_sut(target_sut)
        self.assertEqual(sut.full_name(), target_sut)
        self.assertEqual(sut.loc(), 3)
        self.assertEqual(len(sut.executable_lines()), 3)

        target_sut = 'stub_sut.StubBasicFlow.try_success'
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


# @unittest.skip
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

    def test_intersection(self):
        sut = SUT()
        sut.start_line = 10
        sut.end_line = 20

        lines = [1, 10, 15, 20, 100]
        inter = sut.intersection(lines)

        self.assertEqual(inter, [10, 15, 20])

    def test_loc(self):
        sut = SUT()
        sut.start_line = 10
        sut.end_line = 20

        self.assertEqual(sut.loc(), 10)


# @unittest.skip
class TestCompositeFlows(unittest.TestCase):

    def test_run_simple_if(self):
        trace_result = TestRunner.trace('stub_test.TestStubBasicFlow.test_simple_if_true')
        sut = SUTLoader.find_sut('stub_sut.StubBasicFlow.simple_if')
        flow_result = sut.composite_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [4, 5])
        self.assertEqual(flow_result.sut_name, 'simple_if')
        self.assertIn('test_simple_if_true', flow_result.test_names)

        trace_result = TestRunner.trace('stub_test.TestStubBasicFlow.test_simple_if_false')
        sut = SUTLoader.find_sut('stub_sut.StubBasicFlow.simple_if')
        flow_result = sut.composite_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [4])
        self.assertEqual(flow_result.sut_name, 'simple_if')
        self.assertIn('test_simple_if_false', flow_result.test_names)

    def test_run_simple_if_else(self):
        trace_result = TestRunner.trace('stub_test.TestStubBasicFlow.test_simple_if_else_true_and_false')
        sut = SUTLoader.find_sut('stub_sut.StubBasicFlow.simple_if_else')
        flow_result = sut.composite_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [8, 9, 11])
        self.assertEqual(flow_result.sut_name, 'simple_if_else')
        self.assertIn('test_simple_if_else_true_and_false', flow_result.test_names)

        trace_result = TestRunner.trace('stub_test.TestStubBasicFlow.test_simple_if_else_true')
        sut = SUTLoader.find_sut('stub_sut.StubBasicFlow.simple_if_else')
        flow_result = sut.composite_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [8, 9])
        self.assertEqual(flow_result.sut_name, 'simple_if_else')
        self.assertIn('test_simple_if_else_true', flow_result.test_names)

        trace_result = TestRunner.trace('stub_test.TestStubBasicFlow.test_simple_if_else_false')
        sut = SUTLoader.find_sut('stub_sut.StubBasicFlow.simple_if_else')
        flow_result = sut.composite_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [8, 11])
        self.assertEqual(flow_result.sut_name, 'simple_if_else')
        self.assertIn('test_simple_if_else_false', flow_result.test_names)

        trace_result = TestRunner.trace('stub_test.TestStubBasicFlow')
        sut = SUTLoader.find_sut('stub_sut.StubBasicFlow.simple_if_else')
        flow_result = sut.composite_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 3)
        self.assertEqual(flow_result.sut_name, 'simple_if_else')
        self.assertIn('test_simple_if_else_true', flow_result.test_names)
        self.assertIn('test_simple_if_else_false', flow_result.test_names)
        self.assertIn('test_simple_if_else_true_and_false', flow_result.test_names)

    def test_run_loop(self):
        trace_result = TestRunner.trace('stub_test.TestStubBasicFlow.test_loop')
        sut = SUTLoader.find_sut('stub_sut.StubBasicFlow.loop')
        flow_result = sut.composite_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [14, 15, 16])
        self.assertEqual(flow_result.sut_name, 'loop')
        self.assertIn('test_loop', flow_result.test_names)

    def test_run_try(self):
        trace_result = TestRunner.trace('stub_test.TestStubBasicFlow.test_try_success')
        sut = SUTLoader.find_sut('stub_sut.StubBasicFlow.try_success')
        flow_result = sut.composite_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [19, 20])
        self.assertEqual(flow_result.sut_name, 'try_success')
        self.assertIn('test_try_success', flow_result.test_names)

    def test_run_try_fail(self):
        trace_result = TestRunner.trace('stub_test.TestStubBasicFlow.test_try_fail')
        sut = SUTLoader.find_sut('stub_sut.StubBasicFlow.try_fail')
        flow_result = sut.composite_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [25, 26, 27, 28])
        self.assertEqual(flow_result.sut_name, 'try_fail')
        self.assertIn('test_try_fail', flow_result.test_names)

    def test_run_all(self):
        trace_result = TestRunner.trace('stub_test.TestStubBasicFlow')
        sut = SUTLoader.find_sut('stub_sut.StubBasicFlow')
        flow_result = sut.composite_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 8)
        self.assertEqual(flow_result.sut_name, 'StubBasicFlow')
        self.assertIn('test_simple_if_true', flow_result.test_names)
        self.assertIn('test_simple_if_false', flow_result.test_names)
        self.assertIn('test_simple_if_else_true', flow_result.test_names)
        self.assertIn('test_simple_if_else_false', flow_result.test_names)
        self.assertIn('test_simple_if_else_true_and_false', flow_result.test_names)
        self.assertIn('test_loop', flow_result.test_names)
        self.assertIn('test_try_success', flow_result.test_names)
        self.assertIn('test_try_fail', flow_result.test_names)

    def test_single_call_to_sut(self):
        trace_result = TestRunner.trace('stub_test.TestStubComplexFlow.test_single_call_to_sut_bom_dia')
        sut = SUTLoader.find_sut('stub_sut.StubComplexFlow.hello')
        flow_result = sut.composite_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [35, 39])
        self.assertEqual(flow_result.sut_name, 'hello')
        self.assertIn('test_single_call_to_sut_bom_dia', flow_result.test_names)

        trace_result = TestRunner.trace('stub_test.TestStubComplexFlow.test_single_call_to_sut_boa_tarde')
        sut = SUTLoader.find_sut('stub_sut.StubComplexFlow.hello')
        flow_result = sut.composite_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [35, 36, 38])
        self.assertEqual(flow_result.sut_name, 'hello')
        self.assertIn('test_single_call_to_sut_boa_tarde', flow_result.test_names)

        trace_result = TestRunner.trace('stub_test.TestStubComplexFlow.test_single_call_to_sut_boa_noite')
        sut = SUTLoader.find_sut('stub_sut.StubComplexFlow.hello')
        flow_result = sut.composite_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [35, 36, 37])
        self.assertEqual(flow_result.sut_name, 'hello')
        self.assertIn('test_single_call_to_sut_boa_noite', flow_result.test_names)

    def test_multiple_call_to_sut(self):
        trace_result = TestRunner.trace('stub_test.TestStubComplexFlow.test_multiple_call_to_sut')
        sut = SUTLoader.find_sut('stub_sut.StubComplexFlow.hello')
        flow_result = sut.composite_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [35, 36, 37, 38, 39])
        self.assertEqual(flow_result.sut_name, 'hello')
        self.assertIn('test_multiple_call_to_sut', flow_result.test_names)


# @unittest.skip
class TestBaseFlows(unittest.TestCase):

    def test_run_simple_if(self):
        sut_tracer.SUT_NAME = 'stub_sut.StubBasicFlow.simple_if'
        trace_result = TestRunner.trace('stub_test.TestStubBasicFlow.test_simple_if_true')
        sut = SUTLoader.find_sut(sut_tracer.SUT_NAME)
        flow_result = sut.base_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [4, 5])
        self.assertEqual(flow_result.sut_name, 'simple_if')
        self.assertIn('test_simple_if_true', flow_result.test_names)

        trace_result = TestRunner.trace('stub_test.TestStubBasicFlow.test_simple_if_false')
        sut = SUTLoader.find_sut(sut_tracer.SUT_NAME)
        flow_result = sut.base_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [4])
        self.assertEqual(flow_result.sut_name, 'simple_if')
        self.assertIn('test_simple_if_false', flow_result.test_names)

    def test_run_simple_if_else(self):
        sut_tracer.SUT_NAME = 'stub_sut.StubBasicFlow.simple_if_else'
        trace_result = TestRunner.trace('stub_test.TestStubBasicFlow.test_simple_if_else_true_and_false')
        sut = SUTLoader.find_sut(sut_tracer.SUT_NAME)
        flow_result = sut.base_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 2)
        self.assertIn([8, 9], flow_result.flows)
        self.assertIn([8, 11], flow_result.flows)
        self.assertEqual(flow_result.sut_name, 'simple_if_else')
        self.assertIn('test_simple_if_else_true_and_false', flow_result.test_names)

        trace_result = TestRunner.trace('stub_test.TestStubBasicFlow.test_simple_if_else_true')
        sut = SUTLoader.find_sut(sut_tracer.SUT_NAME)
        flow_result = sut.base_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [8, 9])
        self.assertEqual(flow_result.sut_name, 'simple_if_else')
        self.assertIn('test_simple_if_else_true', flow_result.test_names)

        trace_result = TestRunner.trace('stub_test.TestStubBasicFlow.test_simple_if_else_false')
        sut = SUTLoader.find_sut(sut_tracer.SUT_NAME)
        flow_result = sut.base_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [8, 11])
        self.assertEqual(flow_result.sut_name, 'simple_if_else')
        self.assertIn('test_simple_if_else_false', flow_result.test_names)

        trace_result = TestRunner.trace('stub_test.TestStubBasicFlow')
        sut = SUTLoader.find_sut(sut_tracer.SUT_NAME)
        flow_result = sut.base_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 4)
        self.assertIn([8, 9], flow_result.flows)
        self.assertIn([8, 11], flow_result.flows)
        self.assertEqual(flow_result.sut_name, 'simple_if_else')
        self.assertIn('test_simple_if_else_true', flow_result.test_names)
        self.assertIn('test_simple_if_else_false', flow_result.test_names)
        self.assertIn('test_simple_if_else_true_and_false', flow_result.test_names)

    def test_run_loop(self):
        sut_tracer.SUT_NAME = 'stub_sut.StubBasicFlow.loop'
        trace_result = TestRunner.trace('stub_test.TestStubBasicFlow.test_loop')
        sut = SUTLoader.find_sut(sut_tracer.SUT_NAME)
        flow_result = sut.base_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [14, 15, 16, 15, 16, 15])
        self.assertEqual(flow_result.sut_name, 'loop')
        self.assertIn('test_loop', flow_result.test_names)

    def test_run_try(self):
        sut_tracer.SUT_NAME = 'stub_sut.StubBasicFlow.try_success'
        trace_result = TestRunner.trace('stub_test.TestStubBasicFlow.test_try_success')
        sut = SUTLoader.find_sut(sut_tracer.SUT_NAME)
        flow_result = sut.base_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [19, 20])
        self.assertEqual(flow_result.sut_name, 'try_success')
        self.assertIn('test_try_success', flow_result.test_names)

    def test_run_try_fail(self):
        sut_tracer.SUT_NAME = 'stub_sut.StubBasicFlow.try_fail'
        trace_result = TestRunner.trace('stub_test.TestStubBasicFlow.test_try_fail')
        sut = SUTLoader.find_sut(sut_tracer.SUT_NAME)
        flow_result = sut.base_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [25, 26, 27, 28])
        self.assertEqual(flow_result.sut_name, 'try_fail')
        self.assertIn('test_try_fail', flow_result.test_names)

    def test_single_call_to_sut(self):
        sut_tracer.SUT_NAME = 'stub_sut.StubComplexFlow.hello'
        trace_result = TestRunner.trace('stub_test.TestStubComplexFlow.test_single_call_to_sut_bom_dia')
        sut = SUTLoader.find_sut(sut_tracer.SUT_NAME)
        flow_result = sut.base_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [35, 39])
        self.assertEqual(flow_result.sut_name, 'hello')
        self.assertIn('test_single_call_to_sut_bom_dia', flow_result.test_names)

        trace_result = TestRunner.trace('stub_test.TestStubComplexFlow.test_single_call_to_sut_boa_tarde')
        sut = SUTLoader.find_sut(sut_tracer.SUT_NAME)
        flow_result = sut.base_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [35, 36, 38])
        self.assertEqual(flow_result.sut_name, 'hello')
        self.assertIn('test_single_call_to_sut_boa_tarde', flow_result.test_names)

        trace_result = TestRunner.trace('stub_test.TestStubComplexFlow.test_single_call_to_sut_boa_noite')
        sut = SUTLoader.find_sut(sut_tracer.SUT_NAME)
        flow_result = sut.base_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [35, 36, 37])
        self.assertEqual(flow_result.sut_name, 'hello')
        self.assertIn('test_single_call_to_sut_boa_noite', flow_result.test_names)

    def test_multiple_call_to_sut(self):
        sut_tracer.SUT_NAME = 'stub_sut.StubComplexFlow.hello'
        trace_result = TestRunner.trace('stub_test.TestStubComplexFlow.test_multiple_call_to_sut')
        sut = SUTLoader.find_sut(sut_tracer.SUT_NAME)
        flow_result = sut.base_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 3)
        self.assertIn([35, 39], flow_result.flows)
        self.assertIn([35, 36, 38], flow_result.flows)
        self.assertIn([35, 36, 37], flow_result.flows)
        self.assertEqual(flow_result.sut_name, 'hello')
        self.assertIn('test_multiple_call_to_sut', flow_result.test_names)

    def test_sut_call_sut(self):
        sut_tracer.SUT_NAME = 'stub_sut'
        trace_result = TestRunner.trace('stub_test.TestStubComplexFlow.test_sut_call_sut')
        sut = SUTLoader.find_sut('stub_sut.StubComplexFlow.func')
        flow_result = sut.base_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [42, 43, 44])
        self.assertEqual(flow_result.sut_name, 'func')
        self.assertIn('test_sut_call_sut', flow_result.test_names)

        sut = SUTLoader.find_sut('stub_sut.StubComplexFlow.f1')
        flow_result = sut.base_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [47])
        self.assertEqual(flow_result.sut_name, 'f1')
        self.assertIn('test_sut_call_sut', flow_result.test_names)

        sut = SUTLoader.find_sut('stub_sut.StubComplexFlow.f2')
        flow_result = sut.base_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [50])
        self.assertEqual(flow_result.sut_name, 'f2')
        self.assertIn('test_sut_call_sut', flow_result.test_names)

        sut = SUTLoader.find_sut('stub_sut.StubComplexFlow.f3')
        flow_result = sut.base_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [53])
        self.assertEqual(flow_result.sut_name, 'f3')
        self.assertIn('test_sut_call_sut', flow_result.test_names)


# @unittest.skip
class TestStubState(unittest.TestCase):

    def test_change_var_state(self):
        sut_tracer.COLLECT_STATE = True
        sut_tracer.SUT_NAME = 'stub_sut.StubState.change_var_state'

        trace_result = TestRunner.trace('stub_test.TestStubState.test_change_var_state')
        sut = SUTLoader.find_sut(sut_tracer.SUT_NAME)

        flow_result = sut.base_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [59, 60, 61])
        self.assertEqual(flow_result.sut_name, 'change_var_state')
        self.assertIn('test_change_var_state', flow_result.test_names)

        state_result = flow_result.flows[0].state_result
        states = state_result.vars['a'].states
        self.assertEqual(states[0].value, 1)
        self.assertEqual(states[1].value, 2)
        self.assertEqual(states[2].value, 3)

    def test_change_arg_state(self):
        sut_tracer.COLLECT_STATE = True
        sut_tracer.SUT_NAME = 'stub_sut.StubState.change_arg_state'

        trace_result = TestRunner.trace('stub_test.TestStubState.test_change_arg_state')
        sut = SUTLoader.find_sut(sut_tracer.SUT_NAME)

        flow_result = sut.base_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [64, 65, 66])
        self.assertEqual(flow_result.sut_name, 'change_arg_state')
        self.assertIn('test_change_arg_state', flow_result.test_names)

        state_result = flow_result.flows[0].state_result
        states = state_result.vars['a'].states
        self.assertEqual(states[0].value, 0)
        self.assertEqual(states[1].value, 1)
        self.assertEqual(states[2].value, 2)
        self.assertEqual(states[3].value, 3)

    def test_change_var_state_with_conditional_true(self):
        sut_tracer.COLLECT_STATE = True
        sut_tracer.SUT_NAME = 'stub_sut.StubState.change_var_state_with_conditional'

        trace_result = TestRunner.trace('stub_test.TestStubState.test_change_var_state_with_conditional_true')
        sut = SUTLoader.find_sut(sut_tracer.SUT_NAME)

        flow_result = sut.base_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [69, 70, 71])
        self.assertEqual(flow_result.sut_name, 'change_var_state_with_conditional')
        self.assertIn('test_change_var_state_with_conditional_true', flow_result.test_names)

        state_result = flow_result.flows[0].state_result
        states = state_result.vars['a'].states
        self.assertEqual(states[0].value, 1)
        self.assertEqual(states[-1].value, 100)

    def test_change_var_state_with_conditional_false(self):
        sut_tracer.COLLECT_STATE = True
        sut_tracer.SUT_NAME = 'stub_sut.StubState.change_var_state_with_conditional'

        trace_result = TestRunner.trace('stub_test.TestStubState.test_change_var_state_with_conditional_false')
        sut = SUTLoader.find_sut(sut_tracer.SUT_NAME)

        flow_result = sut.base_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [69, 70, 73])
        self.assertEqual(flow_result.sut_name, 'change_var_state_with_conditional')
        self.assertIn('test_change_var_state_with_conditional_false', flow_result.test_names)

        state_result = flow_result.flows[0].state_result
        states = state_result.vars['a'].states
        self.assertEqual(states[0].value, 1)
        self.assertEqual(states[-1].value, 200)

