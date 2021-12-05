import unittest
from tests.stub_test import TestReturnValue
from happyflow.api import run_and_flow_func


class TestReturn(unittest.TestCase):

    def test_simple_return_local(self):
        target_method_name = 'tests.stub_sut.ReturnValue.simple_return'
        func = TestReturnValue().test_simple_return_local

        result = run_and_flow_func(func, [target_method_name])

        flows = result[target_method_name].calls
        self.assertEqual(len(flows), 1)

        call_state = flows[0].call_state
        return_state = call_state.return_state
        self.assertEqual(return_state, '100')

    def test_simple_return_global(self):
        target_method_name = 'tests.stub_sut.ReturnValue.simple_return'
        func = TestReturnValue().test_simple_return_global

        result = run_and_flow_func(func, [target_method_name])

        flows = result[target_method_name].calls
        self.assertEqual(len(flows), 1)

        call_state = flows[0].call_state
        return_state = call_state.return_state
        self.assertEqual(return_state, '100')

    def test_simple_return_with_arg(self):
        target_method_name = 'tests.stub_sut.ReturnValue.simple_return_with_arg'
        func = TestReturnValue().test_simple_return_with_arg

        result = run_and_flow_func(func, [target_method_name])

        flows = result[target_method_name].calls
        self.assertEqual(len(flows), 1)

        call_state = flows[0].call_state
        return_state = call_state.return_state
        self.assertEqual(return_state, "'hello world'")

    def test_change_return_0(self):
        target_method_name = 'tests.stub_sut.ReturnValue.change_return_0'
        func = TestReturnValue().test_change_return_0

        result = run_and_flow_func(func, [target_method_name])

        flows = result[target_method_name].calls
        self.assertEqual(len(flows), 1)

        call_state = flows[0].call_state
        return_state = call_state.return_state
        self.assertEqual(return_state, '300')

    def test_change_return_1(self):
        target_method_name = 'tests.stub_sut.ReturnValue.change_return_1'
        func = TestReturnValue().test_change_return_1

        result = run_and_flow_func(func, [target_method_name])

        flows = result[target_method_name].calls
        self.assertEqual(len(flows), 1)

        call_state = flows[0].call_state
        return_state = call_state.return_state
        self.assertEqual(return_state, '3')

    def test_change_return_2(self):
        target_method_name = 'tests.stub_sut.ReturnValue.change_return_2'
        func = TestReturnValue().test_change_return_2

        result = run_and_flow_func(func, [target_method_name])

        flows = result[target_method_name].calls
        self.assertEqual(len(flows), 1)

        call_state = flows[0].call_state
        return_state = call_state.return_state
        self.assertEqual(return_state, '4')

    def test_change_return_3(self):
        target_method_name = 'tests.stub_sut.ReturnValue.change_return_3'
        func = TestReturnValue().test_change_return_3

        result = run_and_flow_func(func, [target_method_name])

        flows = result[target_method_name].calls
        self.assertEqual(len(flows), 1)

        call_state = flows[0].call_state
        return_state = call_state.return_state
        self.assertEqual(return_state, "'a and l'")

    def test_change_return_4(self):
        target_method_name = 'tests.stub_sut.ReturnValue.change_return_4'
        func = TestReturnValue().test_change_return_4

        result = run_and_flow_func(func, [target_method_name])

        flows = result[target_method_name].calls
        self.assertEqual(len(flows), 1)

        call_state = flows[0].call_state
        return_state = call_state.return_state
        self.assertEqual(return_state, '[1, 2, 3]')

    def test_change_return_5(self):
        target_method_name = 'tests.stub_sut.ReturnValue.change_return_5'
        func = TestReturnValue().test_change_return_5

        result = run_and_flow_func(func, [target_method_name])

        flows = result[target_method_name].calls
        self.assertEqual(len(flows), 1)

        call_state = flows[0].call_state
        return_state = call_state.return_state
        self.assertEqual(return_state, '10')

    def test_multiple_return_true(self):
        target_method_name = 'tests.stub_sut.ReturnValue.multiple_return'
        func = TestReturnValue().test_multiple_return_true

        result = run_and_flow_func(func, [target_method_name])

        flows = result[target_method_name].calls
        self.assertEqual(len(flows), 1)

        call_state = flows[0].call_state
        return_state = call_state.return_state
        self.assertEqual(return_state, "'enter is true'")

    def test_multiple_return_false(self):
        target_method_name = 'tests.stub_sut.ReturnValue.multiple_return'
        func = TestReturnValue().test_multiple_return_false

        result = run_and_flow_func(func, [target_method_name])

        flows = result[target_method_name].calls
        self.assertEqual(len(flows), 1)

        call_state = flows[0].call_state
        return_state = call_state.return_state
        self.assertEqual(return_state, "'enter is false'")

    def test_change_attribute_0(self):
        target_method_name = 'tests.stub_sut.ReturnValue.change_attribute_0'
        func = TestReturnValue().test_change_attribute_0

        result = run_and_flow_func(func, [target_method_name])

        flows = result[target_method_name].calls
        self.assertEqual(len(flows), 1)

        call_state = flows[0].call_state
        return_state = call_state.return_state
        self.assertEqual(return_state, '500')

    def test_change_attribute_1(self):
        target_method_name = 'tests.stub_sut.ReturnValue.change_attribute_1'
        func = TestReturnValue().test_change_attribute_1

        result = run_and_flow_func(func, [target_method_name])

        flows = result[target_method_name].calls
        self.assertEqual(len(flows), 1)

        call_state = flows[0].call_state
        return_state = call_state.return_state
        self.assertEqual(return_state, '101')

    def test_change_attribute_2(self):
        target_method_name = 'tests.stub_sut.ReturnValue.change_attribute_2'
        func = TestReturnValue().test_change_attribute_2

        result = run_and_flow_func(func, [target_method_name])

        flows = result[target_method_name].calls
        self.assertEqual(len(flows), 1)

        call_state = flows[0].call_state
        return_state = call_state.return_state
        self.assertEqual(return_state, "'foo'")

    def test_change_attribute_3(self):
        target_method_name = 'tests.stub_sut.ReturnValue.change_attribute_3'
        func = TestReturnValue().test_change_attribute_3

        result = run_and_flow_func(func, [target_method_name])

        flows = result[target_method_name].calls
        self.assertEqual(len(flows), 1)

        call_state = flows[0].call_state
        return_state = call_state.return_state
        self.assertEqual(return_state, '5')

    def test_change_obj_1(self):
        target_method_name = 'tests.stub_sut.ReturnValue.change_obj_1'
        func = TestReturnValue().test_change_obj_1

        result = run_and_flow_func(func, [target_method_name])

        flows = result[target_method_name].calls
        self.assertEqual(len(flows), 1)

        call_state = flows[0].call_state
        return_state = call_state.return_state
        self.assertEqual(return_state, '9')

    def test_change_obj_2(self):
        target_method_name = 'tests.stub_sut.ReturnValue.change_obj_2'
        func = TestReturnValue().test_change_obj_2

        result = run_and_flow_func(func, [target_method_name])

        flows = result[target_method_name].calls
        self.assertEqual(len(flows), 1)

        call_state = flows[0].call_state
        return_state = call_state.return_state
        self.assertEqual(return_state, '19')

    def test_explicit_return_state(self):
        target_method_name = 'tests.stub_sut.ReturnValue.explicit_return_state'
        func = TestReturnValue().test_explicit_return_state

        result = run_and_flow_func(func, [target_method_name])

        flows = result[target_method_name].calls
        return_state = flows[0].call_state.return_state

        self.assertEqual(return_state.value, '123')

    def test_explicit_return_none(self):
        target_method_name = 'tests.stub_sut.ReturnValue.explicit_return_none'
        func = TestReturnValue().test_explicit_return_none

        result = run_and_flow_func(func, [target_method_name])

        flows = result[target_method_name].calls
        return_state = flows[0].call_state.return_state

        self.assertEqual(return_state.value, 'None')

    def test_explicit_return(self):
        target_method_name = 'tests.stub_sut.ReturnValue.explicit_return'
        func = TestReturnValue().test_explicit_return

        result = run_and_flow_func(func, [target_method_name])

        flows = result[target_method_name].calls
        return_state = flows[0].call_state.return_state

        self.assertEqual(return_state.value, 'None')

    def test_implicit_return(self):
        target_method_name = 'tests.stub_sut.ReturnValue.implicit_return'
        func = TestReturnValue().test_implicit_return

        result = run_and_flow_func(func, [target_method_name])

        flows = result[target_method_name].calls
        return_state = flows[0].call_state.return_state

        self.assertIsNone(return_state)


if __name__ == '__main__':
    unittest.main()
