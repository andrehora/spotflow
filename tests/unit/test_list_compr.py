import unittest
from tests.unit.stub_test import TComprehension
from spotflow.api import monitor_func


class TestComprehensionCall(unittest.TestCase):

    def test_listcomp_1(self):
        method_name = 'tests.unit.stub_sut.Comprehension.listcomp_1'
        func = TComprehension().test_listcomp_1

        result = monitor_func(func, [method_name])

        self.assertEqual(len(result), 1)
        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [315, 315, 315, 315, 315, 315, 315, 315, 315, 315, 315])
        self.assertEqual(calls[0].distinct_run_lines(), [315])

    def test_listcomp_2(self):
        method_name = 'tests.unit.stub_sut.Comprehension.listcomp_2'
        func = TComprehension().test_listcomp_2

        result = monitor_func(func, [method_name])

        self.assertEqual(len(result), 1)
        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [318, 318, 318, 318, 318, 318, 318, 318, 318, 318, 318])
        self.assertEqual(calls[0].distinct_run_lines(), [318])

    def test_setcomp_1(self):
        method_name = 'tests.unit.stub_sut.Comprehension.setcomp_1'
        func = TComprehension().test_setcomp_1

        result = monitor_func(func, [method_name])

        self.assertEqual(len(result), 1)
        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [321, 321, 321, 321, 321, 321, 321, 321, 321, 321, 321])
        self.assertEqual(calls[0].distinct_run_lines(), [321])

    def test_setcomp_2(self):
        method_name = 'tests.unit.stub_sut.Comprehension.setcomp_2'
        func = TComprehension().test_setcomp_2

        result = monitor_func(func, [method_name])

        self.assertEqual(len(result), 1)
        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [324, 324, 324, 324, 324, 324, 324, 324, 324, 324, 324])
        self.assertEqual(calls[0].distinct_run_lines(), [324])

    def test_dictcomp(self):
        method_name = 'tests.unit.stub_sut.Comprehension.dictcomp'
        func = TComprehension().test_dictcomp

        result = monitor_func(func, [method_name])

        self.assertEqual(len(result), 1)
        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [327, 327, 327, 327, 327, 327, 327, 327, 327, 327, 327])
        self.assertEqual(calls[0].distinct_run_lines(), [327])


if __name__ == '__main__':
    unittest.main()