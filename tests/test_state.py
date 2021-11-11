import unittest
from happyflow.tracer import TraceRunner


class TestChangeState(unittest.TestCase):

    def test_change_var_state(self):
        target_entity_name = 'tests.stub_sut.ChangeState.change_var_state'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestChangeState.test_change_var_state', [target_entity_name])

        self.assertEqual(trace_result[target_entity_name].flows[0].run_lines, [59, 60, 61])
        self.assertEqual(trace_result[target_entity_name].target_entity_name, 'change_var_state')

        state_result = trace_result[target_entity_name].flows[0].state_result
        a = state_result.vars['a'].states
        self.assertEqual(a[0].value, '1')
        self.assertEqual(a[1].value, '2')
        self.assertEqual(a[2].value, '3')

        self.assertTrue(a[0].value_has_changed)
        self.assertTrue(a[1].value_has_changed)
        self.assertTrue(a[2].value_has_changed)

        # seq_values = state_result.vars['a'].distinct_sequential_values()
        # self.assertEqual(seq_values, "['1', '2', '3']")

    def test_change_arg_state(self):
        target_entity_name = 'tests.stub_sut.ChangeState.change_arg_state'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestChangeState.test_change_arg_state', [target_entity_name])

        self.assertEqual(trace_result[target_entity_name].flows[0].run_lines, [64, 65, 66])
        self.assertEqual(trace_result[target_entity_name].target_entity_name, 'change_arg_state')

        state_result = trace_result[target_entity_name].flows[0].state_result
        a = state_result.vars['a'].states
        self.assertEqual(a[0].value, '0')
        self.assertEqual(a[1].value, '1')
        self.assertEqual(a[2].value, '2')
        self.assertEqual(a[3].value, '3')

    def test_change_var_state_with_conditional_true(self):
        target_entity_name = 'tests.stub_sut.ChangeState.change_var_state_with_conditional'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestChangeState.test_change_var_state_with_conditional_true', [target_entity_name])

        self.assertEqual(trace_result[target_entity_name].flows[0].run_lines, [69, 70, 71])
        self.assertEqual(trace_result[target_entity_name].target_entity_name, 'change_var_state_with_conditional')

        state_result = trace_result[target_entity_name].flows[0].state_result
        a = state_result.vars['a'].states
        self.assertEqual(a[0].value, '1')
        self.assertEqual(a[-1].value, '100')

        first, last = state_result.vars['a'].first_last()
        self.assertEqual(first.value, '1')
        self.assertEqual(last.value, '100')

    def test_change_var_state_with_conditional_false(self):
        target_entity_name = 'tests.stub_sut.ChangeState.change_var_state_with_conditional'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestChangeState.test_change_var_state_with_conditional_false', [target_entity_name])

        self.assertEqual(trace_result[target_entity_name].flows[0].run_lines, [69, 70, 73])
        self.assertEqual(trace_result[target_entity_name].target_entity_name, 'change_var_state_with_conditional')

        state_result = trace_result[target_entity_name].flows[0].state_result
        a = state_result.vars['a'].states
        self.assertEqual(a[0].value, '1')
        self.assertEqual(a[-1].value, '200')

        first, last = state_result.vars['a'].first_last()
        self.assertEqual(first.value, '1')
        self.assertEqual(last.value, '200')

    def test_change_multiple_vars_states(self):
        target_entity_name = 'tests.stub_sut.ChangeState.change_multiple_vars_states'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestChangeState.test_change_multiple_vars_states', [target_entity_name])

        self.assertEqual(trace_result[target_entity_name].flows[0].run_lines, [76, 77, 79, 80])
        self.assertEqual(trace_result[target_entity_name].target_entity_name, 'change_multiple_vars_states')

        state_result = trace_result[target_entity_name].flows[0].state_result

        first, last = state_result.vars['a'].first_last()
        self.assertEqual(first.value, '1')
        self.assertEqual(last.value, '2')

        first, last = state_result.vars['b'].first_last()
        self.assertEqual(first.value, '10')
        self.assertEqual(last.value, '110')

    def test_change_list_state(self):
        target_entity_name = 'tests.stub_sut.ChangeState.change_list_state'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestChangeState.test_change_list_state', [target_entity_name])

        self.assertEqual(trace_result[target_entity_name].flows[0].run_lines, [83, 84, 85, 86, 87, 88, 89])
        self.assertEqual(trace_result[target_entity_name].target_entity_name, 'change_list_state')

        state_result = trace_result[target_entity_name].flows[0].state_result
        a_list = state_result.vars['a'].states
        self.assertEqual(a_list[0].value, '[]')
        self.assertEqual(a_list[1].value, '[1]')
        self.assertEqual(a_list[2].value, '[1, 2]')
        self.assertEqual(a_list[3].value, '[1, 2, 3]')
        self.assertEqual(a_list[4].value, '[1, 2]')
        self.assertEqual(a_list[5].value, '[1]')
        self.assertEqual(a_list[6].value, '[]')

    def test_change_var_state_with_loop(self):
        target_entity_name = 'tests.stub_sut.ChangeState.change_var_state_with_loop'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestChangeState.test_change_var_state_with_loop', [target_entity_name])

        self.assertEqual(trace_result[target_entity_name].flows[0].run_lines, [92, 93, 94, 93, 94, 93, 94, 93, 94, 93])
        self.assertEqual(trace_result[target_entity_name].flows[0].distinct_lines(), [92, 93, 94])
        self.assertEqual(trace_result[target_entity_name].target_entity_name, 'change_var_state_with_loop')

        state_result = trace_result[target_entity_name].flows[0].state_result
        a = state_result.vars['a'].states
        self.assertEqual(len(a), 10)

        self.assertEqual(a[0].value, '0')
        self.assertEqual(a[1].value, '0')

        self.assertEqual(a[2].value, '1')
        self.assertEqual(a[3].value, '1')

        self.assertEqual(a[4].value, '2')
        self.assertEqual(a[5].value, '2')

        self.assertEqual(a[6].value, '3')
        self.assertEqual(a[7].value, '3')

        self.assertEqual(a[8].value, '4')
        self.assertEqual(a[9].value, '4')

    def test_change_instance_var(self):
        target_entity_name = 'tests.stub_sut.ChangeState.change_instance_var'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestChangeState.test_change_instance_var', [target_entity_name])

        self.assertEqual(trace_result[target_entity_name].flows[0].run_lines, [100, 101])
        self.assertEqual(trace_result[target_entity_name].target_entity_name, 'change_instance_var')

        state_result = trace_result[target_entity_name].flows[0].state_result
        obj = state_result.vars['self'].states
        self.assertEqual(len(obj), 3)

        self.assertEqual(obj[0].line, 100)
        # self.assertEqual(obj[0].value.inst_var, 'default')

        self.assertEqual(obj[1].line, 101)
        # self.assertEqual(obj[1].value.inst_var, 'foo')

        self.assertEqual(obj[2].line, 101)
        # self.assertEqual(obj[2].value.inst_var, 'new foo')

    def test_init_with_instance_var(self):
        target_entity_name = 'tests.stub_sut.ChangeState.__init__'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestChangeState.test_init', [target_entity_name])

        self.assertEqual(trace_result[target_entity_name].flows[0].run_lines, [97])
        self.assertEqual(trace_result[target_entity_name].target_entity_name, '__init__')

        state_result = trace_result[target_entity_name].flows[0].state_result
        obj = state_result.vars['self'].states
        self.assertEqual(len(obj), 2)

        self.assertEqual(obj[0].line, 97)
        self.assertNotIn('inst_var', dir(obj[0].value))

        self.assertEqual(obj[1].line, 97)
        # self.assertEqual(obj[1].value.inst_var, 'default')

    def test_keep_var_state(self):
        target_entity_name = 'tests.stub_sut.ChangeState.keep_var_state'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestChangeState.test_keep_var_state', [target_entity_name])

        self.assertEqual(trace_result[target_entity_name].flows[0].run_lines, [104, 105, 106])
        self.assertEqual(trace_result[target_entity_name].target_entity_name, 'keep_var_state')

        state_result = trace_result[target_entity_name].flows[0].state_result
        a = state_result.vars['a'].states
        self.assertEqual(a[0].value, '1')
        self.assertEqual(a[1].value, '1')
        self.assertEqual(a[2].value, '1')

        self.assertTrue(a[0].value_has_changed)
        self.assertFalse(a[1].value_has_changed)
        self.assertFalse(a[2].value_has_changed)

        # seq_values = state_result.vars['a'].distinct_sequential_values()
        # self.assertEqual(seq_values, [1])


if __name__ == '__main__':
    unittest.main()