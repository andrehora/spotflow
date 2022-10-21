import unittest
from tests.unit.stub_test import TestReturnValue
from spotflow.api import monitor


class TestReturn(unittest.TestCase):

    def test_simple_return_local(self):
        method_name = 'tests.unit.stub_sut.ReturnValue.simple_return'
        func = TestReturnValue().test_simple_return_local

        result = monitor(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        call_state = calls[0].call_state
        return_state = call_state.return_state
        self.assertEqual(return_state, '100')

    def test_simple_return_global(self):
        method_name = 'tests.unit.stub_sut.ReturnValue.simple_return'
        func = TestReturnValue().test_simple_return_global

        result = monitor(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        call_state = calls[0].call_state
        return_state = call_state.return_state
        self.assertEqual(return_state, '100')

    def test_simple_return_with_arg(self):
        method_name = 'tests.unit.stub_sut.ReturnValue.simple_return_with_arg'
        func = TestReturnValue().test_simple_return_with_arg

        result = monitor(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        call_state = calls[0].call_state
        return_state = call_state.return_state
        self.assertEqual(return_state, "'hello world'")

    def test_change_return_0(self):
        method_name = 'tests.unit.stub_sut.ReturnValue.change_return_0'
        func = TestReturnValue().test_change_return_0

        result = monitor(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        call_state = calls[0].call_state
        return_state = call_state.return_state
        self.assertEqual(return_state, '300')

    def test_change_return_1(self):
        method_name = 'tests.unit.stub_sut.ReturnValue.change_return_1'
        func = TestReturnValue().test_change_return_1

        result = monitor(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        call_state = calls[0].call_state
        return_state = call_state.return_state
        self.assertEqual(return_state, '3')

    def test_change_return_2(self):
        method_name = 'tests.unit.stub_sut.ReturnValue.change_return_2'
        func = TestReturnValue().test_change_return_2

        result = monitor(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        call_state = calls[0].call_state
        return_state = call_state.return_state
        self.assertEqual(return_state, '4')

    def test_change_return_3(self):
        method_name = 'tests.unit.stub_sut.ReturnValue.change_return_3'
        func = TestReturnValue().test_change_return_3

        result = monitor(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        call_state = calls[0].call_state
        return_state = call_state.return_state
        self.assertEqual(return_state, "'a and l'")

    def test_change_return_4(self):
        method_name = 'tests.unit.stub_sut.ReturnValue.change_return_4'
        func = TestReturnValue().test_change_return_4

        result = monitor(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        call_state = calls[0].call_state
        return_state = call_state.return_state
        self.assertEqual(return_state, '[1, 2, 3]')

    def test_change_return_5(self):
        method_name = 'tests.unit.stub_sut.ReturnValue.change_return_5'
        func = TestReturnValue().test_change_return_5

        result = monitor(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        call_state = calls[0].call_state
        return_state = call_state.return_state
        self.assertEqual(return_state, '10')

    def test_multiple_return_true(self):
        method_name = 'tests.unit.stub_sut.ReturnValue.multiple_return'
        func = TestReturnValue().test_multiple_return_true

        result = monitor(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        call_state = calls[0].call_state
        return_state = call_state.return_state
        self.assertEqual(return_state, "'enter is true'")

    def test_multiple_return_false(self):
        method_name = 'tests.unit.stub_sut.ReturnValue.multiple_return'
        func = TestReturnValue().test_multiple_return_false

        result = monitor(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        call_state = calls[0].call_state
        return_state = call_state.return_state
        self.assertEqual(return_state, "'enter is false'")

    def test_change_attribute_0(self):
        method_name = 'tests.unit.stub_sut.ReturnValue.change_attribute_0'
        func = TestReturnValue().test_change_attribute_0

        result = monitor(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        call_state = calls[0].call_state
        return_state = call_state.return_state
        self.assertEqual(return_state, '500')

    def test_change_attribute_1(self):
        method_name = 'tests.unit.stub_sut.ReturnValue.change_attribute_1'
        func = TestReturnValue().test_change_attribute_1

        result = monitor(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        call_state = calls[0].call_state
        return_state = call_state.return_state
        self.assertEqual(return_state, '101')

    def test_change_attribute_2(self):
        method_name = 'tests.unit.stub_sut.ReturnValue.change_attribute_2'
        func = TestReturnValue().test_change_attribute_2

        result = monitor(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        call_state = calls[0].call_state
        return_state = call_state.return_state
        self.assertEqual(return_state, "'foo'")

    def test_change_attribute_3(self):
        method_name = 'tests.unit.stub_sut.ReturnValue.change_attribute_3'
        func = TestReturnValue().test_change_attribute_3

        result = monitor(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        call_state = calls[0].call_state
        return_state = call_state.return_state
        self.assertEqual(return_state, '5')

    def test_change_obj_1(self):
        method_name = 'tests.unit.stub_sut.ReturnValue.change_obj_1'
        func = TestReturnValue().test_change_obj_1

        result = monitor(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        call_state = calls[0].call_state
        return_state = call_state.return_state
        self.assertEqual(return_state, '9')

    def test_change_obj_2(self):
        method_name = 'tests.unit.stub_sut.ReturnValue.change_obj_2'
        func = TestReturnValue().test_change_obj_2

        result = monitor(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        call_state = calls[0].call_state
        return_state = call_state.return_state
        self.assertEqual(return_state, '19')

    def test_explicit_return_state(self):
        method_name = 'tests.unit.stub_sut.ReturnValue.explicit_return_state'
        func = TestReturnValue().test_explicit_return_state

        result = monitor(func, [method_name])

        calls = result[method_name].calls
        return_state = calls[0].call_state.return_state

        self.assertEqual(return_state.value, '123')

    def test_explicit_return_none(self):
        method_name = 'tests.unit.stub_sut.ReturnValue.explicit_return_none'
        func = TestReturnValue().test_explicit_return_none

        result = monitor(func, [method_name])

        calls = result[method_name].calls
        return_state = calls[0].call_state.return_state

        self.assertEqual(return_state.value, 'None')

    def test_explicit_return(self):
        method_name = 'tests.unit.stub_sut.ReturnValue.explicit_return'
        func = TestReturnValue().test_explicit_return

        result = monitor(func, [method_name])

        calls = result[method_name].calls
        return_state = calls[0].call_state.return_state

        self.assertEqual(return_state.value, 'None')

    def test_implicit_return(self):
        method_name = 'tests.unit.stub_sut.ReturnValue.implicit_return'
        func = TestReturnValue().test_implicit_return

        result = monitor(func, [method_name])

        calls = result[method_name].calls
        return_state = calls[0].call_state.return_state

        self.assertIsNone(return_state)


if __name__ == '__main__':
    unittest.main()
