import os
import sys
import unittest

import pytest

from spotflow.api import monitor_func, monitor_unittest_testcase
from spotflow.finder import find_test_id
from tests.unit import stub_unittest_tests

UNITTEST_MODULE = 'tests.unit.stub_unittest_tests'
PYTEST_MODULE = 'tests.unit.stub_pytest_tests'
PYTEST_FILE = os.path.join(os.path.dirname(__file__), 'stub_pytest_tests.py')
SUT = 'tests.unit.stub_sut'
SUT_METHOD = 'tests.unit.stub_sut.SimpleCall.simple_if'


def run_pytest(test_name=None):
    path = PYTEST_FILE + '::' + test_name if test_name else PYTEST_FILE
    pytest.main(['-q', '-p', 'no:cacheprovider', path])


def traced_test_ids(func, module_name):
    """Run func under a tracer and return the test ids seen at call events, without the module name."""
    found = []

    def trace(frame, event, arg):
        if event == 'call':
            test = find_test_id(frame)
            if test:
                found.append(test)
        return None

    previous = sys.gettrace()
    sys.settrace(trace)
    try:
        func()
    finally:
        sys.settrace(previous)
    return [name.split(module_name + '.', 1)[-1] for name in found]


def found_unittest_tests(test_class, method_name):
    test = test_class(method_name)
    return traced_test_ids(lambda: test.run(unittest.TestResult()), UNITTEST_MODULE)


def found_pytest_tests(test_name):
    return traced_test_ids(lambda: run_pytest(test_name), PYTEST_MODULE)


class TestFindUnittestTest(unittest.TestCase):

    def test_snake_case(self):
        self.assertEqual(found_unittest_tests(stub_unittest_tests.Sample, 'test_snake_case'), ['Sample.test_snake_case'])

    def test_camel_case(self):
        self.assertEqual(found_unittest_tests(stub_unittest_tests.Sample, 'testCamelCase'), ['Sample.testCamelCase'])

    def test_decorated(self):
        self.assertEqual(found_unittest_tests(stub_unittest_tests.Sample, 'test_decorated'), ['Sample.test_decorated'])

    def test_generated(self):
        self.assertEqual(found_unittest_tests(stub_unittest_tests.Sample, 'test_generated'), ['Sample.test_generated'])

    def test_inherited_uses_running_class(self):
        self.assertEqual(found_unittest_tests(stub_unittest_tests.Sample, 'test_inherited'), ['Sample.test_inherited'])
        self.assertEqual(found_unittest_tests(stub_unittest_tests.Base, 'test_inherited'), ['Base.test_inherited'])

    def test_nested_function_is_not_a_test(self):
        self.assertEqual(found_unittest_tests(stub_unittest_tests.Sample, 'test_with_nested_function'),
                         ['Sample.test_with_nested_function'])

    def test_helper_method_is_not_a_test(self):
        self.assertEqual(found_unittest_tests(stub_unittest_tests.Sample, 'test_calls_helper'), ['Sample.test_calls_helper'])


class TestFindPytestTest(unittest.TestCase):

    def test_function(self):
        self.assertEqual(found_pytest_tests('test_function'), ['test_function'])

    def test_decorated(self):
        # The wrapper and the function it decorates are the same test
        self.assertEqual(found_pytest_tests('test_decorated'), ['test_decorated', 'test_decorated'])

    def test_parametrized_cases_get_own_ids(self):
        self.assertEqual(found_pytest_tests('test_parametrized'),
                         ['test_parametrized[a/b]', 'test_parametrized[c.d]'])

    def test_method_in_class(self):
        self.assertEqual(found_pytest_tests('TestClass::test_method'), ['TestClass.test_method'])

    def test_nested_function_is_not_a_test(self):
        self.assertEqual(found_pytest_tests('test_with_nested_function'), ['test_with_nested_function'])

    def test_helper_function_is_not_a_test(self):
        self.assertEqual(found_pytest_tests('test_calls_helper'), ['test_calls_helper'])


class TestCollectUnittestTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.program = monitor_unittest_testcase(stub_unittest_tests.Sample, [SUT])
        cls.calls = {call.test_fullname(): call for call in cls.program[SUT_METHOD].calls}

    def test_all_tests_are_collected(self):
        names = ['test_snake_case', 'testCamelCase', 'test_decorated', 'test_generated', 'test_inherited',
                 'test_with_nested_function', 'test_with_lambda', 'test_calls_helper', 'test_no_sut_call']
        expected = sorted(f'{UNITTEST_MODULE}.Sample.{name}' for name in names)
        self.assertEqual(sorted(self.program.tests), expected)

    def test_test_info(self):
        info = self.program.tests[f'{UNITTEST_MODULE}.Sample.test_inherited']
        self.assertEqual(info.full_name, f'{UNITTEST_MODULE}.Base.test_inherited')

    def test_calls_know_their_test(self):
        names = ['test_snake_case', 'testCamelCase', 'test_decorated', 'test_inherited',
                 'test_with_nested_function', 'test_with_lambda', 'test_calls_helper']
        expected = sorted(f'{UNITTEST_MODULE}.Sample.{name}' for name in names)
        self.assertEqual(sorted(self.calls), expected)
        self.assertEqual(self.program[SUT_METHOD].tests(), set(expected))
        self.assertEqual(self.program[SUT_METHOD].info.total_tests, len(expected))

    def test_test_name(self):
        call = self.calls[f'{UNITTEST_MODULE}.Sample.testCamelCase']
        self.assertTrue(call.is_called_by_test())
        self.assertEqual(call.tests, (f'{UNITTEST_MODULE}.Sample.testCamelCase',))
        self.assertEqual(call.test_name(), 'testCamelCase')

    def test_test_id_is_in_call_stack(self):
        call = self.calls[f'{UNITTEST_MODULE}.Sample.test_inherited']
        self.assertIn(f'{UNITTEST_MODULE}.Sample.test_inherited', call.call_stack)
        self.assertNotIn(f'{UNITTEST_MODULE}.Base.test_inherited', call.call_stack)

    def test_directly_called_by_test(self):
        self.assertTrue(self.calls[f'{UNITTEST_MODULE}.Sample.testCamelCase'].is_directly_called_by_test())
        self.assertFalse(self.calls[f'{UNITTEST_MODULE}.Sample.test_calls_helper'].is_directly_called_by_test())

    def test_unnamed_frame_does_not_end_the_call_stack(self):
        # The lambda between the test and the call is skipped
        call = self.calls[f'{UNITTEST_MODULE}.Sample.test_with_lambda']
        self.assertEqual(call.call_stack[-2:], (f'{UNITTEST_MODULE}.Sample.test_with_lambda', 'simple_if'))


class TestCollectPytestTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.program = monitor_func(run_pytest, [SUT])
        cls.calls = {call.test_fullname(): call for call in cls.program[SUT_METHOD].calls}

    def test_all_tests_are_collected(self):
        names = ['test_function', 'test_decorated', 'test_parametrized[a/b]', 'test_parametrized[c.d]',
                 'test_with_nested_function', 'test_calls_helper', 'TestClass.test_method']
        expected = sorted(f'{PYTEST_MODULE}.{name}' for name in names)
        self.assertEqual(sorted(self.program.tests), expected)
        self.assertEqual(sorted(self.calls), expected)

    def test_parametrized_test_name(self):
        call = self.calls[f'{PYTEST_MODULE}.test_parametrized[c.d]']
        self.assertEqual(call.test_name(), 'test_parametrized[c.d]')

    def test_method_test_name(self):
        call = self.calls[f'{PYTEST_MODULE}.TestClass.test_method']
        self.assertEqual(call.test_name(), 'test_method')


class TestNoTest(unittest.TestCase):

    def test_call_outside_a_test_run(self):
        from tests.unit.stub_sut import SimpleCall
        program = monitor_func(lambda: SimpleCall().simple_if(), [SUT])
        call = program[SUT_METHOD].calls[0]
        self.assertFalse(call.is_called_by_test())
        self.assertEqual(call.test_fullname(), '')
        self.assertEqual(call.test_name(), '')
        self.assertFalse(call.is_directly_called_by_test())


if __name__ == '__main__':
    unittest.main()
