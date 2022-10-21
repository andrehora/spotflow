import unittest
from tests.unit.stub_test import TestExceptions
from spotflow.api import monitor


class TestException(unittest.TestCase):

    def test_zero_division(self):
        method_name = 'tests.unit.stub_sut.Exceptions.zero_division'
        func = TestExceptions().test_zero_division

        result = monitor(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        call_state = calls[0].call_state
        exception_state = call_state.exception_state
        self.assertEqual(exception_state.lineno, 237)
        self.assertEqual(exception_state.value, 'ZeroDivisionError')

    def test_raise_generic_exception(self):
        method_name = 'tests.unit.stub_sut.Exceptions.raise_generic_exception'
        func = TestExceptions().test_raise_generic_exception

        result = monitor(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        call_state = calls[0].call_state
        exception_state = call_state.exception_state
        self.assertEqual(exception_state.lineno, 240)
        self.assertEqual(exception_state.value, 'Exception')

    def test_raise_specific_exception(self):
        method_name = 'tests.unit.stub_sut.Exceptions.raise_specific_exception'
        func = TestExceptions().test_raise_specific_exception

        result = monitor(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        call_state = calls[0].call_state
        exception_state = call_state.exception_state
        self.assertEqual(exception_state.lineno, 243)
        self.assertEqual(exception_state.value, 'TypeError')


    def test_raise_exception_line_1(self):
        method_name = 'tests.unit.stub_sut.Exceptions.raise_distinct_exception'
        func = TestExceptions().test_raise_exception_line_1

        result = monitor(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        run_lines = calls[0].run_lines
        self.assertEqual(run_lines, [246])

        call_state = calls[0].call_state
        exception_state = call_state.exception_state
        self.assertEqual(exception_state.lineno, 246)
        self.assertEqual(exception_state.value, 'Exception')

    def test_raise_exception_line_2(self):
        method_name = 'tests.unit.stub_sut.Exceptions.raise_distinct_exception'
        func = TestExceptions().test_raise_exception_line_2

        result = monitor(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        run_lines = calls[0].run_lines
        self.assertEqual(run_lines, [246, 247])

        call_state = calls[0].call_state
        exception_state = call_state.exception_state
        self.assertEqual(exception_state.lineno, 247)
        self.assertEqual(exception_state.value, 'Exception')

    def test_raise_exception_line_3(self):
        method_name = 'tests.unit.stub_sut.Exceptions.raise_distinct_exception'
        func = TestExceptions().test_raise_exception_line_3

        result = monitor(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        run_lines = calls[0].run_lines
        self.assertEqual(run_lines, [246, 247, 248])

        call_state = calls[0].call_state
        exception_state = call_state.exception_state
        self.assertEqual(exception_state.lineno, 248)
        self.assertEqual(exception_state.value, 'Exception')

    def test_raise_no_exception(self):
        method_name = 'tests.unit.stub_sut.Exceptions.raise_distinct_exception'
        func = TestExceptions().test_raise_no_exception

        result = monitor(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        run_lines = calls[0].run_lines
        self.assertEqual(run_lines, [246, 247, 248])

    def test_calls_with_exceptions(self):
        method_name = 'tests.unit.stub_sut.Exceptions.raise_distinct_exception'
        func = TestExceptions().test_calls_with_exceptions

        result = monitor(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 3)

        # Call 1
        run_lines = calls[0].run_lines
        self.assertEqual(run_lines, [246])
        call_state = calls[0].call_state
        exception_state = call_state.exception_state
        self.assertEqual(exception_state.lineno, 246)
        self.assertEqual(exception_state.value, 'Exception')

        # Call 2
        run_lines = calls[1].run_lines
        self.assertEqual(run_lines, [246, 247])
        call_state = calls[1].call_state
        exception_state = call_state.exception_state
        self.assertEqual(exception_state.lineno, 247)
        self.assertEqual(exception_state.value, 'Exception')

        # Call 3
        run_lines = calls[2].run_lines
        self.assertEqual(run_lines, [246, 247, 248])
        call_state = calls[2].call_state
        exception_state = call_state.exception_state
        self.assertEqual(exception_state.lineno, 248)
        self.assertEqual(exception_state.value, 'Exception')


if __name__ == '__main__':
    unittest.main()