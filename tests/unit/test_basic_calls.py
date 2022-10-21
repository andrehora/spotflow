import unittest
from tests.unit.stub_test import TestSimpleCall, TestComplexCall
from spotflow.api import monitor


class TestCallForFunctions(unittest.TestCase):

    def test_simple_if_true(self):
        method_name = 'tests.unit.stub_sut.SimpleCall.simple_if'
        func = TestSimpleCall().test_simple_if_true

        result = monitor(func, [method_name])

        self.assertEqual(result[method_name].calls[0].run_lines, [4, 5])
        self.assertEqual(result[method_name].name, 'simple_if')

    def test_simple_if_false(self):
        method_name = 'tests.unit.stub_sut.SimpleCall.simple_if'
        func = TestSimpleCall().test_simple_if_false

        result = monitor(func, [method_name])

        self.assertEqual(result[method_name].calls[0].run_lines, [4])
        self.assertEqual(result[method_name].name, 'simple_if')

    def test_simple_if_else_true_and_false(self):
        method_name = 'tests.unit.stub_sut.SimpleCall.simple_if_else'
        func = TestSimpleCall().test_simple_if_else_true_and_false

        result = monitor(func, [method_name])

        self.assertIn([8, 9], result[method_name].calls)
        self.assertIn([8, 11], result[method_name].calls)
        self.assertEqual(result[method_name].name, 'simple_if_else')

    def test_simple_if_else_true(self):
        method_name = 'tests.unit.stub_sut.SimpleCall.simple_if_else'
        func = TestSimpleCall().test_simple_if_else_true

        result = monitor(func, [method_name])

        self.assertEqual(result[method_name].calls[0].run_lines, [8, 9])
        self.assertEqual(result[method_name].name, 'simple_if_else')

    def test_simple_if_else_false(self):
        method_name = 'tests.unit.stub_sut.SimpleCall.simple_if_else'
        func = TestSimpleCall().test_simple_if_else_false

        result = monitor(func, [method_name])

        self.assertEqual(result[method_name].calls[0].run_lines, [8, 11])
        self.assertEqual(result[method_name].name, 'simple_if_else')

    def test_TestSimpleCall(self):
        method_name = 'tests.unit.stub_sut.SimpleCall.simple_if_else'
        func = TestSimpleCall().test_simple_if_else_true_and_false

        result = monitor(func, [method_name])

        self.assertIn([8, 9], result[method_name].calls)
        self.assertIn([8, 11], result[method_name].calls)
        self.assertEqual(result[method_name].name, 'simple_if_else')

    def test_loop(self):
        method_name = 'tests.unit.stub_sut.SimpleCall.loop'
        func = TestSimpleCall().test_loop

        result = monitor(func, [method_name])

        self.assertEqual(result[method_name].calls[0].run_lines, [14, 15, 16, 15, 16, 15])
        self.assertEqual(result[method_name].calls[0].distinct_run_lines(), [14, 15, 16])
        self.assertEqual(result[method_name].name, 'loop')

    def test_try_success(self):
        method_name = 'tests.unit.stub_sut.SimpleCall.try_success'
        func = TestSimpleCall().test_try_success

        result = monitor(func, [method_name])

        self.assertEqual(result[method_name].calls[0].run_lines, [19, 20])
        self.assertEqual(result[method_name].name, 'try_success')

    def test_try_fail(self):
        method_name = 'tests.unit.stub_sut.SimpleCall.try_fail'
        func = TestSimpleCall().test_try_fail

        result = monitor(func, [method_name])

        self.assertEqual(result[method_name].calls[0].run_lines, [25, 26, 27, 28])
        self.assertEqual(result[method_name].name, 'try_fail')

    def test_single_call_to_sut_bom_dia(self):
        method_name = 'tests.unit.stub_sut.ComplexCall.hello'
        func = TestComplexCall().test_single_call_to_sut_bom_dia

        result = monitor(func, [method_name])

        self.assertEqual(result[method_name].calls[0].run_lines, [35, 39])
        self.assertEqual(result[method_name].name, 'hello')

    def test_single_call_to_sut_boa_tarde(self):
        method_name = 'tests.unit.stub_sut.ComplexCall.hello'
        func = TestComplexCall().test_single_call_to_sut_boa_tarde

        result = monitor(func, [method_name])

        self.assertEqual(result[method_name].calls[0].run_lines, [35, 36, 38])
        self.assertEqual(result[method_name].name, 'hello')

    def test_single_call_to_sut_boa_noite(self):
        method_name = 'tests.unit.stub_sut.ComplexCall.hello'
        func = TestComplexCall().test_single_call_to_sut_boa_noite

        result = monitor(func, [method_name])

        self.assertEqual(result[method_name].calls[0].run_lines, [35, 36, 37])
        self.assertEqual(result[method_name].name, 'hello')

    def test_multiple_call_to_sut(self):
        method_name = 'tests.unit.stub_sut.ComplexCall.hello'
        func = TestComplexCall().test_multiple_call_to_sut

        result = monitor(func, [method_name])

        self.assertEqual(len(result[method_name].calls), 3)
        self.assertIn([35, 39], result[method_name].calls)
        self.assertIn([35, 36, 38], result[method_name].calls)
        self.assertIn([35, 36, 37], result[method_name].calls)
        self.assertEqual(result[method_name].name, 'hello')


class TestCallForContainers(unittest.TestCase):

    def test_TestSimpleCall(self):
        method_name = 'tests.unit.stub_sut.SimpleCall'
        func = TestSimpleCall().run_all

        result = monitor(func, [method_name])

        self.assertEqual(len(result), 5)

        method_name = 'tests.unit.stub_sut'
        func = TestSimpleCall().run_all

        result = monitor(func, [method_name])

        self.assertEqual(len(result), 5)

    def test_TestComplexCall(self):
        method_name = 'tests.unit.stub_sut.ComplexCall'
        func = TestComplexCall().run_all

        result = monitor(func, [method_name])

        self.assertEqual(len(result), 5)

        method_name = 'tests.unit.stub_sut'
        func = TestComplexCall().run_all

        result = monitor(func, [method_name])

        self.assertEqual(len(result), 5)

    def test_sut_call_sut(self):
        method_name = 'tests.unit.stub_sut'
        func = TestComplexCall().test_sut_call_sut

        result = monitor(func, [method_name])

        method_name = 'tests.unit.stub_sut.ComplexCall.func'
        self.assertEqual(result[method_name].calls[0].run_lines, [42, 43, 44])
        self.assertEqual(result[method_name].name, 'func')

        method_name = 'tests.unit.stub_sut.ComplexCall.f1'
        self.assertEqual(result[method_name].calls[0].run_lines, [47])
        self.assertEqual(result[method_name].name, 'f1')

        method_name = 'tests.unit.stub_sut.ComplexCall.f2'
        self.assertEqual(result[method_name].calls[0].run_lines, [50])
        self.assertEqual(result[method_name].name, 'f2')

        method_name = 'tests.unit.stub_sut.ComplexCall.f3'
        self.assertEqual(result[method_name].calls[0].run_lines, [53])
        self.assertEqual(result[method_name].name, 'f3')


if __name__ == '__main__':
    unittest.main()