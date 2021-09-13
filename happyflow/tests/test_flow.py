import unittest
from happyflow.sut_loader import SUTLoader
from happyflow.tracer import TraceRunner


class TestGlobalFlowSUTMethod(unittest.TestCase):

    def test_run_simple_if(self):
        sut = SUTLoader.find_sut('stub_sut.SimpleFlow.simple_if')

        trace_result = TraceRunner.trace('stub_test.TestSimpleFlow.test_simple_if_true', sut)
        flow_result = sut.global_flows(trace_result)

        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [4, 5])
        self.assertEqual(flow_result.sut_name, 'simple_if')
        self.assertIn('test_simple_if_true', flow_result.test_names)

        trace_result = TraceRunner.trace('stub_test.TestSimpleFlow.test_simple_if_false', sut)
        flow_result = sut.global_flows(trace_result)

        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [4])
        self.assertEqual(flow_result.sut_name, 'simple_if')
        self.assertIn('test_simple_if_false', flow_result.test_names)

    def test_run_simple_if_else(self):
        sut = SUTLoader.find_sut('stub_sut.SimpleFlow.simple_if_else')

        trace_result = TraceRunner.trace('stub_test.TestSimpleFlow.test_simple_if_else_true_and_false', sut)
        flow_result = sut.global_flows(trace_result)

        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [8, 9, 11])
        self.assertEqual(flow_result.sut_name, 'simple_if_else')
        self.assertIn('test_simple_if_else_true_and_false', flow_result.test_names)

        trace_result = TraceRunner.trace('stub_test.TestSimpleFlow.test_simple_if_else_true', sut)
        flow_result = sut.global_flows(trace_result)

        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [8, 9])
        self.assertEqual(flow_result.sut_name, 'simple_if_else')
        self.assertIn('test_simple_if_else_true', flow_result.test_names)

        trace_result = TraceRunner.trace('stub_test.TestSimpleFlow.test_simple_if_else_false', sut)
        flow_result = sut.global_flows(trace_result)

        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [8, 11])
        self.assertEqual(flow_result.sut_name, 'simple_if_else')
        self.assertIn('test_simple_if_else_false', flow_result.test_names)

        trace_result = TraceRunner.trace('stub_test.TestSimpleFlow', sut)
        flow_result = sut.global_flows(trace_result)

        self.assertEqual(flow_result.number_of_tests(), 3)
        self.assertEqual(flow_result.sut_name, 'simple_if_else')
        self.assertIn('test_simple_if_else_true', flow_result.test_names)
        self.assertIn('test_simple_if_else_false', flow_result.test_names)
        self.assertIn('test_simple_if_else_true_and_false', flow_result.test_names)

    def test_run_loop(self):
        sut = SUTLoader.find_sut('stub_sut.SimpleFlow.loop')

        trace_result = TraceRunner.trace('stub_test.TestSimpleFlow.test_loop', sut)
        flow_result = sut.global_flows(trace_result)

        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [14, 15, 16])
        self.assertEqual(flow_result.sut_name, 'loop')
        self.assertIn('test_loop', flow_result.test_names)

    def test_run_try(self):
        sut = SUTLoader.find_sut('stub_sut.SimpleFlow.try_success')

        trace_result = TraceRunner.trace('stub_test.TestSimpleFlow.test_try_success', sut)
        flow_result = sut.global_flows(trace_result)

        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [19, 20])
        self.assertEqual(flow_result.sut_name, 'try_success')
        self.assertIn('test_try_success', flow_result.test_names)

    def test_run_try_fail(self):
        sut = SUTLoader.find_sut('stub_sut.SimpleFlow.try_fail')

        trace_result = TraceRunner.trace('stub_test.TestSimpleFlow.test_try_fail', sut)
        flow_result = sut.global_flows(trace_result)

        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [25, 26, 27, 28])
        self.assertEqual(flow_result.sut_name, 'try_fail')
        self.assertIn('test_try_fail', flow_result.test_names)

    def test_single_call_to_sut(self):
        sut = SUTLoader.find_sut('stub_sut.ComplexFlow.hello')

        trace_result = TraceRunner.trace('stub_test.TestComplexFlow.test_single_call_to_sut_bom_dia', sut)
        flow_result = sut.global_flows(trace_result)

        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [35, 39])
        self.assertEqual(flow_result.sut_name, 'hello')
        self.assertIn('test_single_call_to_sut_bom_dia', flow_result.test_names)

        trace_result = TraceRunner.trace('stub_test.TestComplexFlow.test_single_call_to_sut_boa_tarde', sut)
        flow_result = sut.global_flows(trace_result)

        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [35, 36, 38])
        self.assertEqual(flow_result.sut_name, 'hello')
        self.assertIn('test_single_call_to_sut_boa_tarde', flow_result.test_names)

        trace_result = TraceRunner.trace('stub_test.TestComplexFlow.test_single_call_to_sut_boa_noite', sut)
        flow_result = sut.global_flows(trace_result)

        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [35, 36, 37])
        self.assertEqual(flow_result.sut_name, 'hello')
        self.assertIn('test_single_call_to_sut_boa_noite', flow_result.test_names)

    def test_multiple_call_to_sut(self):
        sut = SUTLoader.find_sut('stub_sut.ComplexFlow.hello')

        trace_result = TraceRunner.trace('stub_test.TestComplexFlow.test_multiple_call_to_sut', sut)
        flow_result = sut.global_flows(trace_result)

        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [35, 36, 37, 38, 39])
        self.assertEqual(flow_result.sut_name, 'hello')
        self.assertIn('test_multiple_call_to_sut', flow_result.test_names)


class TestLocalFlowSUTMethod(unittest.TestCase):

    def test_run_simple_if(self):
        sut = SUTLoader.find_sut('stub_sut.SimpleFlow.simple_if')

        trace_result = TraceRunner.trace('stub_test.TestSimpleFlow.test_simple_if_true', sut)
        flow_result = sut.local_flows(trace_result)

        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [4, 5])
        self.assertEqual(flow_result.sut_name, 'simple_if')
        self.assertIn('test_simple_if_true', flow_result.test_names)

        trace_result = TraceRunner.trace('stub_test.TestSimpleFlow.test_simple_if_false', sut)
        flow_result = sut.local_flows(trace_result)

        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [4])
        self.assertEqual(flow_result.sut_name, 'simple_if')
        self.assertIn('test_simple_if_false', flow_result.test_names)

    def test_run_simple_if_else(self):
        sut = SUTLoader.find_sut('stub_sut.SimpleFlow.simple_if_else')

        trace_result = TraceRunner.trace('stub_test.TestSimpleFlow.test_simple_if_else_true_and_false', sut)
        flow_result = sut.local_flows(trace_result)

        self.assertEqual(flow_result.number_of_tests(), 2)
        self.assertIn([8, 9], flow_result.flows)
        self.assertIn([8, 11], flow_result.flows)
        self.assertEqual(flow_result.sut_name, 'simple_if_else')
        self.assertIn('test_simple_if_else_true_and_false', flow_result.test_names)

        trace_result = TraceRunner.trace('stub_test.TestSimpleFlow.test_simple_if_else_true', sut)
        flow_result = sut.local_flows(trace_result)

        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [8, 9])
        self.assertEqual(flow_result.sut_name, 'simple_if_else')
        self.assertIn('test_simple_if_else_true', flow_result.test_names)

        trace_result = TraceRunner.trace('stub_test.TestSimpleFlow.test_simple_if_else_false', sut)
        flow_result = sut.local_flows(trace_result)

        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [8, 11])
        self.assertEqual(flow_result.sut_name, 'simple_if_else')
        self.assertIn('test_simple_if_else_false', flow_result.test_names)

        trace_result = TraceRunner.trace('stub_test.TestSimpleFlow', sut)
        flow_result = sut.local_flows(trace_result)

        self.assertEqual(flow_result.number_of_tests(), 4)
        self.assertIn([8, 9], flow_result.flows)
        self.assertIn([8, 11], flow_result.flows)
        self.assertEqual(flow_result.sut_name, 'simple_if_else')
        self.assertIn('test_simple_if_else_true', flow_result.test_names)
        self.assertIn('test_simple_if_else_false', flow_result.test_names)
        self.assertIn('test_simple_if_else_true_and_false', flow_result.test_names)

    def test_run_loop(self):
        sut = SUTLoader.find_sut('stub_sut.SimpleFlow.loop')

        trace_result = TraceRunner.trace('stub_test.TestSimpleFlow.test_loop', sut)
        flow_result = sut.local_flows(trace_result)

        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [14, 15, 16, 15, 16, 15])
        self.assertEqual(flow_result.flows[0].distinct_lines(), [14, 15, 16])
        self.assertEqual(flow_result.sut_name, 'loop')
        self.assertIn('test_loop', flow_result.test_names)

    def test_run_try(self):
        sut = SUTLoader.find_sut('stub_sut.SimpleFlow.try_success')

        trace_result = TraceRunner.trace('stub_test.TestSimpleFlow.test_try_success', sut)
        flow_result = sut.local_flows(trace_result)

        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [19, 20])
        self.assertEqual(flow_result.sut_name, 'try_success')
        self.assertIn('test_try_success', flow_result.test_names)

    def test_run_try_fail(self):
        sut = SUTLoader.find_sut('stub_sut.SimpleFlow.try_fail')

        trace_result = TraceRunner.trace('stub_test.TestSimpleFlow.test_try_fail', sut)
        flow_result = sut.local_flows(trace_result)

        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [25, 26, 27, 28])
        self.assertEqual(flow_result.sut_name, 'try_fail')
        self.assertIn('test_try_fail', flow_result.test_names)

    def test_single_call_to_sut(self):
        sut = SUTLoader.find_sut('stub_sut.ComplexFlow.hello')

        trace_result = TraceRunner.trace('stub_test.TestComplexFlow.test_single_call_to_sut_bom_dia', sut)
        flow_result = sut.local_flows(trace_result)

        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [35, 39])
        self.assertEqual(flow_result.sut_name, 'hello')
        self.assertIn('test_single_call_to_sut_bom_dia', flow_result.test_names)

        trace_result = TraceRunner.trace('stub_test.TestComplexFlow.test_single_call_to_sut_boa_tarde', sut)
        flow_result = sut.local_flows(trace_result)

        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [35, 36, 38])
        self.assertEqual(flow_result.sut_name, 'hello')
        self.assertIn('test_single_call_to_sut_boa_tarde', flow_result.test_names)

        trace_result = TraceRunner.trace('stub_test.TestComplexFlow.test_single_call_to_sut_boa_noite', sut)
        flow_result = sut.local_flows(trace_result)

        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [35, 36, 37])
        self.assertEqual(flow_result.sut_name, 'hello')
        self.assertIn('test_single_call_to_sut_boa_noite', flow_result.test_names)

    def test_multiple_call_to_sut(self):
        sut = SUTLoader.find_sut('stub_sut.ComplexFlow.hello')

        trace_result = TraceRunner.trace('stub_test.TestComplexFlow.test_multiple_call_to_sut', sut)
        flow_result = sut.local_flows(trace_result)

        self.assertEqual(flow_result.number_of_tests(), 3)
        self.assertIn([35, 39], flow_result.flows)
        self.assertIn([35, 36, 38], flow_result.flows)
        self.assertIn([35, 36, 37], flow_result.flows)
        self.assertEqual(flow_result.sut_name, 'hello')
        self.assertIn('test_multiple_call_to_sut', flow_result.test_names)

    def test_sut_call_sut(self):
        sut = SUTLoader.find_sut('stub_sut')
        trace_result = TraceRunner.trace('stub_test.TestComplexFlow.test_sut_call_sut', sut)

        sut = SUTLoader.find_sut('stub_sut.ComplexFlow.func')
        flow_result = sut.local_flows(trace_result)

        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [42, 43, 44])
        self.assertEqual(flow_result.sut_name, 'func')
        self.assertIn('test_sut_call_sut', flow_result.test_names)

        sut = SUTLoader.find_sut('stub_sut.ComplexFlow.f1')
        flow_result = sut.local_flows(trace_result)

        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [47])
        self.assertEqual(flow_result.sut_name, 'f1')
        self.assertIn('test_sut_call_sut', flow_result.test_names)

        sut = SUTLoader.find_sut('stub_sut.ComplexFlow.f2')
        flow_result = sut.local_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [50])
        self.assertEqual(flow_result.sut_name, 'f2')
        self.assertIn('test_sut_call_sut', flow_result.test_names)

        sut = SUTLoader.find_sut('stub_sut.ComplexFlow.f3')
        flow_result = sut.local_flows(trace_result)
        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [53])
        self.assertEqual(flow_result.sut_name, 'f3')
        self.assertIn('test_sut_call_sut', flow_result.test_names)


class TestGlobalFlowSUTClass(unittest.TestCase):

    def test_sut_class_SimpleFlow(self):
        sut = SUTLoader.find_sut('stub_sut.SimpleFlow')

        trace_result = TraceRunner.trace('stub_test.TestSimpleFlow', sut)
        flow_result = sut.global_flows(trace_result)

        self.assertEqual(flow_result.number_of_tests(), 8)
        self.assertEqual(len(flow_result.flows), 8)
        self.assertEqual(flow_result.sut_name, 'SimpleFlow')
        self.assertIn('test_simple_if_true', flow_result.test_names)
        self.assertIn('test_simple_if_false', flow_result.test_names)
        self.assertIn('test_simple_if_else_true', flow_result.test_names)
        self.assertIn('test_simple_if_else_false', flow_result.test_names)
        self.assertIn('test_simple_if_else_true_and_false', flow_result.test_names)
        self.assertIn('test_loop', flow_result.test_names)
        self.assertIn('test_try_success', flow_result.test_names)
        self.assertIn('test_try_fail', flow_result.test_names)

    def test_sut_class_ComplexFlow(self):
        sut = SUTLoader.find_sut('stub_sut.ComplexFlow')

        trace_result = TraceRunner.trace('stub_test.TestComplexFlow', sut)
        flow_result = sut.global_flows(trace_result)

        self.assertEqual(flow_result.number_of_tests(), 8)
        self.assertEqual(len(flow_result.flows), 8)
        self.assertEqual(flow_result.sut_name, 'ComplexFlow')
        self.assertIn('test_single_call_to_sut_bom_dia', flow_result.test_names)
        self.assertIn('test_single_call_to_sut_boa_tarde', flow_result.test_names)
        self.assertIn('test_single_call_to_sut_boa_noite', flow_result.test_names)
        self.assertIn('test_multiple_call_to_sut', flow_result.test_names)
        self.assertIn('test_sut_call_sut', flow_result.test_names)


class TestGlobalFlowSUTModule(unittest.TestCase):

    def test_sut_class_SimpleFlow(self):
        sut = SUTLoader.find_sut('stub_sut')

        trace_result = TraceRunner.trace('stub_test.TestSimpleFlow', sut)
        flow_result = sut.global_flows(trace_result)

        self.assertEqual(flow_result.number_of_tests(), 8)
        self.assertEqual(len(flow_result.flows), 8)
        self.assertEqual(flow_result.sut_name, 'stub_sut')
        self.assertIn('test_simple_if_true', flow_result.test_names)
        self.assertIn('test_simple_if_false', flow_result.test_names)
        self.assertIn('test_simple_if_else_true', flow_result.test_names)
        self.assertIn('test_simple_if_else_false', flow_result.test_names)
        self.assertIn('test_simple_if_else_true_and_false', flow_result.test_names)
        self.assertIn('test_loop', flow_result.test_names)
        self.assertIn('test_try_success', flow_result.test_names)
        self.assertIn('test_try_fail', flow_result.test_names)

    def test_sut_class_ComplexFlow(self):
        sut = SUTLoader.find_sut('stub_sut.ComplexFlow')

        trace_result = TraceRunner.trace('stub_test.TestComplexFlow', sut)
        flow_result = sut.global_flows(trace_result)

        self.assertEqual(flow_result.number_of_tests(), 8)
        self.assertEqual(len(flow_result.flows), 8)
        self.assertEqual(flow_result.sut_name, 'ComplexFlow')
        self.assertIn('test_single_call_to_sut_bom_dia', flow_result.test_names)
        self.assertIn('test_single_call_to_sut_boa_tarde', flow_result.test_names)
        self.assertIn('test_single_call_to_sut_boa_noite', flow_result.test_names)
        self.assertIn('test_multiple_call_to_sut', flow_result.test_names)
        self.assertIn('test_sut_call_sut', flow_result.test_names)


class TestLocalFlowSUTClass(unittest.TestCase):

    def test_sut_class_SimpleFlow(self):
        sut = SUTLoader.find_sut('stub_sut.SimpleFlow')

        trace_result = TraceRunner.trace('stub_test.TestSimpleFlow', sut)
        flow_result = sut.local_flows(trace_result)

        self.assertEqual(flow_result.number_of_tests(), 9)
        self.assertEqual(len(flow_result.flows), 9)
        self.assertEqual(flow_result.sut_name, 'SimpleFlow')
        self.assertIn('test_simple_if_true', flow_result.test_names)
        self.assertIn('test_simple_if_false', flow_result.test_names)
        self.assertIn('test_simple_if_else_true', flow_result.test_names)
        self.assertIn('test_simple_if_else_false', flow_result.test_names)
        self.assertIn('test_simple_if_else_true_and_false', flow_result.test_names)
        self.assertIn('test_loop', flow_result.test_names)
        self.assertIn('test_try_success', flow_result.test_names)
        self.assertIn('test_try_fail', flow_result.test_names)

    def test_sut_class_ComplexFlow(self):
        sut = SUTLoader.find_sut('stub_sut.ComplexFlow')

        trace_result = TraceRunner.trace('stub_test.TestComplexFlow', sut)
        flow_result = sut.local_flows(trace_result)

        self.assertEqual(flow_result.number_of_tests(), 10)
        self.assertEqual(len(flow_result.flows), 10)
        self.assertEqual(flow_result.sut_name, 'ComplexFlow')
        self.assertIn('test_single_call_to_sut_bom_dia', flow_result.test_names)
        self.assertIn('test_single_call_to_sut_boa_tarde', flow_result.test_names)
        self.assertIn('test_single_call_to_sut_boa_noite', flow_result.test_names)
        self.assertIn('test_multiple_call_to_sut', flow_result.test_names)
        self.assertIn('test_sut_call_sut', flow_result.test_names)


class TestLocalFlowSUTModule(unittest.TestCase):

    def test_sut_class_SimpleFlow(self):
        sut = SUTLoader.find_sut('stub_sut')

        trace_result = TraceRunner.trace('stub_test.TestSimpleFlow', sut)
        flow_result = sut.local_flows(trace_result)

        self.assertEqual(flow_result.number_of_tests(), 9)
        self.assertEqual(len(flow_result.flows), 9)
        self.assertEqual(flow_result.sut_name, 'stub_sut')
        self.assertIn('test_simple_if_true', flow_result.test_names)
        self.assertIn('test_simple_if_false', flow_result.test_names)
        self.assertIn('test_simple_if_else_true', flow_result.test_names)
        self.assertIn('test_simple_if_else_false', flow_result.test_names)
        self.assertIn('test_simple_if_else_true_and_false', flow_result.test_names)
        self.assertIn('test_loop', flow_result.test_names)
        self.assertIn('test_try_success', flow_result.test_names)
        self.assertIn('test_try_fail', flow_result.test_names)

    def test_sut_class_ComplexFlow(self):
        sut = SUTLoader.find_sut('stub_sut')

        trace_result = TraceRunner.trace('stub_test.TestComplexFlow', sut)
        flow_result = sut.local_flows(trace_result)

        self.assertEqual(flow_result.number_of_tests(), 10)
        self.assertEqual(len(flow_result.flows), 10)
        self.assertEqual(flow_result.sut_name, 'stub_sut')
        self.assertIn('test_single_call_to_sut_bom_dia', flow_result.test_names)
        self.assertIn('test_single_call_to_sut_boa_tarde', flow_result.test_names)
        self.assertIn('test_single_call_to_sut_boa_noite', flow_result.test_names)
        self.assertIn('test_multiple_call_to_sut', flow_result.test_names)
        self.assertIn('test_sut_call_sut', flow_result.test_names)

