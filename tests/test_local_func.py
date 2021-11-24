import unittest
from tests.stub_test import TestLocalMethod, TestLocalFunction
from happyflow.api import run_and_flow_func


class TestLocalMethodFlow(unittest.TestCase):

    def test_has_local_method_1(self):
        target_entity_name = 'tests.stub_sut.LocalMethod.has_local_method_1'
        func = TestLocalMethod().test_has_local_method_1

        result = run_and_flow_func(func, [target_entity_name])

        self.assertEqual(len(result), 1)
        flows = result[target_entity_name].flows
        self.assertEqual(len(flows), 1)

        self.assertEqual(flows[0].run_lines, [333, 334, 336])

    def test_has_local_method_2(self):
        target_entity_name = 'tests.stub_sut.LocalMethod.has_local_method_2'
        func = TestLocalMethod().test_has_local_method_2

        result = run_and_flow_func(func, [target_entity_name])
        self.assertEqual(len(result), 2)

        flows = result['tests.stub_sut.LocalMethod.has_local_method_2'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [340, 341, 343, 346, 347])

        flows = result['tests.stub_sut.LocalMethod.has_local_method_2.<locals>.local_method'].flows
        self.assertEqual(len(flows), 2)
        self.assertEqual(flows[0].run_lines, [344])
        self.assertEqual(flows[1].run_lines, [344])

    def test_has_local_method_3(self):
        target_entity_name = 'tests.stub_sut.LocalMethod.has_local_method_3'
        func = TestLocalMethod().test_has_local_method_3

        result = run_and_flow_func(func, [target_entity_name])
        self.assertEqual(len(result), 3)

        flows = result['tests.stub_sut.LocalMethod.has_local_method_3'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [350, 351, 353, 356, 359, 360])

        flows = result['tests.stub_sut.LocalMethod.has_local_method_3.<locals>.local_method_1'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [354])

        flows = result['tests.stub_sut.LocalMethod.has_local_method_3.<locals>.local_method_2'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [357])

    def test_has_local_method_4(self):
        target_entity_name = 'tests.stub_sut.LocalMethod.has_local_method_4'
        func = TestLocalMethod().test_has_local_method_4

        result = run_and_flow_func(func, [target_entity_name])
        self.assertEqual(len(result), 3)

        flows = result['tests.stub_sut.LocalMethod.has_local_method_4'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [363, 364, 366, 374])

        flows = result['tests.stub_sut.LocalMethod.has_local_method_4.<locals>.local_method_1'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [368, 371, 372])

        # Very nested case
        flows = result['tests.stub_sut.LocalMethod.has_local_method_4.<locals>.local_method_1.<locals>.local_method_2'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [369])


class TestLocalFunctionFlow(unittest.TestCase):

    def test_has_local_method_1(self):
        target_entity_name = 'tests.stub_sut.has_local_function_1'
        func = TestLocalFunction().test_has_local_function_1

        result = run_and_flow_func(func, [target_entity_name])

        self.assertEqual(len(result), 1)
        flows = result[target_entity_name].flows
        self.assertEqual(len(flows), 1)

        self.assertEqual(flows[0].run_lines, [378, 379, 381])

    def test_has_local_function_2(self):
        target_entity_name = 'tests.stub_sut.has_local_function_2'
        func = TestLocalFunction().test_has_local_function_2

        result = run_and_flow_func(func, [target_entity_name])
        self.assertEqual(len(result), 2)

        flows = result['tests.stub_sut.has_local_function_2'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [386, 387, 389, 392, 393])

        flows = result['tests.stub_sut.has_local_function_2.<locals>.local_function'].flows
        self.assertEqual(len(flows), 2)
        self.assertEqual(flows[0].run_lines, [390])
        self.assertEqual(flows[1].run_lines, [390])

    def test_has_local_function_3(self):
        target_entity_name = 'tests.stub_sut.has_local_function_3'
        func = TestLocalFunction().test_has_local_function_3

        result = run_and_flow_func(func, [target_entity_name])
        self.assertEqual(len(result), 3)

        flows = result['tests.stub_sut.has_local_function_3'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [397, 398, 400, 403, 406, 407])

        flows = result['tests.stub_sut.has_local_function_3.<locals>.local_function_1'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [401])

        flows = result['tests.stub_sut.has_local_function_3.<locals>.local_function_2'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [404])

    def test_has_local_function_4(self):
        target_entity_name = 'tests.stub_sut.has_local_function_4'
        func = TestLocalFunction().test_has_local_function_4

        result = run_and_flow_func(func, [target_entity_name])
        self.assertEqual(len(result), 3)

        flows = result['tests.stub_sut.has_local_function_4'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [411, 412, 414, 422])

        flows = result['tests.stub_sut.has_local_function_4.<locals>.local_function_1'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [416, 419, 420])

        # Very nested case
        flows = result['tests.stub_sut.has_local_function_4.<locals>.local_function_1.<locals>.local_function_2'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [417])


if __name__ == '__main__':
    unittest.main()
