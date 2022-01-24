import unittest
from tests.unit.stub_test import TestClassWithExternalDependency
from happyflow.api import monitor


class TestFilter(unittest.TestCase):

    def test_no_filter(self):
        func = TestClassWithExternalDependency().test_call_external_dependencies

        result = monitor(func)
        methods = result.all_methods()

        self.assertGreaterEqual(len(methods), 20)
        self.assertGreaterEqual(len(result.all_calls()), 20)

    def test_filter_by_method_name(self):
        method_name = 'tests.unit.stub_sut'
        func = TestClassWithExternalDependency().test_call_external_dependencies

        result = monitor(func, target_methods=[method_name])
        methods = result.all_methods()

        self.assertEqual(len(methods), 6)
        self.assertEqual(len(result.all_calls()), 6)

        self.assertEqual(methods[0].info.full_name,
                         'tests.unit.stub_sut.ClassWithExternalDependency.call_external_dependencies')
        self.assertEqual(methods[1].info.full_name,
                         'tests.unit.stub_sut.ClassWithExternalDependency.str_split')
        self.assertEqual(methods[2].info.full_name,
                         'tests.unit.stub_sut.ClassWithExternalDependency.time_time')
        self.assertEqual(methods[3].info.full_name,
                         'tests.unit.stub_sut.ClassWithExternalDependency.os_isdir')
        self.assertEqual(methods[4].info.full_name,
                         'tests.unit.stub_sut.ClassWithExternalDependency.os_realpath')
        self.assertEqual(methods[5].info.full_name,
                         'tests.unit.stub_sut.ClassWithExternalDependency.inspect_ismethod')

    def test_filter_by_multiple_method_names(self):
        method_name1 = 'tests.unit.stub_sut'
        method_name2 = 'inspect'
        func = TestClassWithExternalDependency().test_call_external_dependencies

        result = monitor(func, target_methods=[method_name1, method_name2])
        methods = result.all_methods()

        self.assertEqual(len(methods), 7)
        self.assertEqual(len(result.all_calls()), 7)

        self.assertEqual(methods[0].info.full_name,
                         'tests.unit.stub_sut.ClassWithExternalDependency.call_external_dependencies')
        self.assertEqual(methods[1].info.full_name,
                         'tests.unit.stub_sut.ClassWithExternalDependency.str_split')
        self.assertEqual(methods[2].info.full_name,
                         'tests.unit.stub_sut.ClassWithExternalDependency.time_time')
        self.assertEqual(methods[3].info.full_name,
                         'tests.unit.stub_sut.ClassWithExternalDependency.os_isdir')
        self.assertEqual(methods[4].info.full_name,
                         'tests.unit.stub_sut.ClassWithExternalDependency.os_realpath')
        self.assertEqual(methods[5].info.full_name,
                         'tests.unit.stub_sut.ClassWithExternalDependency.inspect_ismethod')
        self.assertEqual(methods[6].info.full_name,
                         'inspect.ismethod')

    def test_filter_by_file_name(self):
        file_name = 'stub_sut'
        func = TestClassWithExternalDependency().test_call_external_dependencies

        result = monitor(func, target_files=[file_name])
        methods = result.all_methods()

        self.assertEqual(len(methods), 9)
        self.assertEqual(len(result.all_calls()), 9)

        self.assertEqual(methods[0].info.full_name,
                         'tests.unit.stub_sut.ClassWithExternalDependency.call_external_dependencies')
        self.assertEqual(methods[1].info.full_name,
                         'tests.unit.stub_sut.ClassWithExternalDependency.str_split')
        self.assertEqual(methods[2].info.full_name,
                         'tests.unit.stub_sut.ClassWithExternalDependency.time_time')
        self.assertEqual(methods[3].info.full_name,
                         'tests.unit.stub_sut.ClassWithExternalDependency.os_isdir')
        self.assertEqual(methods[4].info.full_name,
                         'genericpath.isdir')
        self.assertEqual(methods[5].info.full_name,
                         'tests.unit.stub_sut.ClassWithExternalDependency.os_realpath')
        self.assertEqual(methods[6].info.full_name,
                         'posixpath.realpath')
        self.assertEqual(methods[7].info.full_name,
                         'tests.unit.stub_sut.ClassWithExternalDependency.inspect_ismethod')
        self.assertEqual(methods[8].info.full_name,
                         'inspect.ismethod')

    def test_filter_by_file_name_genericpath(self):
        file_name = 'genericpath'
        func = TestClassWithExternalDependency().test_call_external_dependencies

        result = monitor(func, target_files=[file_name])
        methods = result.all_methods()

        self.assertEqual(len(methods), 1)
        self.assertEqual(len(result.all_calls()), 1)

        self.assertEqual(methods[0].info.full_name, 'genericpath.isdir')

    def test_filter_by_file_name_posixpath(self):
        file_name = 'posixpath'
        func = TestClassWithExternalDependency().test_call_external_dependencies

        result = monitor(func, target_files=[file_name])
        methods = result.all_methods()

        self.assertGreaterEqual(len(methods), 5)

    def test_filter_by_file_name_inspect(self):
        file_name = 'inspect'
        func = TestClassWithExternalDependency().test_call_external_dependencies

        result = monitor(func, target_files=[file_name])
        methods = result.all_methods()

        self.assertEqual(len(methods), 1)
        self.assertEqual(len(result.all_calls()), 1)

        self.assertEqual(methods[0].info.full_name, 'inspect.ismethod')

    def test_filter_by_multiple_file_names(self):
        file_name1 = 'genericpath'
        file_name2 = 'inspect'
        func = TestClassWithExternalDependency().test_call_external_dependencies

        result = monitor(func, target_files=[file_name1, file_name2])
        methods = result.all_methods()

        self.assertEqual(len(methods), 2)
        self.assertEqual(len(result.all_calls()), 2)

        self.assertEqual(methods[0].info.full_name, 'genericpath.isdir')
        self.assertEqual(methods[1].info.full_name, 'inspect.ismethod')


if __name__ == '__main__':
    unittest.main()
