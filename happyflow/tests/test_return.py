import unittest
from happyflow.sut_loader import SUTLoader
from happyflow.tracer import TraceRunner


class TestReturnValue(unittest.TestCase):

    def test_change_var_state(self):
        sut = SUTLoader.find_sut('stub_sut.ReturnValue.simple_return')

        trace_result = TraceRunner.trace('stub_test.TestReturnValue.test_simple_return', sut)
        flow_result = sut.local_flows(trace_result)

        self.assertEqual(flow_result.number_of_tests(), 1)
        self.assertEqual(flow_result.flows[0].run_lines, [59, 60, 61])
        self.assertEqual(flow_result.sut_name, 'change_var_state')
        self.assertIn('test_change_var_state', flow_result.test_names)

        state_result = flow_result.flows[0].state_result
        a = state_result.vars['a'].states
        self.assertEqual(a[0].value, 1)
        self.assertEqual(a[1].value, 2)
        self.assertEqual(a[2].value, 3)

        seq_values = state_result.vars['a'].distinct_sequential_values()
        self.assertEqual(seq_values, [1, 2, 3])


