import unittest
from tests.unit.stub_test import TLocalClass
from spotflow.api import monitor_func


class TestLocalClassCall(unittest.TestCase):

    def test_has_local_class_1(self):
        method_name = 'tests.unit.stub_sut.HasLocalClass.LocalClass1.local'
        func = TLocalClass().test_has_local_class_1

        result = monitor_func(func, [method_name])

        self.assertEqual(len(result), 1)

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [531])

    def test_has_local_class_2(self):
        method_name = 'tests.unit.stub_sut'
        func = TLocalClass().test_has_local_class_2

        result = monitor_func(func, [method_name])

        self.assertEqual(len(result), 2)

        calls = result['tests.unit.stub_sut.HasLocalClass.has_local_class'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [535, 539])

        calls = result['tests.unit.stub_sut.HasLocalClass.has_local_class.<locals>.LocalClass2.local'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [537])

    def test_has_local_class_3(self):
        method_name = 'tests.unit.stub_sut'
        func = TLocalClass().test_has_local_class_3

        result = monitor_func(func, [method_name])

        self.assertEqual(len(result), 2)

        calls = result['tests.unit.stub_sut.has_local_class'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [544, 548])

        calls = result['tests.unit.stub_sut.has_local_class.<locals>.LocalClass3.local'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [546])





if __name__ == '__main__':
    unittest.main()
