import unittest
from tests.unit.stub_test import TReturnValue
from spotflow.api import monitor_func


class TestArg(unittest.TestCase):

    def test_simple_return_local(self):
        method_name = 'tests.unit.stub_sut.ReturnValue.simple_return'
        func = TReturnValue().test_simple_return_local

        result = monitor_func(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        call_state = calls[0].call_state

        args = call_state.arg_states
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

    def test_simple_return_global(self):
        method_name = 'tests.unit.stub_sut.ReturnValue.simple_return'
        func = TReturnValue().test_simple_return_global

        result = monitor_func(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        call_state = calls[0].call_state

        args = call_state.arg_states
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

    def test_simple_return_with_arg(self):
        method_name = 'tests.unit.stub_sut.ReturnValue.simple_return_with_arg'
        func = TReturnValue().test_simple_return_with_arg

        result = monitor_func(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        call_state = calls[0].call_state

        args = call_state.arg_states
        self.assertEqual(len(args), 3)
        self.assertEqual(args[0].name, 'self')
        self.assertEqual(args[1].name, 'msg')
        self.assertEqual(args[2].name, 'name')

    def test_change_return_0(self):
        method_name = 'tests.unit.stub_sut.ReturnValue.change_return_0'
        func = TReturnValue().test_change_return_0

        result = monitor_func(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        call_state = calls[0].call_state

        args = call_state.arg_states
        self.assertEqual(len(args), 3)
        self.assertEqual(args[0].name, 'self')
        self.assertEqual(args[1].name, 'a')
        self.assertEqual(args[2].name, 'b')

    def test_change_return_1(self):
        method_name = 'tests.unit.stub_sut.ReturnValue.change_return_1'
        func = TReturnValue().test_change_return_1

        result = monitor_func(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        call_state = calls[0].call_state

        args = call_state.arg_states
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

    def test_change_return_2(self):
        method_name = 'tests.unit.stub_sut.ReturnValue.change_return_2'
        func = TReturnValue().test_change_return_2

        result = monitor_func(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        call_state = calls[0].call_state

        args = call_state.arg_states
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

    def test_change_return_3(self):
        method_name = 'tests.unit.stub_sut.ReturnValue.change_return_3'
        func = TReturnValue().test_change_return_3

        result = monitor_func(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        call_state = calls[0].call_state

        args = call_state.arg_states
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

    def test_change_return_4(self):
        method_name = 'tests.unit.stub_sut.ReturnValue.change_return_4'
        func = TReturnValue().test_change_return_4

        result = monitor_func(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        call_state = calls[0].call_state

        args = call_state.arg_states
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

    def test_change_return_5(self):
        method_name = 'tests.unit.stub_sut.ReturnValue.change_return_5'
        func = TReturnValue().test_change_return_5

        result = monitor_func(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        call_state = calls[0].call_state

        args = call_state.arg_states
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

    def test_multiple_return_true(self):
        method_name = 'tests.unit.stub_sut.ReturnValue.multiple_return'
        func = TReturnValue().test_multiple_return_true

        result = monitor_func(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        call_state = calls[0].call_state

        args = call_state.arg_states
        self.assertEqual(len(args), 2)
        self.assertEqual(args[0].name, 'self')
        self.assertEqual(args[1].name, 'enter')

    def test_multiple_return_false(self):
        method_name = 'tests.unit.stub_sut.ReturnValue.multiple_return'
        func = TReturnValue().test_multiple_return_false

        result = monitor_func(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        call_state = calls[0].call_state

        args = call_state.arg_states
        self.assertEqual(len(args), 2)
        self.assertEqual(args[0].name, 'self')
        self.assertEqual(args[1].name, 'enter')

    def test_change_attribute_0(self):
        method_name = 'tests.unit.stub_sut.ReturnValue.change_attribute_0'
        func = TReturnValue().test_change_attribute_0

        result = monitor_func(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        call_state = calls[0].call_state

        args = call_state.arg_states
        self.assertEqual(len(args), 2)
        self.assertEqual(args[0].name, 'self')
        self.assertEqual(args[1].name, 'new_n')

    def test_change_attribute_1(self):
        method_name = 'tests.unit.stub_sut.ReturnValue.change_attribute_1'
        func = TReturnValue().test_change_attribute_1

        result = monitor_func(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        call_state = calls[0].call_state

        args = call_state.arg_states
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

    def test_change_attribute_2(self):
        method_name = 'tests.unit.stub_sut.ReturnValue.change_attribute_2'
        func = TReturnValue().test_change_attribute_2

        result = monitor_func(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        call_state = calls[0].call_state

        args = call_state.arg_states
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

    def test_change_attribute_3(self):
        method_name = 'tests.unit.stub_sut.ReturnValue.change_attribute_3'
        func = TReturnValue().test_change_attribute_3

        result = monitor_func(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        call_state = calls[0].call_state

        args = call_state.arg_states
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

    def test_change_obj_1(self):
        method_name = 'tests.unit.stub_sut.ReturnValue.change_obj_1'
        func = TReturnValue().test_change_obj_1

        result = monitor_func(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        call_state = calls[0].call_state

        args = call_state.arg_states
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

    def test_change_obj_2(self):
        method_name = 'tests.unit.stub_sut.ReturnValue.change_obj_2'
        func = TReturnValue().test_change_obj_2

        result = monitor_func(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        call_state = calls[0].call_state

        args = call_state.arg_states
        self.assertEqual(len(args), 4)
        self.assertEqual(args[0].name, 'self')
        self.assertEqual(args[1].name, 'add1')
        self.assertEqual(args[2].name, 'add2')
        self.assertEqual(args[3].name, 'sub')


if __name__ == '__main__':
    unittest.main()
