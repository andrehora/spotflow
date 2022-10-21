import unittest
from tests.unit.stub_test import TestRecursion
from spotflow.api import monitor


class TestRecursiveCalls(unittest.TestCase):

    def test_basic_recursion(self):
        method_name = 'tests.unit.stub_sut.Recursion.basic_recursion'
        func = TestRecursion().test_basic_recursion

        result = monitor(func, [method_name])
        self.assertEqual(len(result), 1)

        calls = result[method_name].calls
        self.assertEqual(len(calls), 3)

        self.assertEqual(calls[0].run_lines, [582, 584])
        self.assertEqual(calls[1].run_lines, [582, 584])
        self.assertEqual(calls[2].run_lines, [582, 583])

    def test_fib_recursive(self):
        method_name = 'tests.unit.stub_sut.Recursion.fib_recursive'
        func = TestRecursion().test_fib_recursive_3

        result = monitor(func, [method_name])
        self.assertEqual(len(result), 2)

        calls = result['tests.unit.stub_sut.Recursion.fib_recursive'].calls
        self.assertEqual(len(calls), 1)

        calls = result['tests.unit.stub_sut.Recursion.fib_recursive.<locals>.fib_recursive_term'].calls
        self.assertEqual(len(calls), 10)


if __name__ == '__main__':
    unittest.main()