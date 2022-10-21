import unittest
from tests.unit.stub_test import TestChangeState
from spotflow.api import monitor


class TestState(unittest.TestCase):

    def test_change_var_state(self):
        method_name = 'tests.unit.stub_sut.ChangeState.change_var_state'
        func = TestChangeState().test_change_var_state

        result = monitor(func, [method_name])

        self.assertEqual(result[method_name].calls[0].run_lines, [59, 60, 61])
        self.assertEqual(result[method_name].name, 'change_var_state')

        call_state = result[method_name].calls[0].call_state
        a = call_state.var_states['a'].states
        self.assertEqual(a[0].value, '1')
        self.assertEqual(a[1].value, '2')
        self.assertEqual(a[2].value, '3')

        self.assertTrue(a[0].value_has_changed)
        self.assertTrue(a[1].value_has_changed)
        self.assertTrue(a[2].value_has_changed)


    def test_change_arg_state(self):
        method_name = 'tests.unit.stub_sut.ChangeState.change_arg_state'
        func = TestChangeState().test_change_arg_state

        result = monitor(func, [method_name])

        self.assertEqual(result[method_name].calls[0].run_lines, [64, 65, 66])
        self.assertEqual(result[method_name].name, 'change_arg_state')

        call_state = result[method_name].calls[0].call_state
        a = call_state.var_states['a'].states
        self.assertEqual(a[0].value, '0')
        self.assertEqual(a[1].value, '1')
        self.assertEqual(a[2].value, '2')
        self.assertEqual(a[3].value, '3')

    def test_change_var_state_with_conditional_true(self):
        method_name = 'tests.unit.stub_sut.ChangeState.change_var_state_with_conditional'
        func = TestChangeState().test_change_var_state_with_conditional_true

        result = monitor(func, [method_name])

        self.assertEqual(result[method_name].calls[0].run_lines, [69, 70, 71])
        self.assertEqual(result[method_name].name, 'change_var_state_with_conditional')

        call_state = result[method_name].calls[0].call_state
        a = call_state.var_states['a'].states
        self.assertEqual(a[0].value, '1')
        self.assertEqual(a[-1].value, '100')

        first, last = call_state.var_states['a'].first_last()
        self.assertEqual(first.value, '1')
        self.assertEqual(last.value, '100')

    def test_change_var_state_with_conditional_false(self):
        method_name = 'tests.unit.stub_sut.ChangeState.change_var_state_with_conditional'
        func = TestChangeState().test_change_var_state_with_conditional_false

        result = monitor(func, [method_name])

        self.assertEqual(result[method_name].calls[0].run_lines, [69, 70, 73])
        self.assertEqual(result[method_name].name, 'change_var_state_with_conditional')

        call_state = result[method_name].calls[0].call_state
        a = call_state.var_states['a'].states
        self.assertEqual(a[0].value, '1')
        self.assertEqual(a[-1].value, '200')

        first, last = call_state.var_states['a'].first_last()
        self.assertEqual(first.value, '1')
        self.assertEqual(last.value, '200')

    def test_change_multiple_vars_states(self):
        method_name = 'tests.unit.stub_sut.ChangeState.change_multiple_vars_states'
        func = TestChangeState().test_change_multiple_vars_states

        result = monitor(func, [method_name])

        self.assertEqual(result[method_name].calls[0].run_lines, [76, 77, 79, 80])
        self.assertEqual(result[method_name].name, 'change_multiple_vars_states')

        call_state = result[method_name].calls[0].call_state

        first, last = call_state.var_states['a'].first_last()
        self.assertEqual(first.value, '1')
        self.assertEqual(last.value, '2')

        first, last = call_state.var_states['b'].first_last()
        self.assertEqual(first.value, '10')
        self.assertEqual(last.value, '110')

    def test_change_list_state(self):
        method_name = 'tests.unit.stub_sut.ChangeState.change_list_state'
        func = TestChangeState().test_change_list_state

        result = monitor(func, [method_name])

        self.assertEqual(result[method_name].calls[0].run_lines, [83, 84, 85, 86, 87, 88, 89])
        self.assertEqual(result[method_name].name, 'change_list_state')

        call_state = result[method_name].calls[0].call_state
        a_list = call_state.var_states['a'].states
        self.assertEqual(a_list[0].value, '[]')
        self.assertEqual(a_list[1].value, '[1]')
        self.assertEqual(a_list[2].value, '[1, 2]')
        self.assertEqual(a_list[3].value, '[1, 2, 3]')
        self.assertEqual(a_list[4].value, '[1, 2]')
        self.assertEqual(a_list[5].value, '[1]')
        self.assertEqual(a_list[6].value, '[]')

    def test_change_var_state_with_loop(self):
        method_name = 'tests.unit.stub_sut.ChangeState.change_var_state_with_loop'
        func = TestChangeState().test_change_var_state_with_loop

        result = monitor(func, [method_name])

        self.assertEqual(result[method_name].calls[0].run_lines, [92, 93, 94, 93, 94, 93, 94, 93, 94, 93])
        self.assertEqual(result[method_name].calls[0].distinct_run_lines(), [92, 93, 94])
        self.assertEqual(result[method_name].name, 'change_var_state_with_loop')

        call_state = result[method_name].calls[0].call_state
        a = call_state.var_states['a'].states
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
        method_name = 'tests.unit.stub_sut.ChangeState.change_instance_var'
        func = TestChangeState().test_change_instance_var

        result = monitor(func, [method_name])

        self.assertEqual(result[method_name].calls[0].run_lines, [100, 101])
        self.assertEqual(result[method_name].name, 'change_instance_var')

        call_state = result[method_name].calls[0].call_state
        obj = call_state.var_states['self'].states
        self.assertEqual(len(obj), 3)

        self.assertEqual(obj[0].lineno, 100)

        self.assertEqual(obj[1].lineno, 101)

        self.assertEqual(obj[2].lineno, 101)

    def test_init_with_instance_var(self):
        method_name = 'tests.unit.stub_sut.ChangeState.__init__'
        func = TestChangeState().test_init

        result = monitor(func, [method_name])

        self.assertEqual(result[method_name].calls[0].run_lines, [97])
        self.assertEqual(result[method_name].name, '__init__')

        call_state = result[method_name].calls[0].call_state
        obj = call_state.var_states['self'].states
        self.assertEqual(len(obj), 2)

        self.assertEqual(obj[0].lineno, 97)
        self.assertNotIn('inst_var', dir(obj[0].value))

        self.assertEqual(obj[1].lineno, 97)
        # self.assertEqual(obj[1].value.inst_var, 'default')

    def test_keep_var_state(self):
        method_name = 'tests.unit.stub_sut.ChangeState.keep_var_state'
        func = TestChangeState().test_keep_var_state

        result = monitor(func, [method_name])

        self.assertEqual(result[method_name].calls[0].run_lines, [104, 105, 106])
        self.assertEqual(result[method_name].name, 'keep_var_state')

        call_state = result[method_name].calls[0].call_state
        a = call_state.var_states['a'].states
        self.assertEqual(a[0].value, '1')
        self.assertEqual(a[1].value, '1')
        self.assertEqual(a[2].value, '1')

        self.assertTrue(a[0].value_has_changed)
        self.assertFalse(a[1].value_has_changed)
        self.assertFalse(a[2].value_has_changed)


if __name__ == '__main__':
    unittest.main()