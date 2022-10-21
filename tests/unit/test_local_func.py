import unittest
from tests.unit.stub_test import TestLocalMethod, TestLocalFunction
from spotflow.api import monitor


class TestLocalMethodCall(unittest.TestCase):

    def test_has_local_method_1(self):
        method_name = 'tests.unit.stub_sut.LocalMethod.has_local_method_1'
        func = TestLocalMethod().test_has_local_method_1

        result = monitor(func, [method_name])

        self.assertEqual(len(result), 1)
        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        self.assertEqual(calls[0].run_lines, [333, 334, 336])

    def test_has_local_method_2(self):
        method_name = 'tests.unit.stub_sut.LocalMethod.has_local_method_2'
        func = TestLocalMethod().test_has_local_method_2

        result = monitor(func, [method_name])
        self.assertEqual(len(result), 2)

        calls = result['tests.unit.stub_sut.LocalMethod.has_local_method_2'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [340, 341, 343, 346, 347])

        calls = result['tests.unit.stub_sut.LocalMethod.has_local_method_2.<locals>.local_method'].calls
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0].run_lines, [344])
        self.assertEqual(calls[1].run_lines, [344])

    def test_has_local_method_3(self):
        method_name = 'tests.unit.stub_sut.LocalMethod.has_local_method_3'
        func = TestLocalMethod().test_has_local_method_3

        result = monitor(func, [method_name])
        self.assertEqual(len(result), 3)

        calls = result['tests.unit.stub_sut.LocalMethod.has_local_method_3'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [350, 351, 353, 356, 359, 360])

        calls = result['tests.unit.stub_sut.LocalMethod.has_local_method_3.<locals>.local_method_1'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [354])

        calls = result['tests.unit.stub_sut.LocalMethod.has_local_method_3.<locals>.local_method_2'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [357])

    def test_has_local_method_4(self):
        method_name = 'tests.unit.stub_sut.LocalMethod.has_local_method_4'
        func = TestLocalMethod().test_has_local_method_4

        result = monitor(func, [method_name])
        self.assertEqual(len(result), 3)

        calls = result['tests.unit.stub_sut.LocalMethod.has_local_method_4'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [363, 364, 366, 374])

        calls = result['tests.unit.stub_sut.LocalMethod.has_local_method_4.<locals>.local_method_1'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [368, 371, 372])

        # Very nested case
        calls = result['tests.unit.stub_sut.LocalMethod.has_local_method_4.<locals>.local_method_1.<locals>.local_method_2'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [369])


class TestLocalFunctionCall(unittest.TestCase):

    def test_has_local_method_1(self):
        method_name = 'tests.unit.stub_sut.has_local_function_1'
        func = TestLocalFunction().test_has_local_function_1

        result = monitor(func, [method_name])

        self.assertEqual(len(result), 1)
        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)

        self.assertEqual(calls[0].run_lines, [378, 379, 381])

    def test_has_local_function_2(self):
        method_name = 'tests.unit.stub_sut.has_local_function_2'
        func = TestLocalFunction().test_has_local_function_2

        result = monitor(func, [method_name])
        self.assertEqual(len(result), 2)

        calls = result['tests.unit.stub_sut.has_local_function_2'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [386, 387, 389, 392, 393])

        calls = result['tests.unit.stub_sut.has_local_function_2.<locals>.local_function'].calls
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0].run_lines, [390])
        self.assertEqual(calls[1].run_lines, [390])

    def test_has_local_function_3(self):
        method_name = 'tests.unit.stub_sut.has_local_function_3'
        func = TestLocalFunction().test_has_local_function_3

        result = monitor(func, [method_name])
        self.assertEqual(len(result), 3)

        calls = result['tests.unit.stub_sut.has_local_function_3'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [397, 398, 400, 403, 406, 407])

        calls = result['tests.unit.stub_sut.has_local_function_3.<locals>.local_function_1'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [401])

        calls = result['tests.unit.stub_sut.has_local_function_3.<locals>.local_function_2'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [404])

    def test_has_local_function_4(self):
        method_name = 'tests.unit.stub_sut.has_local_function_4'
        func = TestLocalFunction().test_has_local_function_4

        result = monitor(func, [method_name])
        self.assertEqual(len(result), 3)

        calls = result['tests.unit.stub_sut.has_local_function_4'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [411, 412, 414, 422])

        calls = result['tests.unit.stub_sut.has_local_function_4.<locals>.local_function_1'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [416, 419, 420])

        # Very nested case
        calls = result['tests.unit.stub_sut.has_local_function_4.<locals>.local_function_1.<locals>.local_function_2'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [417])


if __name__ == '__main__':
    unittest.main()
