import unittest
from tests.stub_test import TestSimpleFlow, TestComplexFlow
from happyflow.api import run_and_flow_func


class TestFlowForFunctions(unittest.TestCase):

    def test_simple_if_true(self):
        target_entity_name = 'tests.stub_sut.SimpleFlow.simple_if'
        func = TestSimpleFlow().test_simple_if_true

        result = run_and_flow_func(func, [target_entity_name])

        self.assertEqual(result[target_entity_name].flows[0].run_lines, [4, 5])
        self.assertEqual(result[target_entity_name].target_entity_name, 'simple_if')

    def test_simple_if_false(self):
        target_entity_name = 'tests.stub_sut.SimpleFlow.simple_if'
        func = TestSimpleFlow().test_simple_if_false

        result = run_and_flow_func(func, [target_entity_name])

        self.assertEqual(result[target_entity_name].flows[0].run_lines, [4])
        self.assertEqual(result[target_entity_name].target_entity_name, 'simple_if')

    def test_simple_if_else_true_and_false(self):
        target_entity_name = 'tests.stub_sut.SimpleFlow.simple_if_else'
        func = TestSimpleFlow().test_simple_if_else_true_and_false

        result = run_and_flow_func(func, [target_entity_name])

        self.assertIn([8, 9], result[target_entity_name].flows)
        self.assertIn([8, 11], result[target_entity_name].flows)
        self.assertEqual(result[target_entity_name].target_entity_name, 'simple_if_else')

    def test_simple_if_else_true(self):
        target_entity_name = 'tests.stub_sut.SimpleFlow.simple_if_else'
        func = TestSimpleFlow().test_simple_if_else_true

        result = run_and_flow_func(func, [target_entity_name])

        self.assertEqual(result[target_entity_name].flows[0].run_lines, [8, 9])
        self.assertEqual(result[target_entity_name].target_entity_name, 'simple_if_else')

    def test_simple_if_else_false(self):
        target_entity_name = 'tests.stub_sut.SimpleFlow.simple_if_else'
        func = TestSimpleFlow().test_simple_if_else_false

        result = run_and_flow_func(func, [target_entity_name])

        self.assertEqual(result[target_entity_name].flows[0].run_lines, [8, 11])
        self.assertEqual(result[target_entity_name].target_entity_name, 'simple_if_else')

    def test_TestSimpleFlow(self):
        target_entity_name = 'tests.stub_sut.SimpleFlow.simple_if_else'
        func = TestSimpleFlow().test_simple_if_else_true_and_false

        result = run_and_flow_func(func, [target_entity_name])

        self.assertIn([8, 9], result[target_entity_name].flows)
        self.assertIn([8, 11], result[target_entity_name].flows)
        self.assertEqual(result[target_entity_name].target_entity_name, 'simple_if_else')

    def test_loop(self):
        target_entity_name = 'tests.stub_sut.SimpleFlow.loop'
        func = TestSimpleFlow().test_loop

        result = run_and_flow_func(func, [target_entity_name])

        self.assertEqual(result[target_entity_name].flows[0].run_lines, [14, 15, 16, 15, 16, 15])
        self.assertEqual(result[target_entity_name].flows[0].distinct_lines(), [14, 15, 16])
        self.assertEqual(result[target_entity_name].target_entity_name, 'loop')

    def test_try_success(self):
        target_entity_name = 'tests.stub_sut.SimpleFlow.try_success'
        func = TestSimpleFlow().test_try_success

        result = run_and_flow_func(func, [target_entity_name])

        self.assertEqual(result[target_entity_name].flows[0].run_lines, [19, 20])
        self.assertEqual(result[target_entity_name].target_entity_name, 'try_success')

    def test_try_fail(self):
        target_entity_name = 'tests.stub_sut.SimpleFlow.try_fail'
        func = TestSimpleFlow().test_try_fail

        result = run_and_flow_func(func, [target_entity_name])

        self.assertEqual(result[target_entity_name].flows[0].run_lines, [25, 26, 27, 28])
        self.assertEqual(result[target_entity_name].target_entity_name, 'try_fail')

    def test_single_call_to_sut_bom_dia(self):
        target_entity_name = 'tests.stub_sut.ComplexFlow.hello'
        func = TestComplexFlow().test_single_call_to_sut_bom_dia

        result = run_and_flow_func(func, [target_entity_name])

        self.assertEqual(result[target_entity_name].flows[0].run_lines, [35, 39])
        self.assertEqual(result[target_entity_name].target_entity_name, 'hello')

    def test_single_call_to_sut_boa_tarde(self):
        target_entity_name = 'tests.stub_sut.ComplexFlow.hello'
        func = TestComplexFlow().test_single_call_to_sut_boa_tarde

        result = run_and_flow_func(func, [target_entity_name])

        self.assertEqual(result[target_entity_name].flows[0].run_lines, [35, 36, 38])
        self.assertEqual(result[target_entity_name].target_entity_name, 'hello')

    def test_single_call_to_sut_boa_noite(self):
        target_entity_name = 'tests.stub_sut.ComplexFlow.hello'
        func = TestComplexFlow().test_single_call_to_sut_boa_noite

        result = run_and_flow_func(func, [target_entity_name])

        self.assertEqual(result[target_entity_name].flows[0].run_lines, [35, 36, 37])
        self.assertEqual(result[target_entity_name].target_entity_name, 'hello')

    def test_multiple_call_to_sut(self):
        target_entity_name = 'tests.stub_sut.ComplexFlow.hello'
        func = TestComplexFlow().test_multiple_call_to_sut

        result = run_and_flow_func(func, [target_entity_name])

        self.assertEqual(len(result[target_entity_name].flows), 3)
        self.assertIn([35, 39], result[target_entity_name].flows)
        self.assertIn([35, 36, 38], result[target_entity_name].flows)
        self.assertIn([35, 36, 37], result[target_entity_name].flows)
        self.assertEqual(result[target_entity_name].target_entity_name, 'hello')


class TestFlowForContainers(unittest.TestCase):

    def test_TestSimpleFlow(self):
        target_entity_name = 'tests.stub_sut.SimpleFlow'
        func = TestSimpleFlow().run_all

        result = run_and_flow_func(func, [target_entity_name])

        self.assertEqual(len(result), 5)

        target_entity_name = 'tests.stub_sut'
        func = TestSimpleFlow().run_all

        result = run_and_flow_func(func, [target_entity_name])

        self.assertEqual(len(result), 5)

    def test_TestComplexFlow(self):
        target_entity_name = 'tests.stub_sut.ComplexFlow'
        func = TestComplexFlow().run_all

        result = run_and_flow_func(func, [target_entity_name])

        self.assertEqual(len(result), 5)

        target_entity_name = 'tests.stub_sut'
        func = TestComplexFlow().run_all

        result = run_and_flow_func(func, [target_entity_name])

        self.assertEqual(len(result), 5)

    def test_sut_call_sut(self):
        target_entity_name = 'tests.stub_sut'
        func = TestComplexFlow().test_sut_call_sut

        result = run_and_flow_func(func, [target_entity_name])

        target_entity_name = 'tests.stub_sut.ComplexFlow.func'
        self.assertEqual(result[target_entity_name].flows[0].run_lines, [42, 43, 44])
        self.assertEqual(result[target_entity_name].target_entity_name, 'func')

        target_entity_name = 'tests.stub_sut.ComplexFlow.f1'
        self.assertEqual(result[target_entity_name].flows[0].run_lines, [47])
        self.assertEqual(result[target_entity_name].target_entity_name, 'f1')

        target_entity_name = 'tests.stub_sut.ComplexFlow.f2'
        self.assertEqual(result[target_entity_name].flows[0].run_lines, [50])
        self.assertEqual(result[target_entity_name].target_entity_name, 'f2')

        target_entity_name = 'tests.stub_sut.ComplexFlow.f3'
        self.assertEqual(result[target_entity_name].flows[0].run_lines, [53])
        self.assertEqual(result[target_entity_name].target_entity_name, 'f3')


if __name__ == '__main__':
    unittest.main()