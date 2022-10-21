import unittest
from tests.unit.stub_test import TestClassWithManyCalls
from spotflow.api import monitor


class TestFilter(unittest.TestCase):

    def test_basics(self):
        method_name = 'tests.unit.stub_sut.ClassWithManyCalls.method_called_many_times'
        func = TestClassWithManyCalls().test_method_called_many_times

        result = monitor(func, [method_name])

        self.assertEqual(len(result), 1)
        self.assertEqual(len(result.all_methods()), 1)
        self.assertEqual(len(result.all_calls()), 100)
        self.assertEqual(result.all_methods()[0], result[method_name])

    def test_filter_calls_based_on_specific_arg_value(self):
        method_name = 'tests.unit.stub_sut.ClassWithManyCalls'
        func = TestClassWithManyCalls().test_call_methods

        result = monitor(func, [method_name])

        def with_arg_value_123(call):
            arg_states = call.call_state.arg_states
            for arg_state in arg_states:
                if arg_state.name == 'arg1' and arg_state.value == '123':
                    return True
            return False

        filtered_calls = []
        for call in result.all_calls():
            if with_arg_value_123(call):
                filtered_calls.append(call)

        self.assertEqual(len(list(filtered_calls)), 1)
        self.assertEqual(len(result.all_calls()), 4)

    def test_filter_calls_based_on_specific_return_value(self):
        method_name = 'tests.unit.stub_sut.ClassWithManyCalls'
        func = TestClassWithManyCalls().test_call_methods

        result = monitor(func, [method_name])

        def with_return_value_123(call):
            return_state = call.call_state.return_state
            return return_state and return_state.value == '123'

        filtered_calls = []
        for call in result.all_calls():
            if with_return_value_123(call):
                filtered_calls.append(call)

        self.assertEqual(len(list(filtered_calls)), 1)
        self.assertEqual(len(result.all_calls()), 4)

    def test_filter_calls_based_on_exceptions(self):
        method_name = 'tests.unit.stub_sut.ClassWithManyCalls'
        func = TestClassWithManyCalls().test_call_methods

        result = monitor(func, [method_name])

        def with_exception(call):
            return call.call_state.has_exception()

        filtered_calls = []
        for call in result.all_calls():
            if with_exception(call):
                filtered_calls.append(call)

        self.assertEqual(len(list(filtered_calls)), 2)
        self.assertEqual(len(result.all_calls()), 4)

    def test_filter_calls_based_on_specific_exception(self):
        method_name = 'tests.unit.stub_sut.ClassWithManyCalls'
        func = TestClassWithManyCalls().test_call_methods

        result = monitor(func, [method_name])

        def with_ZeroDivisionError(call):
            exception_state = call.call_state.exception_state
            return exception_state and exception_state.value == 'ZeroDivisionError'

        filtered_calls = []
        for call in result.all_calls():
            if with_ZeroDivisionError(call):
                filtered_calls.append(call)

        self.assertEqual(len(list(filtered_calls)), 2)
        self.assertEqual(len(result.all_calls()), 4)

    def test_filter_calls_based_on_arg_values(self):
        method_name = 'tests.unit.stub_sut.ClassWithManyCalls.method_called_many_times'
        func = TestClassWithManyCalls().test_method_called_many_times

        result = monitor(func, [method_name])

        def with_arg_value_less_than_51(call):
            arg_states = call.call_state.arg_states
            for arg_state in arg_states:
                if arg_state.name == 'index' and int(arg_state.value) < 51:
                    return True
            return False

        filtered_calls = []
        for call in result.all_calls():
            if with_arg_value_less_than_51(call):
                filtered_calls.append(call)

        self.assertEqual(len(list(filtered_calls)), 50)
        self.assertEqual(len(result.all_calls()), 100)

    def test_filter_calls_based_on_return_values(self):
        method_name = 'tests.unit.stub_sut.ClassWithManyCalls.method_called_many_times'
        func = TestClassWithManyCalls().test_method_called_many_times

        result = monitor(func, [method_name])

        def with_return_value_less_than_51(call):
            return_state = call.call_state.return_state
            return return_state and int(return_state.value) < 51

        filtered_calls = []
        for call in result.all_calls():
            if with_return_value_less_than_51(call):
                filtered_calls.append(call)

        self.assertEqual(len(list(filtered_calls)), 50)
        self.assertEqual(len(result.all_calls()), 100)


if __name__ == '__main__':
    unittest.main()