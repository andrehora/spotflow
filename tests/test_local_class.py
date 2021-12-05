import unittest
from tests.stub_test import TestLocalClass
from happyflow.api import run_and_flow_func


class TestLocalClassFlow(unittest.TestCase):

    def test_has_local_class_1(self):
        target_method_name = 'tests.stub_sut.HasLocalClass.LocalClass1.local'
        func = TestLocalClass().test_has_local_class_1

        result = run_and_flow_func(func, [target_method_name])

        self.assertEqual(len(result), 1)

        flows = result[target_method_name].calls
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [531])

    def test_has_local_class_2(self):
        target_method_name = 'tests.stub_sut'
        func = TestLocalClass().test_has_local_class_2

        result = run_and_flow_func(func, [target_method_name])

        self.assertEqual(len(result), 2)

        flows = result['tests.stub_sut.HasLocalClass.has_local_class'].calls
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [535, 539])

        flows = result['tests.stub_sut.HasLocalClass.has_local_class.<locals>.LocalClass2.local'].calls
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [537])

    def test_has_local_class_3(self):
        target_method_name = 'tests.stub_sut'
        func = TestLocalClass().test_has_local_class_3

        result = run_and_flow_func(func, [target_method_name])

        self.assertEqual(len(result), 2)

        flows = result['tests.stub_sut.has_local_class'].calls
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [544, 548])

        flows = result['tests.stub_sut.has_local_class.<locals>.LocalClass3.local'].calls
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [546])





if __name__ == '__main__':
    unittest.main()
