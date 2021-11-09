import unittest
from happyflow.tracer import TraceRunner


class TestArgAndReturnValue(unittest.TestCase):

    def test_simple_return_local(self):
        target_entity_name = 'tests.stub_sut.ReturnValue.simple_return'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestReturnValue.test_simple_return_local', [target_entity_name])

        flows = trace_result[target_entity_name].flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.arg_states
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

        return_state = state_result.return_state
        self.assertEqual(return_state, 100)

    def test_simple_return_global(self):
        target_entity_name = 'tests.stub_sut.ReturnValue.simple_return'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestReturnValue.test_simple_return_global', [target_entity_name])

        flows = trace_result[target_entity_name].flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.arg_states
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

        return_state = state_result.return_state
        self.assertEqual(return_state, 100)

    def test_simple_return_with_arg(self):
        target_entity_name = 'tests.stub_sut.ReturnValue.simple_return_with_arg'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestReturnValue.test_simple_return_with_arg', [target_entity_name])

        flows = trace_result[target_entity_name].flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.arg_states
        self.assertEqual(len(args), 3)
        self.assertEqual(args[0].name, 'self')
        self.assertEqual(args[1].name, 'msg')
        self.assertEqual(args[2].name, 'name')

        return_state = state_result.return_state
        self.assertEqual(return_state, 'hello world')

    def test_change_return_0(self):
        target_entity_name = 'tests.stub_sut.ReturnValue.change_return_0'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestReturnValue.test_change_return_0', [target_entity_name])

        flows = trace_result[target_entity_name].flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.arg_states
        self.assertEqual(len(args), 3)
        self.assertEqual(args[0].name, 'self')
        self.assertEqual(args[1].name, 'a')
        self.assertEqual(args[2].name, 'b')

        return_state = state_result.return_state
        self.assertEqual(return_state, 300)

    def test_change_return_1(self):
        target_entity_name = 'tests.stub_sut.ReturnValue.change_return_1'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestReturnValue.test_change_return_1', [target_entity_name])

        flows = trace_result[target_entity_name].flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.arg_states
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

        return_state = state_result.return_state
        self.assertEqual(return_state, 3)

    def test_change_return_2(self):
        target_entity_name = 'tests.stub_sut.ReturnValue.change_return_2'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestReturnValue.test_change_return_2', [target_entity_name])

        flows = trace_result[target_entity_name].flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.arg_states
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

        return_state = state_result.return_state
        self.assertEqual(return_state, 4)

    def test_change_return_3(self):
        target_entity_name = 'tests.stub_sut.ReturnValue.change_return_3'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestReturnValue.test_change_return_3', [target_entity_name])

        flows = trace_result[target_entity_name].flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.arg_states
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

        return_state = state_result.return_state
        self.assertEqual(return_state, 'a and l')

    def test_change_return_4(self):
        target_entity_name = 'tests.stub_sut.ReturnValue.change_return_4'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestReturnValue.test_change_return_4', [target_entity_name])

        flows = trace_result[target_entity_name].flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.arg_states
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

        return_state = state_result.return_state
        self.assertEqual(return_state, [1, 2, 3])

    def test_change_return_5(self):
        target_entity_name = 'tests.stub_sut.ReturnValue.change_return_5'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestReturnValue.test_change_return_5', [target_entity_name])

        flows = trace_result[target_entity_name].flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.arg_states
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

        return_state = state_result.return_state
        self.assertEqual(return_state, 10)

    def test_multiple_return_true(self):
        target_entity_name = 'tests.stub_sut.ReturnValue.multiple_return'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestReturnValue.test_multiple_return_true', [target_entity_name])

        flows = trace_result[target_entity_name].flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.arg_states
        self.assertEqual(len(args), 2)
        self.assertEqual(args[0].name, 'self')
        self.assertEqual(args[1].name, 'enter')

        return_state = state_result.return_state
        self.assertEqual(return_state, 'enter is true')

    def test_multiple_return_false(self):
        target_entity_name = 'tests.stub_sut.ReturnValue.multiple_return'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestReturnValue.test_multiple_return_false', [target_entity_name])

        flows = trace_result[target_entity_name].flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.arg_states
        self.assertEqual(len(args), 2)
        self.assertEqual(args[0].name, 'self')
        self.assertEqual(args[1].name, 'enter')

        return_state = state_result.return_state
        self.assertEqual(return_state, 'enter is false')

    def test_change_attribute_0(self):
        target_entity_name = 'tests.stub_sut.ReturnValue.change_attribute_0'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestReturnValue.test_change_attribute_0', [target_entity_name])

        flows = trace_result[target_entity_name].flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.arg_states
        self.assertEqual(len(args), 2)
        self.assertEqual(args[0].name, 'self')
        self.assertEqual(args[1].name, 'new_n')

        return_state = state_result.return_state
        self.assertEqual(return_state, 500)

    def test_change_attribute_1(self):
        target_entity_name = 'tests.stub_sut.ReturnValue.change_attribute_1'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestReturnValue.test_change_attribute_1', [target_entity_name])

        flows = trace_result[target_entity_name].flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.arg_states
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

        return_state = state_result.return_state
        self.assertEqual(return_state, 101)

    def test_change_attribute_2(self):
        target_entity_name = 'tests.stub_sut.ReturnValue.change_attribute_2'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestReturnValue.test_change_attribute_2', [target_entity_name])

        flows = trace_result[target_entity_name].flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.arg_states
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

        return_state = state_result.return_state
        self.assertEqual(return_state, 'foo')

    def test_change_attribute_3(self):
        target_entity_name = 'tests.stub_sut.ReturnValue.change_attribute_3'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestReturnValue.test_change_attribute_3', [target_entity_name])

        flows = trace_result[target_entity_name].flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.arg_states
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

        return_state = state_result.return_state
        self.assertEqual(return_state, 5)

    def test_change_obj_1(self):
        target_entity_name = 'tests.stub_sut.ReturnValue.change_obj_1'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestReturnValue.test_change_obj_1', [target_entity_name])

        flows = trace_result[target_entity_name].flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.arg_states
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

        return_state = state_result.return_state
        self.assertEqual(return_state, 9)

    def test_change_obj_2(self):
        target_entity_name = 'tests.stub_sut.ReturnValue.change_obj_2'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestReturnValue.test_change_obj_2', [target_entity_name])

        flows = trace_result[target_entity_name].flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.arg_states
        self.assertEqual(len(args), 4)
        self.assertEqual(args[0].name, 'self')
        self.assertEqual(args[1].name, 'add1')
        self.assertEqual(args[2].name, 'add2')
        self.assertEqual(args[3].name, 'sub')

        return_state = state_result.return_state
        self.assertEqual(return_state, 19)

    def test_change_obj_3(self):
        target_entity_name = 'tests.stub_sut.ReturnValue.change_obj_3'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestReturnValue.test_change_obj_3', [target_entity_name])

        flows = trace_result[target_entity_name].flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.arg_states
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

        return_state = state_result.return_state
        from tests.stub_sut import Calculator
        self.assertEqual(return_state, Calculator(9))

    def test_explicit_return_state(self):
        target_entity_name = 'tests.stub_sut.ReturnValue.explicit_return_state'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestReturnValue.test_explicit_return_state', [target_entity_name])

        flows = trace_result[target_entity_name].flows
        return_state = flows[0].state_result.return_state

        self.assertTrue(return_state.has_return)
        self.assertEqual(return_state.value, 123)

    def test_explicit_return_none(self):
        target_entity_name = 'tests.stub_sut.ReturnValue.explicit_return_none'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestReturnValue.test_explicit_return_none', [target_entity_name])

        flows = trace_result[target_entity_name].flows
        return_state = flows[0].state_result.return_state

        self.assertTrue(return_state.has_return)
        self.assertEqual(return_state.value, None)

    def test_explicit_return(self):
        target_entity_name = 'tests.stub_sut.ReturnValue.explicit_return'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestReturnValue.test_explicit_return', [target_entity_name])

        flows = trace_result[target_entity_name].flows
        return_state = flows[0].state_result.return_state

        self.assertTrue(return_state.has_return)
        self.assertEqual(return_state.value, None)

    def test_implicit_return(self):
        target_entity_name = 'tests.stub_sut.ReturnValue.implicit_return'
        trace_result = TraceRunner.trace_from_tests('tests.stub_test.TestReturnValue.test_implicit_return', [target_entity_name])

        flows = trace_result[target_entity_name].flows
        return_state = flows[0].state_result.return_state

        self.assertFalse(return_state.has_return)
        self.assertEqual(return_state.value, None)


if __name__ == '__main__':
    unittest.main()
