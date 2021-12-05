import unittest
from tests.stub_test import TestReturnValue
from happyflow.api import run_and_flow_func


class TestArg(unittest.TestCase):

    def test_simple_return_local(self):
        target_method_name = 'tests.stub_sut.ReturnValue.simple_return'
        func = TestReturnValue().test_simple_return_local

        result = run_and_flow_func(func, [target_method_name])

        flows = result[target_method_name].calls
        self.assertEqual(len(flows), 1)

        call_state = flows[0].call_state

        args = call_state.arg_states
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

    def test_simple_return_global(self):
        target_method_name = 'tests.stub_sut.ReturnValue.simple_return'
        func = TestReturnValue().test_simple_return_global

        result = run_and_flow_func(func, [target_method_name])

        flows = result[target_method_name].calls
        self.assertEqual(len(flows), 1)

        call_state = flows[0].call_state

        args = call_state.arg_states
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

    def test_simple_return_with_arg(self):
        target_method_name = 'tests.stub_sut.ReturnValue.simple_return_with_arg'
        func = TestReturnValue().test_simple_return_with_arg

        result = run_and_flow_func(func, [target_method_name])

        flows = result[target_method_name].calls
        self.assertEqual(len(flows), 1)

        call_state = flows[0].call_state

        args = call_state.arg_states
        self.assertEqual(len(args), 3)
        self.assertEqual(args[0].name, 'self')
        self.assertEqual(args[1].name, 'msg')
        self.assertEqual(args[2].name, 'name')

    def test_change_return_0(self):
        target_method_name = 'tests.stub_sut.ReturnValue.change_return_0'
        func = TestReturnValue().test_change_return_0

        result = run_and_flow_func(func, [target_method_name])

        flows = result[target_method_name].calls
        self.assertEqual(len(flows), 1)

        call_state = flows[0].call_state

        args = call_state.arg_states
        self.assertEqual(len(args), 3)
        self.assertEqual(args[0].name, 'self')
        self.assertEqual(args[1].name, 'a')
        self.assertEqual(args[2].name, 'b')

    def test_change_return_1(self):
        target_method_name = 'tests.stub_sut.ReturnValue.change_return_1'
        func = TestReturnValue().test_change_return_1

        result = run_and_flow_func(func, [target_method_name])

        flows = result[target_method_name].calls
        self.assertEqual(len(flows), 1)

        call_state = flows[0].call_state

        args = call_state.arg_states
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

    def test_change_return_2(self):
        target_method_name = 'tests.stub_sut.ReturnValue.change_return_2'
        func = TestReturnValue().test_change_return_2

        result = run_and_flow_func(func, [target_method_name])

        flows = result[target_method_name].calls
        self.assertEqual(len(flows), 1)

        call_state = flows[0].call_state

        args = call_state.arg_states
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

    def test_change_return_3(self):
        target_method_name = 'tests.stub_sut.ReturnValue.change_return_3'
        func = TestReturnValue().test_change_return_3

        result = run_and_flow_func(func, [target_method_name])

        flows = result[target_method_name].calls
        self.assertEqual(len(flows), 1)

        call_state = flows[0].call_state

        args = call_state.arg_states
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

    def test_change_return_4(self):
        target_method_name = 'tests.stub_sut.ReturnValue.change_return_4'
        func = TestReturnValue().test_change_return_4

        result = run_and_flow_func(func, [target_method_name])

        flows = result[target_method_name].calls
        self.assertEqual(len(flows), 1)

        call_state = flows[0].call_state

        args = call_state.arg_states
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

    def test_change_return_5(self):
        target_method_name = 'tests.stub_sut.ReturnValue.change_return_5'
        func = TestReturnValue().test_change_return_5

        result = run_and_flow_func(func, [target_method_name])

        flows = result[target_method_name].calls
        self.assertEqual(len(flows), 1)

        call_state = flows[0].call_state

        args = call_state.arg_states
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

    def test_multiple_return_true(self):
        target_method_name = 'tests.stub_sut.ReturnValue.multiple_return'
        func = TestReturnValue().test_multiple_return_true

        result = run_and_flow_func(func, [target_method_name])

        flows = result[target_method_name].calls
        self.assertEqual(len(flows), 1)

        call_state = flows[0].call_state

        args = call_state.arg_states
        self.assertEqual(len(args), 2)
        self.assertEqual(args[0].name, 'self')
        self.assertEqual(args[1].name, 'enter')

    def test_multiple_return_false(self):
        target_method_name = 'tests.stub_sut.ReturnValue.multiple_return'
        func = TestReturnValue().test_multiple_return_false

        result = run_and_flow_func(func, [target_method_name])

        flows = result[target_method_name].calls
        self.assertEqual(len(flows), 1)

        call_state = flows[0].call_state

        args = call_state.arg_states
        self.assertEqual(len(args), 2)
        self.assertEqual(args[0].name, 'self')
        self.assertEqual(args[1].name, 'enter')

    def test_change_attribute_0(self):
        target_method_name = 'tests.stub_sut.ReturnValue.change_attribute_0'
        func = TestReturnValue().test_change_attribute_0

        result = run_and_flow_func(func, [target_method_name])

        flows = result[target_method_name].calls
        self.assertEqual(len(flows), 1)

        call_state = flows[0].call_state

        args = call_state.arg_states
        self.assertEqual(len(args), 2)
        self.assertEqual(args[0].name, 'self')
        self.assertEqual(args[1].name, 'new_n')

    def test_change_attribute_1(self):
        target_method_name = 'tests.stub_sut.ReturnValue.change_attribute_1'
        func = TestReturnValue().test_change_attribute_1

        result = run_and_flow_func(func, [target_method_name])

        flows = result[target_method_name].calls
        self.assertEqual(len(flows), 1)

        call_state = flows[0].call_state

        args = call_state.arg_states
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

    def test_change_attribute_2(self):
        target_method_name = 'tests.stub_sut.ReturnValue.change_attribute_2'
        func = TestReturnValue().test_change_attribute_2

        result = run_and_flow_func(func, [target_method_name])

        flows = result[target_method_name].calls
        self.assertEqual(len(flows), 1)

        call_state = flows[0].call_state

        args = call_state.arg_states
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

    def test_change_attribute_3(self):
        target_method_name = 'tests.stub_sut.ReturnValue.change_attribute_3'
        func = TestReturnValue().test_change_attribute_3

        result = run_and_flow_func(func, [target_method_name])

        flows = result[target_method_name].calls
        self.assertEqual(len(flows), 1)

        call_state = flows[0].call_state

        args = call_state.arg_states
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

    def test_change_obj_1(self):
        target_method_name = 'tests.stub_sut.ReturnValue.change_obj_1'
        func = TestReturnValue().test_change_obj_1

        result = run_and_flow_func(func, [target_method_name])

        flows = result[target_method_name].calls
        self.assertEqual(len(flows), 1)

        call_state = flows[0].call_state

        args = call_state.arg_states
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

    def test_change_obj_2(self):
        target_method_name = 'tests.stub_sut.ReturnValue.change_obj_2'
        func = TestReturnValue().test_change_obj_2

        result = run_and_flow_func(func, [target_method_name])

        flows = result[target_method_name].calls
        self.assertEqual(len(flows), 1)

        call_state = flows[0].call_state

        args = call_state.arg_states
        self.assertEqual(len(args), 4)
        self.assertEqual(args[0].name, 'self')
        self.assertEqual(args[1].name, 'add1')
        self.assertEqual(args[2].name, 'add2')
        self.assertEqual(args[3].name, 'sub')


if __name__ == '__main__':
    unittest.main()
