import unittest
from happyflow.target_loader import TargetEntityLoader
from happyflow.tracer import TraceRunner


class TestArgAndReturnValue(unittest.TestCase):

    def test_simple_return_local(self):
        sut = TargetEntityLoader.find('stub_sut.ReturnValue.simple_return', '.', 'stub_sut')

        trace_result = TraceRunner.trace_tests('tests.stub_test.TestReturnValue.test_simple_return_local', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result[0].flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.args
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

        return_state = state_result.return_state
        self.assertEqual(return_state, 100)

    def test_simple_return_global(self):
        sut = TargetEntityLoader.find('stub_sut.ReturnValue.simple_return', '.', 'stub_sut')

        trace_result = TraceRunner.trace_tests('tests.stub_test.TestReturnValue.test_simple_return_global', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result[0].flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.args
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

        return_state = state_result.return_state
        self.assertEqual(return_state, 100)

    def test_simple_return_with_arg(self):
        sut = TargetEntityLoader.find('stub_sut.ReturnValue.simple_return_with_arg', '.', 'stub_sut')

        trace_result = TraceRunner.trace_tests('tests.stub_test.TestReturnValue.test_simple_return_with_arg', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result[0].flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.args
        self.assertEqual(len(args), 3)
        self.assertEqual(args[0].name, 'self')
        self.assertEqual(args[1].name, 'msg')
        self.assertEqual(args[2].name, 'name')

        return_state = state_result.return_state
        self.assertEqual(return_state, 'hello world')

    def test_change_return_0(self):
        sut = TargetEntityLoader.find('stub_sut.ReturnValue.change_return_0', '.', 'stub_sut')

        trace_result = TraceRunner.trace_tests('tests.stub_test.TestReturnValue.test_change_return_0', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result[0].flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.args
        self.assertEqual(len(args), 3)
        self.assertEqual(args[0].name, 'self')
        self.assertEqual(args[1].name, 'a')
        self.assertEqual(args[2].name, 'b')

        return_state = state_result.return_state
        self.assertEqual(return_state, 300)

    def test_change_return_1(self):
        sut = TargetEntityLoader.find('stub_sut.ReturnValue.change_return_1', '.', 'stub_sut')

        trace_result = TraceRunner.trace_tests('tests.stub_test.TestReturnValue.test_change_return_1', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result[0].flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.args
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

        return_state = state_result.return_state
        self.assertEqual(return_state, 3)

    def test_change_return_2(self):
        sut = TargetEntityLoader.find('stub_sut.ReturnValue.change_return_2', '.', 'stub_sut')

        trace_result = TraceRunner.trace_tests('tests.stub_test.TestReturnValue.test_change_return_2', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result[0].flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.args
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

        return_state = state_result.return_state
        self.assertEqual(return_state, 4)

    def test_change_return_3(self):
        sut = TargetEntityLoader.find('stub_sut.ReturnValue.change_return_3', '.', 'stub_sut')

        trace_result = TraceRunner.trace_tests('tests.stub_test.TestReturnValue.test_change_return_3', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result[0].flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.args
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

        return_state = state_result.return_state
        self.assertEqual(return_state, 'a and l')

    def test_change_return_4(self):
        sut = TargetEntityLoader.find('stub_sut.ReturnValue.change_return_4', '.', 'stub_sut')

        trace_result = TraceRunner.trace_tests('tests.stub_test.TestReturnValue.test_change_return_4', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result[0].flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.args
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

        return_state = state_result.return_state
        self.assertEqual(return_state, [1, 2, 3])

    def test_change_return_5(self):
        sut = TargetEntityLoader.find('stub_sut.ReturnValue.change_return_5', '.', 'stub_sut')

        trace_result = TraceRunner.trace_tests('tests.stub_test.TestReturnValue.test_change_return_5', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result[0].flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.args
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

        return_state = state_result.return_state
        self.assertEqual(return_state, 10)

    def test_multiple_return_true(self):
        sut = TargetEntityLoader.find('stub_sut.ReturnValue.multiple_return', '.', 'stub_sut')

        trace_result = TraceRunner.trace_tests('tests.stub_test.TestReturnValue.test_multiple_return_true', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result[0].flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.args
        self.assertEqual(len(args), 2)
        self.assertEqual(args[0].name, 'self')
        self.assertEqual(args[1].name, 'enter')

        return_state = state_result.return_state
        self.assertEqual(return_state, 'enter is true')

    def test_multiple_return_false(self):
        sut = TargetEntityLoader.find('stub_sut.ReturnValue.multiple_return', '.', 'stub_sut')

        trace_result = TraceRunner.trace_tests('tests.stub_test.TestReturnValue.test_multiple_return_false', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result[0].flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.args
        self.assertEqual(len(args), 2)
        self.assertEqual(args[0].name, 'self')
        self.assertEqual(args[1].name, 'enter')

        return_state = state_result.return_state
        self.assertEqual(return_state, 'enter is false')

    def test_change_attribute_0(self):
        sut = TargetEntityLoader.find('stub_sut.ReturnValue.change_attribute_0', '.', 'stub_sut')

        trace_result = TraceRunner.trace_tests('tests.stub_test.TestReturnValue.test_change_attribute_0', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result[0].flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.args
        self.assertEqual(len(args), 2)
        self.assertEqual(args[0].name, 'self')
        self.assertEqual(args[1].name, 'new_n')

        return_state = state_result.return_state
        self.assertEqual(return_state, 500)

    def test_change_attribute_1(self):
        sut = TargetEntityLoader.find('stub_sut.ReturnValue.change_attribute_1', '.', 'stub_sut')

        trace_result = TraceRunner.trace_tests('tests.stub_test.TestReturnValue.test_change_attribute_1', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result[0].flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.args
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

        return_state = state_result.return_state
        self.assertEqual(return_state, 101)

    def test_change_attribute_2(self):
        sut = TargetEntityLoader.find('stub_sut.ReturnValue.change_attribute_2', '.', 'stub_sut')

        trace_result = TraceRunner.trace_tests('tests.stub_test.TestReturnValue.test_change_attribute_2', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result[0].flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.args
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

        return_state = state_result.return_state
        self.assertEqual(return_state, 'foo')

    def test_change_attribute_3(self):
        sut = TargetEntityLoader.find('stub_sut.ReturnValue.change_attribute_3', '.', 'stub_sut')

        trace_result = TraceRunner.trace_tests('tests.stub_test.TestReturnValue.test_change_attribute_3', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result[0].flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.args
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

        return_state = state_result.return_state
        self.assertEqual(return_state, 5)

    def test_change_obj_1(self):
        sut = TargetEntityLoader.find('stub_sut.ReturnValue.change_obj_1', '.', 'stub_sut')

        trace_result = TraceRunner.trace_tests('tests.stub_test.TestReturnValue.test_change_obj_1', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result[0].flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.args
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

        return_state = state_result.return_state
        self.assertEqual(return_state, 9)

    def test_change_obj_2(self):
        sut = TargetEntityLoader.find('stub_sut.ReturnValue.change_obj_2', '.', 'stub_sut')

        trace_result = TraceRunner.trace_tests('tests.stub_test.TestReturnValue.test_change_obj_2', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result[0].flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.args
        self.assertEqual(len(args), 4)
        self.assertEqual(args[0].name, 'self')
        self.assertEqual(args[1].name, 'add1')
        self.assertEqual(args[2].name, 'add2')
        self.assertEqual(args[3].name, 'sub')

        return_state = state_result.return_state
        self.assertEqual(return_state, 19)

    def test_change_obj_3(self):
        sut = TargetEntityLoader.find('stub_sut.ReturnValue.change_obj_3', '.', 'stub_sut')

        trace_result = TraceRunner.trace_tests('tests.stub_test.TestReturnValue.test_change_obj_3', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result[0].flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.args
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

        return_state = state_result.return_state
        from tests.stub_sut import Calculator
        self.assertEqual(return_state, Calculator(9))

    def test_explicit_return_state(self):
        sut = TargetEntityLoader.find('stub_sut.ReturnValue.explicit_return_state', '.', 'stub_sut')
        trace_result = TraceRunner.trace_tests('tests.stub_test.TestReturnValue.test_explicit_return_state', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result[0].flows
        return_state = flows[0].state_result.return_state

        self.assertTrue(return_state.has_return)
        self.assertEqual(return_state.value, 123)

    def test_explicit_return_none(self):
        sut = TargetEntityLoader.find('stub_sut.ReturnValue.explicit_return_none', '.', 'stub_sut')
        trace_result = TraceRunner.trace_tests('tests.stub_test.TestReturnValue.test_explicit_return_none', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result[0].flows
        return_state = flows[0].state_result.return_state

        self.assertTrue(return_state.has_return)
        self.assertEqual(return_state.value, None)

    def test_explicit_return(self):
        sut = TargetEntityLoader.find('stub_sut.ReturnValue.explicit_return', '.', 'stub_sut')
        trace_result = TraceRunner.trace_tests('tests.stub_test.TestReturnValue.test_explicit_return', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result[0].flows
        return_state = flows[0].state_result.return_state

        self.assertTrue(return_state.has_return)
        self.assertEqual(return_state.value, None)

    def test_implicit_return(self):
        sut = TargetEntityLoader.find('stub_sut.ReturnValue.implicit_return', '.', 'stub_sut')
        trace_result = TraceRunner.trace_tests('tests.stub_test.TestReturnValue.test_implicit_return', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result[0].flows
        return_state = flows[0].state_result.return_state

        self.assertFalse(return_state.has_return)
        self.assertEqual(return_state.value, None)


if __name__ == '__main__':
    unittest.main()
