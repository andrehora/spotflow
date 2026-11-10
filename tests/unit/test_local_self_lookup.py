import unittest
from tests.unit import stub_sut
from spotflow.api import monitor_func


class TestLocalSelfLookup(unittest.TestCase):

    def test_does_not_run_properties_of_monitored_object(self):
        stub_sut.HasSideEffectProperty.reads = 0

        def func():
            stub_sut.HasSideEffectProperty([1, 2, 3])

        monitor_func(func, ['tests.unit.stub_sut.HasSideEffectProperty'])

        self.assertEqual(stub_sut.HasSideEffectProperty.reads, 0)

    def test_local_static_method(self):
        base = 'tests.unit.stub_sut.has_local_static_method_and_func_attr'
        func = stub_sut.has_local_static_method_and_func_attr

        result = monitor_func(func, ['tests.unit.stub_sut'])

        calls = result[base + '.<locals>.LocalClass4.local_static'].calls
        self.assertEqual(len(calls), 1)

    def test_local_func_as_instance_attribute(self):
        base = 'tests.unit.stub_sut.has_local_static_method_and_func_attr'
        func = stub_sut.has_local_static_method_and_func_attr

        result = monitor_func(func, ['tests.unit.stub_sut'])

        calls = result[base + '.<locals>.local_callback'].calls
        self.assertEqual(len(calls), 1)


if __name__ == '__main__':
    unittest.main()
