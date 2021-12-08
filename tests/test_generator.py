import unittest
from tests.stub_test import TestGenerator, TestGeneratorExpression
from happyflow.api import run_and_flow_func


class TestGeneratorFlow(unittest.TestCase):

    def test_no_generator(self):
        method_name = 'tests.stub_sut.Generators.no_generator'
        func = TestGenerator().test_no_generator

        result = run_and_flow_func(func, [method_name])

        self.assertEqual(len(result), 1)

    def test_call_generator_1(self):
        method_name1 = 'tests.stub_sut.Generators.call_generator_1'
        method_name2 = 'tests.stub_sut.Generators.has_generator_1'
        func = TestGenerator().test_call_generator_1

        result = run_and_flow_func(func, [method_name1, method_name2])

        self.assertEqual(len(result), 2)

        flows = result[method_name1].calls
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [261, 262])

        flows = result[method_name2].calls
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [277])

        call_state = flows[0].call_state
        self.assertEqual(len(call_state.get_yield_states()), 1)
        self.assertEqual(call_state.yield_states[0].value, 'None')


    def test_call_generator_2(self):
        method_name1 = 'tests.stub_sut.Generators.call_generator_2'
        method_name2 = 'tests.stub_sut.Generators.has_generator_2'
        func = TestGenerator().test_call_generator_2

        result = run_and_flow_func(func, [method_name1, method_name2])

        self.assertEqual(len(result), 2)

        flows = result[method_name1].calls
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [265, 266, 267])

        flows = result[method_name2].calls
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [280, 281])

        call_state = flows[0].call_state
        self.assertEqual(len(call_state.get_yield_states()), 2)
        self.assertEqual(call_state.yield_states[0].value, '100')
        self.assertEqual(call_state.yield_states[1].value, '200')


    def test_call_generator_3(self):
        method_name1 = 'tests.stub_sut.Generators.call_generator_3'
        method_name2 = 'tests.stub_sut.Generators.has_generator_3'
        func = TestGenerator().test_call_generator_3

        result = run_and_flow_func(func, [method_name1, method_name2])

        self.assertEqual(len(result), 2)

        flows = result[method_name1].calls
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [270, 271, 272, 273, 274])

        flows = result[method_name2].calls
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [284, 285, 286, 284, 285, 286, 284, 285, 286, 287])
        self.assertEqual(flows[0].distinct_run_lines(), [284, 285, 286, 287])

    def test_call_generator_4(self):
        method_name1 = 'tests.stub_sut.Generators.call_generator_4'
        method_name2 = 'tests.stub_sut.Generators.has_generator_4'
        func = TestGenerator().test_call_generator_4

        result = run_and_flow_func(func, [method_name1, method_name2])

        self.assertEqual(len(result), 2)

        flows = result[method_name1].calls
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [290, 291, 292])

        flows = result[method_name2].calls
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [295, 296])

        call_state = flows[0].call_state
        self.assertEqual(len(call_state.get_yield_states()), 2)
        self.assertEqual(call_state.yield_states[0].value, '100')
        self.assertEqual(call_state.yield_states[1].value, '200')

    def test_has_generator_1(self):
        method_name = 'tests.stub_sut.Generators.has_generator_1'
        func = TestGenerator().test_has_generator_1

        result = run_and_flow_func(func, [method_name])
        self.assertEqual(len(result), 1)

        flows = result[method_name].calls
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [])

    def test_has_generator_2(self):
        method_name = 'tests.stub_sut.Generators.has_generator_2'
        func = TestGenerator().test_has_generator_2

        result = run_and_flow_func(func, [method_name])
        self.assertEqual(len(result), 1)

        flows = result[method_name].calls
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [])

    def test_has_generator_3(self):
        method_name = 'tests.stub_sut.Generators.has_generator_3'
        func = TestGenerator().test_has_generator_3

        result = run_and_flow_func(func, [method_name])
        self.assertEqual(len(result), 1)

        flows = result[method_name].calls
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [])

    def test_has_generator_4(self):
        method_name = 'tests.stub_sut.Generators.has_generator_4'
        func = TestGenerator().test_has_generator_4

        result = run_and_flow_func(func, [method_name])
        self.assertEqual(len(result), 1)

        flows = result[method_name].calls
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [])

    def test_generators_all(self):
        method_name = 'tests.stub_sut.Generators'
        func = TestGenerator().run_all

        result = run_and_flow_func(func, [method_name])
        self.assertEqual(len(result), 9)


class TestGeneratorExpressionFlow(unittest.TestCase):

    def test_generator_expression_1(self):
        method_name = 'tests.stub_sut.GeneratorExpression.generator_expression_1'
        func = TestGeneratorExpression().test_generator_expression_1

        result = run_and_flow_func(func, [method_name])

        self.assertEqual(len(result), 1)
        flows = result[method_name].calls
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [303])

    def test_generator_expression_2(self):
        method_name = 'tests.stub_sut.GeneratorExpression.generator_expression_2'
        func = TestGeneratorExpression().test_generator_expression_2

        result = run_and_flow_func(func, [method_name])

        self.assertEqual(len(result), 1)
        flows = result[method_name].calls
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [306, 307, 306, 308, 306, 309, 306])
        self.assertEqual(flows[0].distinct_run_lines(), [306, 307, 308, 309])


if __name__ == '__main__':
    unittest.main()