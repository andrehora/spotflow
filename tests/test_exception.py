import unittest
from happyflow.tracer import TraceRunner


class TestException(unittest.TestCase):

    def test_zero_division(self):
        target_entity_name = 'tests.stub_sut.Exceptions.zero_division'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestExceptions.test_zero_division', [target_entity_name])

        flows = trace_result[target_entity_name].flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result
        exception_state = state_result.exception_state
        self.assertEqual(exception_state.line, 237)
        self.assertEqual(exception_state.value[0], ZeroDivisionError)

    def test_raise_generic_exception(self):
        target_entity_name = 'tests.stub_sut.Exceptions.raise_generic_exception'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestExceptions.test_raise_generic_exception', [target_entity_name])

        flows = trace_result[target_entity_name].flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result
        exception_state = state_result.exception_state
        self.assertEqual(exception_state.line, 240)
        self.assertEqual(exception_state.value[0], Exception)

    def test_raise_specific_exception(self):
        target_entity_name = 'tests.stub_sut.Exceptions.raise_specific_exception'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestExceptions.test_raise_specific_exception', [target_entity_name])

        flows = trace_result[target_entity_name].flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result
        exception_state = state_result.exception_state
        self.assertEqual(exception_state.line, 243)
        self.assertEqual(exception_state.value[0], TypeError)


    def test_raise_exception_line_1(self):
        target_entity_name = 'tests.stub_sut.Exceptions.raise_distinct_exception'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestExceptions.test_raise_exception_line_1', [target_entity_name])

        flows = trace_result[target_entity_name].flows
        self.assertEqual(len(flows), 1)

        run_lines = flows[0].run_lines
        self.assertEqual(run_lines, [246])

        state_result = flows[0].state_result
        exception_state = state_result.exception_state
        self.assertEqual(exception_state.line, 246)
        self.assertEqual(exception_state.value[0], Exception)

    def test_raise_exception_line_2(self):
        target_entity_name = 'tests.stub_sut.Exceptions.raise_distinct_exception'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestExceptions.test_raise_exception_line_2', [target_entity_name])

        flows = trace_result[target_entity_name].flows
        self.assertEqual(len(flows), 1)

        run_lines = flows[0].run_lines
        self.assertEqual(run_lines, [246, 247])

        state_result = flows[0].state_result
        exception_state = state_result.exception_state
        self.assertEqual(exception_state.line, 247)
        self.assertEqual(exception_state.value[0], Exception)

    def test_raise_exception_line_3(self):
        target_entity_name = 'tests.stub_sut.Exceptions.raise_distinct_exception'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestExceptions.test_raise_exception_line_3', [target_entity_name])

        flows = trace_result[target_entity_name].flows
        self.assertEqual(len(flows), 1)

        run_lines = flows[0].run_lines
        self.assertEqual(run_lines, [246, 247, 248])

        state_result = flows[0].state_result
        exception_state = state_result.exception_state
        self.assertEqual(exception_state.line, 248)
        self.assertEqual(exception_state.value[0], Exception)

    def test_raise_no_exception(self):
        target_entity_name = 'tests.stub_sut.Exceptions.raise_distinct_exception'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestExceptions.test_raise_no_exception', [target_entity_name])

        flows = trace_result[target_entity_name].flows
        self.assertEqual(len(flows), 1)

        run_lines = flows[0].run_lines
        self.assertEqual(run_lines, [246, 247, 248])

    def test_flows_with_exceptions(self):
        target_entity_name = 'tests.stub_sut.Exceptions.raise_distinct_exception'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestExceptions.test_flows_with_exceptions', [target_entity_name])

        flows = trace_result[target_entity_name].flows
        self.assertEqual(len(flows), 3)

        # Flow 1
        run_lines = flows[0].run_lines
        self.assertEqual(run_lines, [246])
        state_result = flows[0].state_result
        exception_state = state_result.exception_state
        self.assertEqual(exception_state.line, 246)
        self.assertEqual(exception_state.value[0], Exception)

        # Flow 2
        run_lines = flows[1].run_lines
        self.assertEqual(run_lines, [246, 247])
        state_result = flows[1].state_result
        exception_state = state_result.exception_state
        self.assertEqual(exception_state.line, 247)
        self.assertEqual(exception_state.value[0], Exception)

        # Flow 3
        run_lines = flows[2].run_lines
        self.assertEqual(run_lines, [246, 247, 248])
        state_result = flows[2].state_result
        exception_state = state_result.exception_state
        self.assertEqual(exception_state.line, 248)
        self.assertEqual(exception_state.value[0], Exception)


if __name__ == '__main__':
    unittest.main()