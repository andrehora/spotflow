import unittest
from happyflow.target_loader import TargetEntityLoader
from happyflow.tracer import TraceRunner


class TestArgAndReturnValue(unittest.TestCase):

    def test_simple_return_local(self):
        sut = TargetEntityLoader.find_sut('stub_sut.ReturnValue.simple_return')

        trace_result = TraceRunner.trace('stub_test.TestReturnValue.test_simple_return_local', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result.flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.args
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

        return_value = state_result.return_value
        self.assertEqual(return_value, 100)

    def test_simple_return_global(self):
        sut = TargetEntityLoader.find_sut('stub_sut.ReturnValue.simple_return')

        trace_result = TraceRunner.trace('stub_test.TestReturnValue.test_simple_return_global', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result.flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.args
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

        return_value = state_result.return_value
        self.assertEqual(return_value, 100)

    def test_simple_return_with_arg(self):
        sut = TargetEntityLoader.find_sut('stub_sut.ReturnValue.simple_return_with_arg')

        trace_result = TraceRunner.trace('stub_test.TestReturnValue.test_simple_return_with_arg', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result.flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.args
        self.assertEqual(len(args), 3)
        self.assertEqual(args[0].name, 'self')
        self.assertEqual(args[1].name, 'msg')
        self.assertEqual(args[2].name, 'name')

        return_value = state_result.return_value
        self.assertEqual(return_value, 'hello world')

    def test_change_return_0(self):
        sut = TargetEntityLoader.find_sut('stub_sut.ReturnValue.change_return_0')

        trace_result = TraceRunner.trace('stub_test.TestReturnValue.test_change_return_0', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result.flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.args
        self.assertEqual(len(args), 3)
        self.assertEqual(args[0].name, 'self')
        self.assertEqual(args[1].name, 'a')
        self.assertEqual(args[2].name, 'b')

        return_value = state_result.return_value
        self.assertEqual(return_value, 300)

    def test_change_return_1(self):
        sut = TargetEntityLoader.find_sut('stub_sut.ReturnValue.change_return_1')

        trace_result = TraceRunner.trace('stub_test.TestReturnValue.test_change_return_1', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result.flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.args
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

        return_value = state_result.return_value
        self.assertEqual(return_value, 3)

    def test_change_return_2(self):
        sut = TargetEntityLoader.find_sut('stub_sut.ReturnValue.change_return_2')

        trace_result = TraceRunner.trace('stub_test.TestReturnValue.test_change_return_2', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result.flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.args
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

        return_value = state_result.return_value
        self.assertEqual(return_value, 4)

    def test_change_return_3(self):
        sut = TargetEntityLoader.find_sut('stub_sut.ReturnValue.change_return_3')

        trace_result = TraceRunner.trace('stub_test.TestReturnValue.test_change_return_3', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result.flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.args
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

        return_value = state_result.return_value
        self.assertEqual(return_value, 'a and l')

    def test_change_return_4(self):
        sut = TargetEntityLoader.find_sut('stub_sut.ReturnValue.change_return_4')

        trace_result = TraceRunner.trace('stub_test.TestReturnValue.test_change_return_4', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result.flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.args
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

        return_value = state_result.return_value
        self.assertEqual(return_value, [1, 2, 3])

    def test_change_return_5(self):
        sut = TargetEntityLoader.find_sut('stub_sut.ReturnValue.change_return_5')

        trace_result = TraceRunner.trace('stub_test.TestReturnValue.test_change_return_5', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result.flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.args
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

        return_value = state_result.return_value
        self.assertEqual(return_value, 10)

    def test_multiple_return_true(self):
        sut = TargetEntityLoader.find_sut('stub_sut.ReturnValue.multiple_return')

        trace_result = TraceRunner.trace('stub_test.TestReturnValue.test_multiple_return_true', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result.flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.args
        self.assertEqual(len(args), 2)
        self.assertEqual(args[0].name, 'self')
        self.assertEqual(args[1].name, 'enter')

        return_value = state_result.return_value
        self.assertEqual(return_value, 'enter is true')

    def test_multiple_return_false(self):
        sut = TargetEntityLoader.find_sut('stub_sut.ReturnValue.multiple_return')

        trace_result = TraceRunner.trace('stub_test.TestReturnValue.test_multiple_return_false', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result.flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.args
        self.assertEqual(len(args), 2)
        self.assertEqual(args[0].name, 'self')
        self.assertEqual(args[1].name, 'enter')

        return_value = state_result.return_value
        self.assertEqual(return_value, 'enter is false')

    def test_change_attribute_0(self):
        sut = TargetEntityLoader.find_sut('stub_sut.ReturnValue.change_attribute_0')

        trace_result = TraceRunner.trace('stub_test.TestReturnValue.test_change_attribute_0', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result.flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.args
        self.assertEqual(len(args), 2)
        self.assertEqual(args[0].name, 'self')
        self.assertEqual(args[1].name, 'new_n')

        return_value = state_result.return_value
        self.assertEqual(return_value, 500)

    def test_change_attribute_1(self):
        sut = TargetEntityLoader.find_sut('stub_sut.ReturnValue.change_attribute_1')

        trace_result = TraceRunner.trace('stub_test.TestReturnValue.test_change_attribute_1', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result.flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.args
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

        return_value = state_result.return_value
        self.assertEqual(return_value, 101)

    def test_change_attribute_2(self):
        sut = TargetEntityLoader.find_sut('stub_sut.ReturnValue.change_attribute_2')

        trace_result = TraceRunner.trace('stub_test.TestReturnValue.test_change_attribute_2', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result.flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.args
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

        return_value = state_result.return_value
        self.assertEqual(return_value, 'foo')

    def test_change_attribute_3(self):
        sut = TargetEntityLoader.find_sut('stub_sut.ReturnValue.change_attribute_3')

        trace_result = TraceRunner.trace('stub_test.TestReturnValue.test_change_attribute_3', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result.flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.args
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

        return_value = state_result.return_value
        self.assertEqual(return_value, 5)

    def test_change_obj_1(self):
        sut = TargetEntityLoader.find_sut('stub_sut.ReturnValue.change_obj_1')

        trace_result = TraceRunner.trace('stub_test.TestReturnValue.test_change_obj_1', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result.flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.args
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

        return_value = state_result.return_value
        self.assertEqual(return_value, 9)

    def test_change_obj_2(self):
        sut = TargetEntityLoader.find_sut('stub_sut.ReturnValue.change_obj_2')

        trace_result = TraceRunner.trace('stub_test.TestReturnValue.test_change_obj_2', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result.flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.args
        self.assertEqual(len(args), 4)
        self.assertEqual(args[0].name, 'self')
        self.assertEqual(args[1].name, 'add1')
        self.assertEqual(args[2].name, 'add2')
        self.assertEqual(args[3].name, 'sub')

        return_value = state_result.return_value
        self.assertEqual(return_value, 19)

    def test_change_obj_3(self):
        sut = TargetEntityLoader.find_sut('stub_sut.ReturnValue.change_obj_3')

        trace_result = TraceRunner.trace('stub_test.TestReturnValue.test_change_obj_3', sut)
        flow_result = sut.local_flows(trace_result)

        flows = flow_result.flows
        self.assertEqual(len(flows), 1)

        state_result = flows[0].state_result

        args = state_result.args
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')

        return_value = state_result.return_value
        from happyflow.tests.stub_sut import Calculator
        self.assertEqual(return_value, Calculator(9))



