import unittest
from tests.unit import stub_sut
from spotflow.api import monitor_func


class TestDescriptors(unittest.TestCase):

    base = 'tests.unit.stub_sut.HasDescriptors'

    def monitor(self, func):
        return monitor_func(func, ['tests.unit.stub_sut'])

    def test_class_method(self):
        result = self.monitor(stub_sut.call_descriptors)

        calls = result[self.base + '.class_method'].calls
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0].call_state.return_state, '2')
        self.assertEqual(calls[1].call_state.return_state, '3')
        self.assertEqual(len(calls[0].run_lines), 1)

    def test_static_method(self):
        result = self.monitor(stub_sut.call_descriptors)

        calls = result[self.base + '.static_method'].calls
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0].call_state.return_state, '3')
        self.assertEqual(calls[1].call_state.return_state, '4')
        self.assertEqual(calls[0].call_state.arg_states[0].name, 'x')

    def test_property_getter_and_setter(self):
        result = self.monitor(stub_sut.call_descriptors)

        # The getter and the setter have the same name
        calls = result[self.base + '.value'].calls
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0].call_state.arg_states[1].value, '5')
        self.assertEqual(calls[1].call_state.return_state, '5')

    def test_cached_property(self):
        result = self.monitor(stub_sut.call_descriptors)

        calls = result[self.base + '.cached_value'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].call_state.return_state, '15')

    def test_inherited_descriptors(self):
        result = self.monitor(stub_sut.call_inherited_descriptors)

        # Named by the class that defines them
        for name in ['class_method', 'static_method', 'cached_value']:
            self.assertEqual(len(result[f'{self.base}.{name}'].calls), 1, name)
        self.assertEqual(len(result[self.base + '.value'].calls), 2)

    def test_target_by_method_name(self):
        result = monitor_func(stub_sut.call_descriptors, [self.base + '.static_method'])

        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[self.base + '.static_method'].calls), 2)


if __name__ == '__main__':
    unittest.main()
