import unittest
from happyflow.tracer import TraceRunner


@unittest.skip
class TestGenerator(unittest.TestCase):

    def test_no_generator1(self):
        target_entity_name = 'tests.stub_sut.Generators.no_generator_1'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestGenerators.test_no_generator_1', [target_entity_name])
        self.assertEqual(len(trace_result), 1)

    def test_no_generator2(self):
        target_entity_name = 'tests.stub_sut.Generators.no_generator_2'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestGenerators.test_no_generator_2', [target_entity_name])
        self.assertEqual(len(trace_result), 1)

    def test_no_generator3(self):
        target_entity_name = 'tests.stub_sut.Generators.no_generator_3'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestGenerators.test_no_generator_3', [target_entity_name])
        self.assertEqual(len(trace_result), 1)

    def test_has_generator_1(self):
        target_entity_name = 'tests.stub_sut.Generators.has_generator_1'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestGenerators.test_has_generator_1', [target_entity_name])
        self.assertEqual(len(trace_result), 0)

    def test_has_generator_2(self):
        target_entity_name = 'tests.stub_sut.Generators.has_generator_2'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestGenerators.test_has_generator_2', [target_entity_name])
        self.assertEqual(len(trace_result), 0)

    def test_generators_all(self):
        target_entity_name = 'tests.stub_sut.Generators'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestGenerators', [target_entity_name])
        self.assertEqual(len(trace_result), 3)


if __name__ == '__main__':
    unittest.main()