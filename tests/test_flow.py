import unittest
from happyflow.tracer import TraceRunner


class TestFlowSUTMethod(unittest.TestCase):

    def test_run_simple_if(self):

        target_entity_name = 'tests.stub_sut.SimpleFlow.simple_if'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestSimpleFlow.test_simple_if_true', [target_entity_name])

        self.assertEqual(trace_result[target_entity_name].flows[0].run_lines, [4, 5])
        self.assertEqual(trace_result[target_entity_name].target_entity_name, 'simple_if')

        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestSimpleFlow.test_simple_if_false', [target_entity_name])

        self.assertEqual(trace_result[target_entity_name].flows[0].run_lines, [4])
        self.assertEqual(trace_result[target_entity_name].target_entity_name, 'simple_if')

    def test_run_simple_if_else(self):
        target_entity_name = 'tests.stub_sut.SimpleFlow.simple_if_else'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestSimpleFlow.test_simple_if_else_true_and_false', [target_entity_name])

        self.assertIn([8, 9], trace_result[target_entity_name].flows)
        self.assertIn([8, 11], trace_result[target_entity_name].flows)
        self.assertEqual(trace_result[target_entity_name].target_entity_name, 'simple_if_else')

        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestSimpleFlow.test_simple_if_else_true', [target_entity_name])

        self.assertEqual(trace_result[target_entity_name].flows[0].run_lines, [8, 9])
        self.assertEqual(trace_result[target_entity_name].target_entity_name, 'simple_if_else')

        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestSimpleFlow.test_simple_if_else_false', [target_entity_name])

        self.assertEqual(trace_result[target_entity_name].flows[0].run_lines, [8, 11])
        self.assertEqual(trace_result[target_entity_name].target_entity_name, 'simple_if_else')

        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestSimpleFlow', [target_entity_name])

        self.assertIn([8, 9], trace_result[target_entity_name].flows)
        self.assertIn([8, 11], trace_result[target_entity_name].flows)
        self.assertEqual(trace_result[target_entity_name].target_entity_name, 'simple_if_else')


    def test_run_loop(self):
        target_entity_name = 'tests.stub_sut.SimpleFlow.loop'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestSimpleFlow.test_loop', [target_entity_name])

        self.assertEqual(trace_result[target_entity_name].flows[0].run_lines, [14, 15, 16, 15, 16, 15])
        self.assertEqual(trace_result[target_entity_name].flows[0].distinct_lines(), [14, 15, 16])
        self.assertEqual(trace_result[target_entity_name].target_entity_name, 'loop')

    def test_run_try(self):
        target_entity_name = 'tests.stub_sut.SimpleFlow.try_success'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestSimpleFlow.test_try_success', [target_entity_name])

        self.assertEqual(trace_result[target_entity_name].flows[0].run_lines, [19, 20])
        self.assertEqual(trace_result[target_entity_name].target_entity_name, 'try_success')

    def test_run_try_fail(self):
        target_entity_name = 'tests.stub_sut.SimpleFlow.try_fail'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestSimpleFlow.test_try_fail', [target_entity_name])

        self.assertEqual(trace_result[target_entity_name].flows[0].run_lines, [25, 26, 27, 28])
        self.assertEqual(trace_result[target_entity_name].target_entity_name, 'try_fail')

    def test_single_call_to_sut(self):
        target_entity_name = 'tests.stub_sut.ComplexFlow.hello'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestComplexFlow.test_single_call_to_sut_bom_dia', [target_entity_name])

        self.assertEqual(trace_result[target_entity_name].flows[0].run_lines, [35, 39])
        self.assertEqual(trace_result[target_entity_name].target_entity_name, 'hello')

        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestComplexFlow.test_single_call_to_sut_boa_tarde', [target_entity_name])

        self.assertEqual(trace_result[target_entity_name].flows[0].run_lines, [35, 36, 38])
        self.assertEqual(trace_result[target_entity_name].target_entity_name, 'hello')

        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestComplexFlow.test_single_call_to_sut_boa_noite', [target_entity_name])

        self.assertEqual(trace_result[target_entity_name].flows[0].run_lines, [35, 36, 37])
        self.assertEqual(trace_result[target_entity_name].target_entity_name, 'hello')

    def test_multiple_call_to_sut(self):
        target_entity_name = 'tests.stub_sut.ComplexFlow.hello'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestComplexFlow.test_multiple_call_to_sut', [target_entity_name])

        self.assertEqual(len(trace_result[target_entity_name].flows), 3)

        self.assertIn([35, 39], trace_result[target_entity_name].flows)
        self.assertIn([35, 36, 38], trace_result[target_entity_name].flows)
        self.assertIn([35, 36, 37], trace_result[target_entity_name].flows)
        self.assertEqual(trace_result[target_entity_name].target_entity_name, 'hello')

    def test_sut_call_sut(self):
        target_entity_name = 'tests.stub_sut'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestComplexFlow.test_sut_call_sut', [target_entity_name])

        target_entity_name = 'tests.stub_sut.ComplexFlow.func'
        self.assertEqual(trace_result[target_entity_name].flows[0].run_lines, [42, 43, 44])
        self.assertEqual(trace_result[target_entity_name].target_entity_name, 'func')

        target_entity_name = 'tests.stub_sut.ComplexFlow.f1'
        self.assertEqual(trace_result[target_entity_name].flows[0].run_lines, [47])
        self.assertEqual(trace_result[target_entity_name].target_entity_name, 'f1')

        target_entity_name = 'tests.stub_sut.ComplexFlow.f2'
        self.assertEqual(trace_result[target_entity_name].flows[0].run_lines, [50])
        self.assertEqual(trace_result[target_entity_name].target_entity_name, 'f2')

        target_entity_name = 'tests.stub_sut.ComplexFlow.f3'
        self.assertEqual(trace_result[target_entity_name].flows[0].run_lines, [53])
        self.assertEqual(trace_result[target_entity_name].target_entity_name, 'f3')


class TestFlowSUTContainer(unittest.TestCase):

    def test_sut_class1(self):
        target_entity_name = 'tests.stub_sut.SimpleFlow'
        run_result = TraceRunner.trace_from_tests('tests.stub_test.TestSimpleFlow', [target_entity_name])
        self.assertEqual(len(run_result), 5)

    def test_sut_class2(self):
        target_entity_name = 'tests.stub_sut.ComplexFlow'
        run_result = TraceRunner.trace_from_tests('tests.stub_test.TestComplexFlow', [target_entity_name])
        self.assertEqual(len(run_result), 5)

    def test_sut_module(self):
        target_entity_name = 'tests.stub_sut'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestSimpleFlow', [target_entity_name])
        self.assertTrue(len(trace_result) == 5)


if __name__ == '__main__':
    unittest.main()