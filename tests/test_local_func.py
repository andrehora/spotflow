import unittest
from tests.stub_test import TestInternalMethod
from happyflow.api import run_and_flow_func


class TestLocalMethod(unittest.TestCase):

    def test_has_local_method_1(self):
        target_entity_name = 'tests.stub_sut.LocalMethod.has_local_method_1'
        func = TestInternalMethod().test_has_local_method_1

        result = run_and_flow_func(func, [target_entity_name])

        self.assertEqual(len(result), 1)
        flows = result[target_entity_name].flows
        self.assertEqual(len(flows), 1)

        self.assertEqual(flows[0].run_lines, [333, 334, 336])

    def test_has_local_method_2(self):
        target_entity_name = 'tests.stub_sut.LocalMethod.has_local_method_2'
        func = TestInternalMethod().test_has_local_method_2

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
        func = TestInternalMethod().test_has_local_method_3

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
        func = TestInternalMethod().test_has_local_method_4

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


if __name__ == '__main__':
    unittest.main()
