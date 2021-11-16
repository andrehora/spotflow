import unittest
from happyflow.tracer import TraceRunner


class TestGenerator(unittest.TestCase):

    def test_no_generator(self):
        target_entity_name = 'tests.stub_sut.Generators.no_generator'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestGenerators.test_no_generator', [target_entity_name])
        self.assertEqual(len(trace_result), 1)

    def test_call_generator_1(self):
        target_entity_name1 = 'tests.stub_sut.Generators.call_generator_1'
        target_entity_name2 = 'tests.stub_sut.Generators.has_generator_1'

        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestGenerators.test_call_generator_1', [target_entity_name1, target_entity_name2])
        self.assertEqual(len(trace_result), 2)

        flows = trace_result[target_entity_name1].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [261, 262])

        flows = trace_result[target_entity_name2].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [277])

        state_result = flows[0].state_result
        self.assertEqual(len(state_result.get_yield_states()), 1)
        self.assertEqual(state_result.yield_states[0].value, 'None')


    def test_call_generator_2(self):
        target_entity_name1 = 'tests.stub_sut.Generators.call_generator_2'
        target_entity_name2 = 'tests.stub_sut.Generators.has_generator_2'

        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestGenerators.test_call_generator_2', [target_entity_name1, target_entity_name2])
        self.assertEqual(len(trace_result), 2)

        flows = trace_result[target_entity_name1].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [265, 266, 267])

        flows = trace_result[target_entity_name2].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [280, 281])

        state_result = flows[0].state_result
        self.assertEqual(len(state_result.get_yield_states()), 2)
        self.assertEqual(state_result.yield_states[0].value, '100')
        self.assertEqual(state_result.yield_states[1].value, '200')


    def test_call_generator_3(self):
        target_entity_name1 = 'tests.stub_sut.Generators.call_generator_3'
        target_entity_name2 = 'tests.stub_sut.Generators.has_generator_3'

        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestGenerators.test_call_generator_3', [target_entity_name1, target_entity_name2])
        self.assertEqual(len(trace_result), 2)

        flows = trace_result[target_entity_name1].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [270, 271, 272, 273, 274])

        flows = trace_result[target_entity_name2].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [284, 285, 286, 284, 285, 286, 284, 285, 286, 287])
        self.assertEqual(flows[0].distinct_lines(), [284, 285, 286, 287])

        print(flows[0].state_result.return_state)

    def test_has_generator_1(self):
        target_entity_name = 'tests.stub_sut.Generators.has_generator_1'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestGenerators.test_has_generator_1', [target_entity_name])
        self.assertEqual(len(trace_result), 1)

        flows = trace_result[target_entity_name].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [])

    def test_has_generator_3(self):
        target_entity_name = 'tests.stub_sut.Generators.has_generator_3'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestGenerators.test_has_generator_3', [target_entity_name])
        self.assertEqual(len(trace_result), 1)

        flows = trace_result[target_entity_name].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [])

    def test_generators_all(self):
        target_entity_name = 'tests.stub_sut.Generators'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestGenerators', [target_entity_name])
        self.assertEqual(len(trace_result), 7)


if __name__ == '__main__':
    unittest.main()