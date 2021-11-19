import unittest
from tests.stub_test import TestGenerators
from happyflow.api import run_and_flow_func


class TestGenerator(unittest.TestCase):

    def test_no_generator(self):
        target_entity_name = 'tests.stub_sut.Generators.no_generator'
        func = TestGenerators().test_no_generator

        result = run_and_flow_func(func, [target_entity_name])

        self.assertEqual(len(result), 1)

    def test_call_generator_1(self):
        target_entity_name1 = 'tests.stub_sut.Generators.call_generator_1'
        target_entity_name2 = 'tests.stub_sut.Generators.has_generator_1'
        func = TestGenerators().test_call_generator_1

        result = run_and_flow_func(func, [target_entity_name1, target_entity_name2])

        self.assertEqual(len(result), 2)

        flows = result[target_entity_name1].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [261, 262])

        flows = result[target_entity_name2].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [277])

        state_history = flows[0].state_history
        self.assertEqual(len(state_history.get_yield_states()), 1)
        self.assertEqual(state_history.yield_states[0].value, 'None')


    def test_call_generator_2(self):
        target_entity_name1 = 'tests.stub_sut.Generators.call_generator_2'
        target_entity_name2 = 'tests.stub_sut.Generators.has_generator_2'
        func = TestGenerators().test_call_generator_2

        result = run_and_flow_func(func, [target_entity_name1, target_entity_name2])

        self.assertEqual(len(result), 2)

        flows = result[target_entity_name1].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [265, 266, 267])

        flows = result[target_entity_name2].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [280, 281])

        state_history = flows[0].state_history
        self.assertEqual(len(state_history.get_yield_states()), 2)
        self.assertEqual(state_history.yield_states[0].value, '100')
        self.assertEqual(state_history.yield_states[1].value, '200')


    def test_call_generator_3(self):
        target_entity_name1 = 'tests.stub_sut.Generators.call_generator_3'
        target_entity_name2 = 'tests.stub_sut.Generators.has_generator_3'
        func = TestGenerators().test_call_generator_3

        result = run_and_flow_func(func, [target_entity_name1, target_entity_name2])

        self.assertEqual(len(result), 2)

        flows = result[target_entity_name1].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [270, 271, 272, 273, 274])

        flows = result[target_entity_name2].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [284, 285, 286, 284, 285, 286, 284, 285, 286, 287])
        self.assertEqual(flows[0].distinct_lines(), [284, 285, 286, 287])

        print(flows[0].state_history.return_state)

    def test_call_generator_4(self):
        target_entity_name1 = 'tests.stub_sut.Generators.call_generator_4'
        target_entity_name2 = 'tests.stub_sut.Generators.has_generator_4'
        func = TestGenerators().test_call_generator_4

        result = run_and_flow_func(func, [target_entity_name1, target_entity_name2])

        self.assertEqual(len(result), 2)

        flows = result[target_entity_name1].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [290, 291, 292])

        flows = result[target_entity_name2].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [295, 296])

        state_history = flows[0].state_history
        self.assertEqual(len(state_history.get_yield_states()), 2)
        self.assertEqual(state_history.yield_states[0].value, '100')
        self.assertEqual(state_history.yield_states[1].value, '200')

    def test_has_generator_1(self):
        target_entity_name = 'tests.stub_sut.Generators.has_generator_1'
        func = TestGenerators().test_has_generator_1

        result = run_and_flow_func(func, [target_entity_name])
        self.assertEqual(len(result), 1)

        flows = result[target_entity_name].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [])

    def test_has_generator_2(self):
        target_entity_name = 'tests.stub_sut.Generators.has_generator_2'
        func = TestGenerators().test_has_generator_2

        result = run_and_flow_func(func, [target_entity_name])
        self.assertEqual(len(result), 1)

        flows = result[target_entity_name].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [])

    def test_has_generator_3(self):
        target_entity_name = 'tests.stub_sut.Generators.has_generator_3'
        func = TestGenerators().test_has_generator_3

        result = run_and_flow_func(func, [target_entity_name])
        self.assertEqual(len(result), 1)

        flows = result[target_entity_name].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [])

    def test_has_generator_4(self):
        target_entity_name = 'tests.stub_sut.Generators.has_generator_4'
        func = TestGenerators().test_has_generator_4

        result = run_and_flow_func(func, [target_entity_name])
        self.assertEqual(len(result), 1)

        flows = result[target_entity_name].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [])

    def test_generators_all(self):
        target_entity_name = 'tests.stub_sut.Generators'
        func = TestGenerators().run_all

        result = run_and_flow_func(func, [target_entity_name])
        self.assertEqual(len(result), 9)


if __name__ == '__main__':
    unittest.main()