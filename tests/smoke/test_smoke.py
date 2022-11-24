import unittest
from tests.unit.stub_test import TestReturnValue
from spotflow.api import monitor


class TestSmoke(unittest.TestCase):

    def test_simple_return_local(self):
        method_name = 'tests.unit.stub_sut.ReturnValue.simple_return'
        func = TestReturnValue().test_simple_return_local

        result = monitor(func, [method_name])

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        call_state = calls[0].call_state

        args = call_state.arg_states
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].name, 'self')


if __name__ == '__main__':
    unittest.main()
