import unittest
from tests.unit.stub_test import TestFuncRunner
from spotflow.api import monitor


class TestFuncRunnerCalls(unittest.TestCase):

    def test_run_decorator_once(self):
        method_name = 'tests.unit.stub_sut.FuncRunner'
        func = TestFuncRunner().test_run_decorator_once

        result = monitor(func, [method_name])
        self.assertEqual(len(result), 4)

        calls = result['tests.unit.stub_sut.FuncRunner.decorator'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [554, 556])

        calls = result['tests.unit.stub_sut.FuncRunner.decorator.<locals>.inner'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [555])

        calls = result['tests.unit.stub_sut.FuncRunner.func_to_be_run'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [559])

        calls = result['tests.unit.stub_sut.FuncRunner.run_decorator_once'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [562, 563])

    def test_run_decorator_twice(self):
        method_name = 'tests.unit.stub_sut.FuncRunner'
        func = TestFuncRunner().test_run_decorator_twice

        result = monitor(func, [method_name])
        self.assertEqual(len(result), 4)

        calls = result['tests.unit.stub_sut.FuncRunner.decorator'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [554, 556])

        calls = result['tests.unit.stub_sut.FuncRunner.decorator.<locals>.inner'].calls
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0].run_lines, [555])

        calls = result['tests.unit.stub_sut.FuncRunner.func_to_be_run'].calls
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0].run_lines, [559])

        calls = result['tests.unit.stub_sut.FuncRunner.run_decorator_twice'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [566, 567, 568])

    def test_run_call_func(self):
        method_name = 'tests.unit.stub_sut.FuncRunner'
        func = TestFuncRunner().test_run_call_func

        result = monitor(func, [method_name])
        self.assertEqual(len(result), 3)

        calls = result['tests.unit.stub_sut.FuncRunner.call_func_three_times'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [571, 572, 573])

        calls = result['tests.unit.stub_sut.FuncRunner.func_to_be_run'].calls
        self.assertEqual(len(calls), 3)
        self.assertEqual(calls[0].run_lines, [559])

        calls = result['tests.unit.stub_sut.FuncRunner.run_call_func'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [576])


if __name__ == '__main__':
    unittest.main()