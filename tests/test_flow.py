import unittest
from happyflow.target_loader import TargetEntityLoader
from happyflow.tracer import TraceRunner


class TestLocalFlowSUTMethod(unittest.TestCase):

    def test_run_simple_if(self):
        sut = TargetEntityLoader.find('stub_sut.SimpleFlow.simple_if', '.', 'stub_sut')

        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestSimpleFlow.test_simple_if_true', sut)
        flow_result = sut.local_flows(trace_result)[0]

        self.assertEqual(flow_result.flows[0].run_lines, [4, 5])
        self.assertEqual(flow_result.target_entity_name, 'simple_if')

        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestSimpleFlow.test_simple_if_false', sut)
        flow_result = sut.local_flows(trace_result)[0]

        self.assertEqual(flow_result.flows[0].run_lines, [4])
        self.assertEqual(flow_result.target_entity_name, 'simple_if')

    def test_run_simple_if_else(self):
        sut = TargetEntityLoader.find('stub_sut.SimpleFlow.simple_if_else', '.', 'stub_sut')

        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestSimpleFlow.test_simple_if_else_true_and_false', sut)
        flow_result = sut.local_flows(trace_result)[0]

        self.assertIn([8, 9], flow_result.flows)
        self.assertIn([8, 11], flow_result.flows)
        self.assertEqual(flow_result.target_entity_name, 'simple_if_else')

        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestSimpleFlow.test_simple_if_else_true', sut)
        flow_result = sut.local_flows(trace_result)[0]

        self.assertEqual(flow_result.flows[0].run_lines, [8, 9])
        self.assertEqual(flow_result.target_entity_name, 'simple_if_else')

        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestSimpleFlow.test_simple_if_else_false', sut)
        flow_result = sut.local_flows(trace_result)[0]

        self.assertEqual(flow_result.flows[0].run_lines, [8, 11])
        self.assertEqual(flow_result.target_entity_name, 'simple_if_else')

        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestSimpleFlow', sut)
        flow_result = sut.local_flows(trace_result)[0]

        self.assertIn([8, 9], flow_result.flows)
        self.assertIn([8, 11], flow_result.flows)
        self.assertEqual(flow_result.target_entity_name, 'simple_if_else')


    def test_run_loop(self):
        sut = TargetEntityLoader.find('stub_sut.SimpleFlow.loop', '.', 'stub_sut')

        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestSimpleFlow.test_loop', sut)
        flow_result = sut.local_flows(trace_result)[0]

        self.assertEqual(flow_result.flows[0].run_lines, [14, 15, 16, 15, 16, 15])
        self.assertEqual(flow_result.flows[0].distinct_lines(), [14, 15, 16])
        self.assertEqual(flow_result.target_entity_name, 'loop')

    def test_run_try(self):
        sut = TargetEntityLoader.find('stub_sut.SimpleFlow.try_success', '.', 'stub_sut')

        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestSimpleFlow.test_try_success', sut)
        flow_result = sut.local_flows(trace_result)[0]

        self.assertEqual(flow_result.flows[0].run_lines, [19, 20])
        self.assertEqual(flow_result.target_entity_name, 'try_success')

    def test_run_try_fail(self):
        sut = TargetEntityLoader.find('stub_sut.SimpleFlow.try_fail', '.', 'stub_sut')

        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestSimpleFlow.test_try_fail', sut)
        flow_result = sut.local_flows(trace_result)[0]

        self.assertEqual(flow_result.flows[0].run_lines, [25, 26, 27, 28])
        self.assertEqual(flow_result.target_entity_name, 'try_fail')

    def test_single_call_to_sut(self):
        sut = TargetEntityLoader.find('stub_sut.ComplexFlow.hello', '.', 'stub_sut')

        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestComplexFlow.test_single_call_to_sut_bom_dia', sut)
        flow_result = sut.local_flows(trace_result)[0]

        self.assertEqual(flow_result.flows[0].run_lines, [35, 39])
        self.assertEqual(flow_result.target_entity_name, 'hello')

        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestComplexFlow.test_single_call_to_sut_boa_tarde', sut)
        flow_result = sut.local_flows(trace_result)[0]

        self.assertEqual(flow_result.flows[0].run_lines, [35, 36, 38])
        self.assertEqual(flow_result.target_entity_name, 'hello')

        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestComplexFlow.test_single_call_to_sut_boa_noite', sut)
        flow_result = sut.local_flows(trace_result)[0]

        self.assertEqual(flow_result.flows[0].run_lines, [35, 36, 37])
        self.assertEqual(flow_result.target_entity_name, 'hello')

    def test_multiple_call_to_sut(self):
        sut = TargetEntityLoader.find('stub_sut.ComplexFlow.hello', '.', 'stub_sut')

        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestComplexFlow.test_multiple_call_to_sut', sut)
        flow_result = sut.local_flows(trace_result)[0]

        self.assertIn([35, 39], flow_result.flows)
        self.assertIn([35, 36, 38], flow_result.flows)
        self.assertIn([35, 36, 37], flow_result.flows)
        self.assertEqual(flow_result.target_entity_name, 'hello')

    def test_sut_call_sut(self):
        sut = TargetEntityLoader.find('stub_sut', '.', 'stub_sut')
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestComplexFlow.test_sut_call_sut', sut)

        sut = TargetEntityLoader.find('stub_sut.ComplexFlow.func', '.', 'stub_sut')
        flow_result = sut.local_flows(trace_result)[0]

        self.assertEqual(flow_result.flows[0].run_lines, [42, 43, 44])
        self.assertEqual(flow_result.target_entity_name, 'func')

        sut = TargetEntityLoader.find('stub_sut.ComplexFlow.f1', '.', 'stub_sut')
        flow_result = sut.local_flows(trace_result)[0]

        self.assertEqual(flow_result.flows[0].run_lines, [47])
        self.assertEqual(flow_result.target_entity_name, 'f1')

        sut = TargetEntityLoader.find('stub_sut.ComplexFlow.f2', '.', 'stub_sut')
        flow_result = sut.local_flows(trace_result)[0]
        self.assertEqual(flow_result.flows[0].run_lines, [50])
        self.assertEqual(flow_result.target_entity_name, 'f2')

        sut = TargetEntityLoader.find('stub_sut.ComplexFlow.f3', '.', 'stub_sut')
        flow_result = sut.local_flows(trace_result)[0]
        self.assertEqual(flow_result.flows[0].run_lines, [53])
        self.assertEqual(flow_result.target_entity_name, 'f3')


class TestLocalFlowSUTContainer(unittest.TestCase):

    def test_sut_class1(self):
        sut = TargetEntityLoader.find('stub_sut.SimpleFlow', '.', 'stub_sut')
        run_result = TraceRunner.trace_from_tests('tests.stub_test.TestSimpleFlow', sut)
        for each in run_result:
            print(each)
        self.assertEqual(len(run_result), 5)

    def test_sut_class2(self):
        sut = TargetEntityLoader.find('stub_sut.ComplexFlow', '.', 'stub_sut')

        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestComplexFlow', sut)
        flow_result = sut.local_flows(trace_result)

        self.assertEqual(len(flow_result), 5)

    def test_sut_module(self):
        sut = TargetEntityLoader.find('stub_sut', '.', 'stub_sut')

        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestSimpleFlow', sut)
        flow_result = sut.local_flows(trace_result)

        self.assertTrue(len(flow_result) > 45)


if __name__ == '__main__':
    unittest.main()