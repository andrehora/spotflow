import unittest
from tests.stub_test import TestExceptions
from happyflow.api import run_and_flow_func


class TestException(unittest.TestCase):

    def test_zero_division(self):
        target_entity_name = 'tests.stub_sut.Exceptions.zero_division'
        func = TestExceptions().test_zero_division

        result = run_and_flow_func(func, [target_entity_name])

        flows = result[target_entity_name].flows
        self.assertEqual(len(flows), 1)

        state_history = flows[0].state_history
        exception_state = state_history.exception_state
        self.assertEqual(exception_state.line, 237)
        self.assertEqual(exception_state.value[0], ZeroDivisionError)

    def test_raise_generic_exception(self):
        target_entity_name = 'tests.stub_sut.Exceptions.raise_generic_exception'
        func = TestExceptions().test_raise_generic_exception

        result = run_and_flow_func(func, [target_entity_name])

        flows = result[target_entity_name].flows
        self.assertEqual(len(flows), 1)

        state_history = flows[0].state_history
        exception_state = state_history.exception_state
        self.assertEqual(exception_state.line, 240)
        self.assertEqual(exception_state.value[0], Exception)

    def test_raise_specific_exception(self):
        target_entity_name = 'tests.stub_sut.Exceptions.raise_specific_exception'
        func = TestExceptions().test_raise_specific_exception

        result = run_and_flow_func(func, [target_entity_name])

        flows = result[target_entity_name].flows
        self.assertEqual(len(flows), 1)

        state_history = flows[0].state_history
        exception_state = state_history.exception_state
        self.assertEqual(exception_state.line, 243)
        self.assertEqual(exception_state.value[0], TypeError)


    def test_raise_exception_line_1(self):
        target_entity_name = 'tests.stub_sut.Exceptions.raise_distinct_exception'
        func = TestExceptions().test_raise_exception_line_1

        result = run_and_flow_func(func, [target_entity_name])

        flows = result[target_entity_name].flows
        self.assertEqual(len(flows), 1)

        run_lines = flows[0].run_lines
        self.assertEqual(run_lines, [246])

        state_history = flows[0].state_history
        exception_state = state_history.exception_state
        self.assertEqual(exception_state.line, 246)
        self.assertEqual(exception_state.value[0], Exception)

    def test_raise_exception_line_2(self):
        target_entity_name = 'tests.stub_sut.Exceptions.raise_distinct_exception'
        func = TestExceptions().test_raise_exception_line_2

        result = run_and_flow_func(func, [target_entity_name])

        flows = result[target_entity_name].flows
        self.assertEqual(len(flows), 1)

        run_lines = flows[0].run_lines
        self.assertEqual(run_lines, [246, 247])

        state_history = flows[0].state_history
        exception_state = state_history.exception_state
        self.assertEqual(exception_state.line, 247)
        self.assertEqual(exception_state.value[0], Exception)

    def test_raise_exception_line_3(self):
        target_entity_name = 'tests.stub_sut.Exceptions.raise_distinct_exception'
        func = TestExceptions().test_raise_exception_line_3

        result = run_and_flow_func(func, [target_entity_name])

        flows = result[target_entity_name].flows
        self.assertEqual(len(flows), 1)

        run_lines = flows[0].run_lines
        self.assertEqual(run_lines, [246, 247, 248])

        state_history = flows[0].state_history
        exception_state = state_history.exception_state
        self.assertEqual(exception_state.line, 248)
        self.assertEqual(exception_state.value[0], Exception)

    def test_raise_no_exception(self):
        target_entity_name = 'tests.stub_sut.Exceptions.raise_distinct_exception'
        func = TestExceptions().test_raise_no_exception

        result = run_and_flow_func(func, [target_entity_name])

        flows = result[target_entity_name].flows
        self.assertEqual(len(flows), 1)

        run_lines = flows[0].run_lines
        self.assertEqual(run_lines, [246, 247, 248])

    def test_flows_with_exceptions(self):
        target_entity_name = 'tests.stub_sut.Exceptions.raise_distinct_exception'
        func = TestExceptions().test_flows_with_exceptions

        result = run_and_flow_func(func, [target_entity_name])

        flows = result[target_entity_name].flows
        self.assertEqual(len(flows), 3)

        # Flow 1
        run_lines = flows[0].run_lines
        self.assertEqual(run_lines, [246])
        state_history = flows[0].state_history
        exception_state = state_history.exception_state
        self.assertEqual(exception_state.line, 246)
        self.assertEqual(exception_state.value[0], Exception)

        # Flow 2
        run_lines = flows[1].run_lines
        self.assertEqual(run_lines, [246, 247])
        state_history = flows[1].state_history
        exception_state = state_history.exception_state
        self.assertEqual(exception_state.line, 247)
        self.assertEqual(exception_state.value[0], Exception)

        # Flow 3
        run_lines = flows[2].run_lines
        self.assertEqual(run_lines, [246, 247, 248])
        state_history = flows[2].state_history
        exception_state = state_history.exception_state
        self.assertEqual(exception_state.line, 248)
        self.assertEqual(exception_state.value[0], Exception)


if __name__ == '__main__':
    unittest.main()