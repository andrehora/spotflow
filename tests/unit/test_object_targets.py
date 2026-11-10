import unittest
from tests.unit import stub_sut
from spotflow.api import monitor_func


class TestObjectTargets(unittest.TestCase):

    base = 'tests.unit.stub_sut'

    def calls_per_method(self, targets):
        result = monitor_func(stub_sut.call_targets, targets)
        return {method.full_name: len(method.calls) for method in result}

    def test_one_function(self):
        calls = self.calls_per_method([stub_sut.target_one])
        self.assertEqual(calls, {f'{self.base}.target_one': 1})

    def test_two_functions(self):
        calls = self.calls_per_method([stub_sut.target_one, stub_sut.target_two])
        self.assertEqual(calls, {f'{self.base}.target_one': 1, f'{self.base}.target_two': 2})

    def test_two_functions_in_reverse_order(self):
        calls = self.calls_per_method([stub_sut.target_two, stub_sut.target_one])
        self.assertEqual(calls, {f'{self.base}.target_one': 1, f'{self.base}.target_two': 2})

    def test_function_and_method(self):
        targets = [stub_sut.target_two, stub_sut.HasTargets.target_method, stub_sut.target_one]
        calls = self.calls_per_method(targets)
        self.assertEqual(calls, {
            f'{self.base}.target_one': 1,
            f'{self.base}.target_two': 2,
            f'{self.base}.HasTargets.target_method': 1,
        })

    def test_bound_method(self):
        calls = self.calls_per_method([stub_sut.HasTargets().target_method, stub_sut.target_one])
        self.assertEqual(calls, {
            f'{self.base}.target_one': 1,
            f'{self.base}.HasTargets.target_method': 1,
        })

    def test_function_and_name(self):
        calls = self.calls_per_method([stub_sut.target_one, f'{self.base}.target_two'])
        self.assertEqual(calls, {f'{self.base}.target_one': 1, f'{self.base}.target_two': 2})

    def test_calls_have_lines_and_states(self):
        result = monitor_func(stub_sut.call_targets, [stub_sut.target_one, stub_sut.target_two])
        call = result[f'{self.base}.target_two'].calls[1]
        self.assertEqual(len(call.run_lines), 1)
        self.assertEqual(call.call_state.return_state, '4')


if __name__ == '__main__':
    unittest.main()
