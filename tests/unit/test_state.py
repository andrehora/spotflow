import unittest
from tests.unit.stub_test import TChangeState
from spotflow.api import monitor_func


class TestState(unittest.TestCase):

    def test_change_var_state(self):
        method_name = 'tests.unit.stub_sut.ChangeState.change_var_state'
        func = TChangeState().test_change_var_state

        result = monitor_func(func, [method_name])

        self.assertEqual(result[method_name].calls[0].run_lines, [59, 60, 61])
        self.assertEqual(result[method_name].name, 'change_var_state')



    def test_change_arg_state(self):
        method_name = 'tests.unit.stub_sut.ChangeState.change_arg_state'
        func = TChangeState().test_change_arg_state

        result = monitor_func(func, [method_name])

        self.assertEqual(result[method_name].calls[0].run_lines, [64, 65, 66])
        self.assertEqual(result[method_name].name, 'change_arg_state')


    def test_change_var_state_with_conditional_true(self):
        method_name = 'tests.unit.stub_sut.ChangeState.change_var_state_with_conditional'
        func = TChangeState().test_change_var_state_with_conditional_true

        result = monitor_func(func, [method_name])

        self.assertEqual(result[method_name].calls[0].run_lines, [69, 70, 71])
        self.assertEqual(result[method_name].name, 'change_var_state_with_conditional')


    def test_change_var_state_with_conditional_false(self):
        method_name = 'tests.unit.stub_sut.ChangeState.change_var_state_with_conditional'
        func = TChangeState().test_change_var_state_with_conditional_false

        result = monitor_func(func, [method_name])

        self.assertEqual(result[method_name].calls[0].run_lines, [69, 70, 73])
        self.assertEqual(result[method_name].name, 'change_var_state_with_conditional')


    def test_change_multiple_vars_states(self):
        method_name = 'tests.unit.stub_sut.ChangeState.change_multiple_vars_states'
        func = TChangeState().test_change_multiple_vars_states

        result = monitor_func(func, [method_name])

        self.assertEqual(result[method_name].calls[0].run_lines, [76, 77, 79, 80])
        self.assertEqual(result[method_name].name, 'change_multiple_vars_states')


    def test_change_list_state(self):
        method_name = 'tests.unit.stub_sut.ChangeState.change_list_state'
        func = TChangeState().test_change_list_state

        result = monitor_func(func, [method_name])

        self.assertEqual(result[method_name].calls[0].run_lines, [83, 84, 85, 86, 87, 88, 89])
        self.assertEqual(result[method_name].name, 'change_list_state')


    def test_change_var_state_with_loop(self):
        method_name = 'tests.unit.stub_sut.ChangeState.change_var_state_with_loop'
        func = TChangeState().test_change_var_state_with_loop

        result = monitor_func(func, [method_name])

        self.assertEqual(result[method_name].calls[0].run_lines, [92, 93, 94, 93, 94, 93, 94, 93, 94, 93])
        self.assertEqual(result[method_name].calls[0].distinct_run_lines(), [92, 93, 94])
        self.assertEqual(result[method_name].name, 'change_var_state_with_loop')


    def test_change_instance_var(self):
        method_name = 'tests.unit.stub_sut.ChangeState.change_instance_var'
        func = TChangeState().test_change_instance_var

        result = monitor_func(func, [method_name])

        self.assertEqual(result[method_name].calls[0].run_lines, [100, 101])
        self.assertEqual(result[method_name].name, 'change_instance_var')


    def test_init_with_instance_var(self):
        method_name = 'tests.unit.stub_sut.ChangeState.__init__'
        func = TChangeState().test_init

        result = monitor_func(func, [method_name])

        self.assertEqual(result[method_name].calls[0].run_lines, [97])
        self.assertEqual(result[method_name].name, '__init__')


    def test_keep_var_state(self):
        method_name = 'tests.unit.stub_sut.ChangeState.keep_var_state'
        func = TChangeState().test_keep_var_state

        result = monitor_func(func, [method_name])

        self.assertEqual(result[method_name].calls[0].run_lines, [104, 105, 106])
        self.assertEqual(result[method_name].name, 'keep_var_state')



if __name__ == '__main__':
    unittest.main()