import unittest
from happyflow.loader import SUTLoader
from happyflow.runner import TestRunner
from happyflow import sut_tracer


class TestState(unittest.TestCase):

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
        a = state_result.vars['a'].states
        self.assertEqual(a[0].value, 1)
        self.assertEqual(a[1].value, 2)
        self.assertEqual(a[2].value, 3)

        seq_values = state_result.vars['a'].distinct_sequential_values()
        self.assertEqual(seq_values, [1, 2, 3])

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
        a = state_result.vars['a'].states
        self.assertEqual(a[0].value, 0)
        self.assertEqual(a[1].value, 1)
        self.assertEqual(a[2].value, 2)
        self.assertEqual(a[3].value, 3)

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
        a = state_result.vars['a'].states
        self.assertEqual(a[0].value, 1)
        self.assertEqual(a[-1].value, 100)

        first, last = state_result.vars['a'].first_last()
        self.assertEqual(first.value, 1)
        self.assertEqual(last.value, 100)

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
        a = state_result.vars['a'].states
        self.assertEqual(a[0].value, 1)
        self.assertEqual(a[-1].value, 200)

        first, last = state_result.vars['a'].first_last()
        self.assertEqual(first.value, 1)
        self.assertEqual(last.value, 200)

    def test_change_multiple_vars_states(self):
        sut_tracer.COLLECT_STATE = True
        sut_tracer.SUT_NAME = 'stub_sut.StubState.change_multiple_vars_states'

        trace_result = TestRunner.trace('stub_test.TestStubState.test_change_multiple_vars_states')
        sut = SUTLoader.find_sut(sut_tracer.SUT_NAME)

        flow_result = sut.base_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [76, 77, 79, 80])
        self.assertEqual(flow_result.sut_name, 'change_multiple_vars_states')
        self.assertIn('test_change_multiple_vars_states', flow_result.test_names)

        state_result = flow_result.flows[0].state_result

        first, last = state_result.vars['a'].first_last()
        self.assertEqual(first.value, 1)
        self.assertEqual(last.value, 2)

        first, last = state_result.vars['b'].first_last()
        self.assertEqual(first.value, 10)
        self.assertEqual(last.value, 110)

    def test_change_list_state(self):
        sut_tracer.COLLECT_STATE = True
        sut_tracer.SUT_NAME = 'stub_sut.StubState.change_list_state'

        trace_result = TestRunner.trace('stub_test.TestStubState.test_change_list_state')
        sut = SUTLoader.find_sut(sut_tracer.SUT_NAME)

        flow_result = sut.base_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [83, 84, 85, 86, 87, 88, 89])
        self.assertEqual(flow_result.sut_name, 'change_list_state')
        self.assertIn('test_change_list_state', flow_result.test_names)

        state_result = flow_result.flows[0].state_result
        a_list = state_result.vars['a'].states
        self.assertEqual(a_list[0].value, [])
        self.assertEqual(a_list[1].value, [1])
        self.assertEqual(a_list[2].value, [1, 2])
        self.assertEqual(a_list[3].value, [1, 2, 3])
        self.assertEqual(a_list[4].value, [1, 2])
        self.assertEqual(a_list[5].value, [1])
        self.assertEqual(a_list[6].value, [])

    def test_change_var_state_with_loop(self):
        sut_tracer.COLLECT_STATE = True
        sut_tracer.SUT_NAME = 'stub_sut.StubState.change_var_state_with_loop'

        trace_result = TestRunner.trace('stub_test.TestStubState.test_change_var_state_with_loop')
        sut = SUTLoader.find_sut(sut_tracer.SUT_NAME)

        flow_result = sut.base_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [92, 93, 94, 93, 94, 93, 94, 93, 94, 93])
        self.assertEqual(flow_result.flows[0].distinct_lines(), [92, 93, 94])
        self.assertEqual(flow_result.sut_name, 'change_var_state_with_loop')
        self.assertIn('test_change_var_state_with_loop', flow_result.test_names)

        state_result = flow_result.flows[0].state_result
        a = state_result.vars['a'].states
        self.assertEqual(len(a), 10)

        self.assertEqual(a[0].value, 0)
        self.assertEqual(a[1].value, 0)

        self.assertEqual(a[2].value, 1)
        self.assertEqual(a[3].value, 1)

        self.assertEqual(a[4].value, 2)
        self.assertEqual(a[5].value, 2)

        self.assertEqual(a[6].value, 3)
        self.assertEqual(a[7].value, 3)

        self.assertEqual(a[8].value, 4)
        self.assertEqual(a[9].value, 4)

    def test_change_instance_var(self):
        sut_tracer.COLLECT_STATE = True
        sut_tracer.SUT_NAME = 'stub_sut.StubState.change_instance_var'

        trace_result = TestRunner.trace('stub_test.TestStubState.test_change_instance_var')
        sut = SUTLoader.find_sut(sut_tracer.SUT_NAME)

        flow_result = sut.base_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [100, 101])
        self.assertEqual(flow_result.sut_name, 'change_instance_var')
        self.assertIn('test_change_instance_var', flow_result.test_names)

        state_result = flow_result.flows[0].state_result
        obj = state_result.vars['self'].states
        self.assertEqual(len(obj), 3)

        self.assertEqual(obj[0].line, 100)
        self.assertEqual(obj[0].value.inst_var, 'default')

        self.assertEqual(obj[1].line, 101)
        self.assertEqual(obj[1].value.inst_var, 'foo')

        self.assertEqual(obj[2].line, 101)
        self.assertEqual(obj[2].value.inst_var, 'new foo')

    def test_init_with_instance_var(self):
        sut_tracer.COLLECT_STATE = True
        sut_tracer.SUT_NAME = 'stub_sut.StubState.__init__'

        trace_result = TestRunner.trace('stub_test.TestStubState.test_init')
        sut = SUTLoader.find_sut(sut_tracer.SUT_NAME)

        flow_result = sut.base_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [97])
        self.assertEqual(flow_result.sut_name, '__init__')
        self.assertIn('test_init', flow_result.test_names)

        state_result = flow_result.flows[0].state_result
        obj = state_result.vars['self'].states
        self.assertEqual(len(obj), 2)

        self.assertEqual(obj[0].line, 97)
        self.assertNotIn('inst_var', dir(obj[0].value))

        self.assertEqual(obj[1].line, 97)
        self.assertEqual(obj[1].value.inst_var, 'default')
