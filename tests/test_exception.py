import unittest
from happyflow.target_loader import TargetEntityLoader
from happyflow.tracer import TraceRunner


class TestException(unittest.TestCase):

    def test_zero_division(self):
        sut = TargetEntityLoader.find('stub_sut.Exceptions.zero_division', '.', 'stub_sut')

        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestExceptions.test_zero_division', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result[0].flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result
        exception_state = state_result.exception_state
        self.assertEqual(exception_state.line, 237)
        self.assertEqual(exception_state.value[0], ZeroDivisionError)

    def test_raise_generic_exception(self):
        sut = TargetEntityLoader.find('stub_sut.Exceptions.raise_generic_exception', '.', 'stub_sut')

        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestExceptions.test_raise_generic_exception', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result[0].flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result
        exception_state = state_result.exception_state
        self.assertEqual(exception_state.line, 240)
        self.assertEqual(exception_state.value[0], Exception)

    def test_raise_specific_exception(self):
        sut = TargetEntityLoader.find('stub_sut.Exceptions.raise_specific_exception', '.', 'stub_sut')

        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestExceptions.test_raise_specific_exception', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result[0].flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result
        exception_state = state_result.exception_state
        self.assertEqual(exception_state.line, 243)
        self.assertEqual(exception_state.value[0], TypeError)


if __name__ == '__main__':
    unittest.main()