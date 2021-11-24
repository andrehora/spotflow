import unittest
from tests.stub_test import TestComprehension
from happyflow.api import run_and_flow_func


class TestComprehensionFlow(unittest.TestCase):

    def test_listcomp_1(self):
        target_entity_name = 'tests.stub_sut.Comprehension.listcomp_1'
        func = TestComprehension().test_listcomp_1

        result = run_and_flow_func(func, [target_entity_name])

        self.assertEqual(len(result), 1)
        flows = result[target_entity_name].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [315, 315, 315, 315, 315, 315, 315, 315, 315, 315, 315])
        self.assertEqual(flows[0].distinct_lines(), [315])

    def test_listcomp_2(self):
        target_entity_name = 'tests.stub_sut.Comprehension.listcomp_2'
        func = TestComprehension().test_listcomp_2

        result = run_and_flow_func(func, [target_entity_name])

        self.assertEqual(len(result), 1)
        flows = result[target_entity_name].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [318, 318, 318, 318, 318, 318, 318, 318, 318, 318, 318])
        self.assertEqual(flows[0].distinct_lines(), [318])

    def test_setcomp_1(self):
        target_entity_name = 'tests.stub_sut.Comprehension.setcomp_1'
        func = TestComprehension().test_setcomp_1

        result = run_and_flow_func(func, [target_entity_name])

        self.assertEqual(len(result), 1)
        flows = result[target_entity_name].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [321, 321, 321, 321, 321, 321, 321, 321, 321, 321, 321])
        self.assertEqual(flows[0].distinct_lines(), [321])

    def test_setcomp_2(self):
        target_entity_name = 'tests.stub_sut.Comprehension.setcomp_2'
        func = TestComprehension().test_setcomp_2

        result = run_and_flow_func(func, [target_entity_name])

        self.assertEqual(len(result), 1)
        flows = result[target_entity_name].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [324, 324, 324, 324, 324, 324, 324, 324, 324, 324, 324])
        self.assertEqual(flows[0].distinct_lines(), [324])

    def test_dictcomp(self):
        target_entity_name = 'tests.stub_sut.Comprehension.dictcomp'
        func = TestComprehension().test_dictcomp

        result = run_and_flow_func(func, [target_entity_name])

        self.assertEqual(len(result), 1)
        flows = result[target_entity_name].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [327, 327, 327, 327, 327, 327, 327, 327, 327, 327, 327])
        self.assertEqual(flows[0].distinct_lines(), [327])


if __name__ == '__main__':
    unittest.main()