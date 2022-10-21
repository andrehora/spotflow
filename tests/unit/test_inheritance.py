import unittest
from tests.unit.stub_test import TestSuper, TestMoreSuper, TestOverride
from spotflow.api import monitor


class TestSuperCall(unittest.TestCase):

    def test_super_init_a(self):
        method_name = 'tests.unit.stub_sut'
        func = TestSuper().test_super_init_a

        result = monitor(func, [method_name])

        self.assertEqual(len(result), 1)

        calls = result['tests.unit.stub_sut.ClassA.__init__'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [428, 429])

    def test_super_init_b(self):
        method_name = 'tests.unit.stub_sut'
        func = TestSuper().test_super_init_b

        result = monitor(func, [method_name])

        self.assertEqual(len(result), 2)

        calls = result['tests.unit.stub_sut.ClassB.__init__'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [438, 439])

        calls = result['tests.unit.stub_sut.ClassA.__init__'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [428, 429])

    def test_super_init_c(self):
        method_name = 'tests.unit.stub_sut'
        func = TestSuper().test_super_init_c

        result = monitor(func, [method_name])

        self.assertEqual(len(result), 3)

        calls = result['tests.unit.stub_sut.ClassC.__init__'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [450, 451])

        calls = result['tests.unit.stub_sut.ClassB.__init__'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [438, 439])

        calls = result['tests.unit.stub_sut.ClassA.__init__'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [428, 429])

    def test_super_init_d(self):
        method_name = 'tests.unit.stub_sut'
        func = TestSuper().test_super_init_d

        result = monitor(func, [method_name])

        self.assertEqual(len(result), 3)

        calls = result['tests.unit.stub_sut.ClassD.__init__'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [461, 462])

        calls = result['tests.unit.stub_sut.ClassB.__init__'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [438, 439])

        calls = result['tests.unit.stub_sut.ClassA.__init__'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [428, 429])

    def test_super_foobar_a(self):
        method_name = 'tests.unit.stub_sut.ClassA.foobar'
        func = TestSuper().test_super_foobar_a

        result = monitor(func, [method_name])

        self.assertEqual(len(result), 1)

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [432])

    def test_super_foobar_b(self):
        method_name = 'tests.unit.stub_sut'
        func = TestSuper().test_super_foobar_b

        result = monitor(func, [method_name])

        self.assertEqual(len(result), 4)

        calls = result['tests.unit.stub_sut.ClassB.foobar'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [442, 443, 444])

        calls = result['tests.unit.stub_sut.ClassA.foobar'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [432])

        calls = result['tests.unit.stub_sut.ClassB.__init__'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [438, 439])

        calls = result['tests.unit.stub_sut.ClassA.__init__'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [428, 429])

    def test_super_foobar_c(self):
        method_name = 'tests.unit.stub_sut'
        func = TestSuper().test_super_foobar_c

        result = monitor(func, [method_name])

        self.assertEqual(len(result), 6)

        calls = result['tests.unit.stub_sut.ClassC.foobar'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [454, 455])

        calls = result['tests.unit.stub_sut.ClassB.foobar'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [442, 443, 444])

        calls = result['tests.unit.stub_sut.ClassA.foobar'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [432])

        calls = result['tests.unit.stub_sut.ClassC.__init__'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [450, 451])

        calls = result['tests.unit.stub_sut.ClassB.__init__'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [438, 439])

        calls = result['tests.unit.stub_sut.ClassA.__init__'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [428, 429])


class TestMoreSuperCall(unittest.TestCase):

    def test_super_1(self):
        method_name = 'tests.unit.stub_sut'
        func = TestMoreSuper().test_super_1

        result = monitor(func, [method_name])

        self.assertEqual(len(result), 2)

        calls = result['tests.unit.stub_sut.ClassSuper1.__init__'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [505, 506, 507])

        calls = result['tests.unit.stub_sut.ClassSuper1.foobar'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [510, 511])

    def test_super_2(self):
        method_name = 'tests.unit.stub_sut'
        func = TestMoreSuper().test_super_2

        result = monitor(func, [method_name])

        self.assertEqual(len(result), 3)

        calls = result['tests.unit.stub_sut.ClassSuper2.__init__'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [517])

        calls = result['tests.unit.stub_sut.ClassSuper1.__init__'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [505, 506, 507])

        calls = result['tests.unit.stub_sut.ClassSuper1.foobar'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [510, 511])

    def test_super_3(self):
        method_name = 'tests.unit.stub_sut'
        func = TestMoreSuper().test_super_3

        result = monitor(func, [method_name])

        self.assertEqual(len(result), 4)

        calls = result['tests.unit.stub_sut.ClassSuper2.__init__'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [517])

        calls = result['tests.unit.stub_sut.ClassSuper1.__init__'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [505, 506, 507])

        calls = result['tests.unit.stub_sut.ClassSuper3.foobar'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [523])

        calls = result['tests.unit.stub_sut.ClassSuper1.foobar'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [510, 511])


class TestOverrideCall(unittest.TestCase):

    def test_base_class_main(self):
        method_name = 'tests.unit.stub_sut.BaseClass.main'
        func = TestOverride().test_base_class_main

        result = monitor(func, [method_name])

        self.assertEqual(len(result), 1)

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [472])

    def test_base_class_show(self):
        method_name = 'tests.unit.stub_sut.BaseClass.show'
        func = TestOverride().test_base_class_show

        result = monitor(func, [method_name])

        self.assertEqual(len(result), 1)

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [475])

    def test_base_class_report(self):
        method_name = 'tests.unit.stub_sut.BaseClass.report'
        func = TestOverride().test_base_class_report

        result = monitor(func, [method_name])

        self.assertEqual(len(result), 1)

        calls = result[method_name].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [478])

    def test_override_show(self):
        method_name = 'tests.unit.stub_sut'
        func = TestOverride().test_override_show

        result = monitor(func, [method_name])

        self.assertEqual(len(result), 2)

        calls = result['tests.unit.stub_sut.OverrideShow.show'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [484])

        calls = result['tests.unit.stub_sut.BaseClass.main'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [472])

    def test_override_main(self):
        method_name = 'tests.unit.stub_sut'
        func = TestOverride().test_override_main

        result = monitor(func, [method_name])

        self.assertEqual(len(result), 2)

        calls = result['tests.unit.stub_sut.OverrideMain.main'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [490])

        calls = result['tests.unit.stub_sut.BaseClass.report'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [478])

    def test_override_main_and_report(self):
        method_name = 'tests.unit.stub_sut'
        func = TestOverride().test_override_main_and_report

        result = monitor(func, [method_name])

        self.assertEqual(len(result), 3)

        calls = result['tests.unit.stub_sut.OverrideMainAndReport.main'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [496])

        calls = result['tests.unit.stub_sut.OverrideMainAndReport.report'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [499])

        calls = result['tests.unit.stub_sut.BaseClass.show'].calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].run_lines, [475])


if __name__ == '__main__':
    unittest.main()
