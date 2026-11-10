import unittest
from tests.unit import stub_sut
from spotflow.api import monitor_func


class TestNameTargets(unittest.TestCase):

    base = 'tests.unit.stub_sut'

    def calls_per_method(self, targets, func=stub_sut.call_prefixes):
        result = monitor_func(func, targets)
        return {method.full_name[len(self.base) + 1:]: len(method.calls) for method in result}

    def test_function_name_is_not_a_prefix_of_other_names(self):
        calls = self.calls_per_method([f'{self.base}.prefix'])
        self.assertEqual(calls, {'prefix': 1})

    def test_class_name_is_not_a_prefix_of_other_names(self):
        calls = self.calls_per_method([f'{self.base}.Prefix'])
        self.assertEqual(calls, {'Prefix.run': 1})

    def test_longer_name(self):
        calls = self.calls_per_method([f'{self.base}.PrefixLonger'])
        self.assertEqual(calls, {'PrefixLonger.run': 1})

    def test_module_name(self):
        calls = self.calls_per_method([self.base])
        self.assertEqual(calls, {
            'call_prefixes': 1,
            'prefix': 1,
            'prefix_longer': 1,
            'Prefix.run': 1,
            'PrefixLonger.run': 1,
        })

    def test_package_name(self):
        calls = self.calls_per_method(['tests.unit'])
        self.assertEqual(len(calls), 5)

    def test_part_of_module_name(self):
        calls = self.calls_per_method(['tests.unit.stub_s'])
        self.assertEqual(calls, {})

    def test_local_function_of_target(self):
        calls = self.calls_per_method([f'{self.base}.has_local_static_method_and_func_attr'],
                                      stub_sut.has_local_static_method_and_func_attr)
        self.assertIn('has_local_static_method_and_func_attr.<locals>.local_callback', calls)

    def test_overlapping_names(self):
        calls = self.calls_per_method([self.base, f'{self.base}.prefix', f'{self.base}.Prefix.run'])
        self.assertEqual(calls['prefix'], 1)
        self.assertEqual(calls['Prefix.run'], 1)
        self.assertEqual(calls['prefix_longer'], 1)

    def test_same_name_twice(self):
        calls = self.calls_per_method([f'{self.base}.prefix', f'{self.base}.prefix'])
        self.assertEqual(calls, {'prefix': 1})

    def test_overlapping_name_and_function(self):
        for targets in ([self.base, stub_sut.prefix], [stub_sut.prefix, self.base]):
            calls = self.calls_per_method(targets)
            self.assertEqual(calls['prefix'], 1)
            self.assertEqual(calls['prefix_longer'], 1)

    def test_same_function_twice(self):
        calls = self.calls_per_method([stub_sut.prefix, stub_sut.prefix])
        self.assertEqual(calls, {'prefix': 1})

    def test_overlapping_targets_keep_lines_and_states(self):
        result = monitor_func(stub_sut.call_prefixes, [self.base, f'{self.base}.prefix'])
        call = result[f'{self.base}.prefix'].calls[0]
        self.assertEqual(len(call.run_lines), 1)
        self.assertEqual(call.call_state.return_state, '1')
        self.assertEqual(list(result[f'{self.base}.prefix'].run_lines.values()), [1])

    def test_no_targets_monitors_all_methods(self):
        calls = self.calls_per_method(None)
        self.assertEqual(calls['prefix'], 1)
        self.assertEqual(calls['Prefix.run'], 1)

    def test_empty_targets_monitors_nothing(self):
        calls = self.calls_per_method([])
        self.assertEqual(calls, {})

    def test_method_is_monitored_in_all_its_calls(self):
        def func():
            for _ in range(3):
                stub_sut.call_prefixes()

        calls = self.calls_per_method([f'{self.base}.prefix', f'{self.base}.Prefix'], func)
        self.assertEqual(calls, {'prefix': 3, 'Prefix.run': 3})

    def test_targets_can_change_between_runs(self):
        from spotflow.api import SpotFlow
        flow = SpotFlow()
        flow.target_method_full_names([f'{self.base}.prefix'])
        flow.start()
        stub_sut.call_prefixes()
        flow.stop()
        flow.target_method_full_names([f'{self.base}.prefix_longer'])
        flow.start()
        stub_sut.call_prefixes()
        flow.stop()

        calls = {method.name: len(method.calls) for method in flow.result()}
        self.assertEqual(calls, {'prefix': 1, 'prefix_longer': 1})


if __name__ == '__main__':
    unittest.main()
