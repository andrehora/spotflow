import unittest
from tests.stub_test import TestSuper, TestMoreSuper, TestOverride
from happyflow.api import run_and_flow_func


class TestSuperFlow(unittest.TestCase):

    def test_super_init_a(self):
        target_entity_name = 'tests.stub_sut'
        func = TestSuper().test_super_init_a

        result = run_and_flow_func(func, [target_entity_name])

        self.assertEqual(len(result), 1)

        flows = result['tests.stub_sut.ClassA.__init__'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [428, 429])

    def test_super_init_b(self):
        target_entity_name = 'tests.stub_sut'
        func = TestSuper().test_super_init_b

        result = run_and_flow_func(func, [target_entity_name])

        self.assertEqual(len(result), 2)

        flows = result['tests.stub_sut.ClassB.__init__'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [438, 439])

        flows = result['tests.stub_sut.ClassA.__init__'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [428, 429])

    def test_super_init_c(self):
        target_entity_name = 'tests.stub_sut'
        func = TestSuper().test_super_init_c

        result = run_and_flow_func(func, [target_entity_name])

        self.assertEqual(len(result), 3)

        flows = result['tests.stub_sut.ClassC.__init__'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [450, 451])

        flows = result['tests.stub_sut.ClassB.__init__'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [438, 439])

        flows = result['tests.stub_sut.ClassA.__init__'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [428, 429])

    def test_super_init_d(self):
        target_entity_name = 'tests.stub_sut'
        func = TestSuper().test_super_init_d

        result = run_and_flow_func(func, [target_entity_name])

        self.assertEqual(len(result), 3)

        flows = result['tests.stub_sut.ClassD.__init__'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [461, 462])

        flows = result['tests.stub_sut.ClassB.__init__'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [438, 439])

        flows = result['tests.stub_sut.ClassA.__init__'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [428, 429])

    def test_super_foobar_a(self):
        target_entity_name = 'tests.stub_sut.ClassA.foobar'
        func = TestSuper().test_super_foobar_a

        result = run_and_flow_func(func, [target_entity_name])

        self.assertEqual(len(result), 1)

        flows = result[target_entity_name].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [432])

    def test_super_foobar_b(self):
        target_entity_name = 'tests.stub_sut'
        func = TestSuper().test_super_foobar_b

        result = run_and_flow_func(func, [target_entity_name])

        self.assertEqual(len(result), 4)

        flows = result['tests.stub_sut.ClassB.foobar'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [442, 443, 444])

        flows = result['tests.stub_sut.ClassA.foobar'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [432])

        flows = result['tests.stub_sut.ClassB.__init__'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [438, 439])

        flows = result['tests.stub_sut.ClassA.__init__'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [428, 429])

    def test_super_foobar_c(self):
        target_entity_name = 'tests.stub_sut'
        func = TestSuper().test_super_foobar_c

        result = run_and_flow_func(func, [target_entity_name])

        self.assertEqual(len(result), 6)

        flows = result['tests.stub_sut.ClassC.foobar'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [454, 455])

        flows = result['tests.stub_sut.ClassB.foobar'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [442, 443, 444])

        flows = result['tests.stub_sut.ClassA.foobar'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [432])

        flows = result['tests.stub_sut.ClassC.__init__'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [450, 451])

        flows = result['tests.stub_sut.ClassB.__init__'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [438, 439])

        flows = result['tests.stub_sut.ClassA.__init__'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [428, 429])


class TestMoreSuperFlow(unittest.TestCase):

    def test_super_1(self):
        target_entity_name = 'tests.stub_sut'
        func = TestMoreSuper().test_super_1

        result = run_and_flow_func(func, [target_entity_name])

        self.assertEqual(len(result), 2)

        flows = result['tests.stub_sut.ClassSuper1.__init__'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [505, 506, 507])

        flows = result['tests.stub_sut.ClassSuper1.foobar'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [510, 511])

    def test_super_2(self):
        target_entity_name = 'tests.stub_sut'
        func = TestMoreSuper().test_super_2

        result = run_and_flow_func(func, [target_entity_name])

        self.assertEqual(len(result), 3)

        flows = result['tests.stub_sut.ClassSuper2.__init__'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [517])

        flows = result['tests.stub_sut.ClassSuper1.__init__'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [505, 506, 507])

        flows = result['tests.stub_sut.ClassSuper1.foobar'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [510, 511])

    def test_super_3(self):
        target_entity_name = 'tests.stub_sut'
        func = TestMoreSuper().test_super_3

        result = run_and_flow_func(func, [target_entity_name])

        self.assertEqual(len(result), 4)

        flows = result['tests.stub_sut.ClassSuper2.__init__'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [517])

        flows = result['tests.stub_sut.ClassSuper1.__init__'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [505, 506, 507])

        flows = result['tests.stub_sut.ClassSuper3.foobar'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [523])

        flows = result['tests.stub_sut.ClassSuper1.foobar'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [510, 511])


class TestOverrideFlow(unittest.TestCase):

    def test_base_class_main(self):
        target_entity_name = 'tests.stub_sut.BaseClass.main'
        func = TestOverride().test_base_class_main

        result = run_and_flow_func(func, [target_entity_name])

        self.assertEqual(len(result), 1)

        flows = result[target_entity_name].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [472])

    def test_base_class_show(self):
        target_entity_name = 'tests.stub_sut.BaseClass.show'
        func = TestOverride().test_base_class_show

        result = run_and_flow_func(func, [target_entity_name])

        self.assertEqual(len(result), 1)

        flows = result[target_entity_name].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [475])

    def test_base_class_report(self):
        target_entity_name = 'tests.stub_sut.BaseClass.report'
        func = TestOverride().test_base_class_report

        result = run_and_flow_func(func, [target_entity_name])

        self.assertEqual(len(result), 1)

        flows = result[target_entity_name].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [478])

    def test_override_show(self):
        target_entity_name = 'tests.stub_sut'
        func = TestOverride().test_override_show

        result = run_and_flow_func(func, [target_entity_name])

        self.assertEqual(len(result), 2)

        flows = result['tests.stub_sut.OverrideShow.show'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [484])

        flows = result['tests.stub_sut.BaseClass.main'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [472])

    def test_override_main(self):
        target_entity_name = 'tests.stub_sut'
        func = TestOverride().test_override_main

        result = run_and_flow_func(func, [target_entity_name])

        self.assertEqual(len(result), 2)

        flows = result['tests.stub_sut.OverrideMain.main'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [490])

        flows = result['tests.stub_sut.BaseClass.report'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [478])

    def test_override_main_and_report(self):
        target_entity_name = 'tests.stub_sut'
        func = TestOverride().test_override_main_and_report

        result = run_and_flow_func(func, [target_entity_name])

        self.assertEqual(len(result), 3)

        flows = result['tests.stub_sut.OverrideMainAndReport.main'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [496])

        flows = result['tests.stub_sut.OverrideMainAndReport.report'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [499])

        flows = result['tests.stub_sut.BaseClass.show'].flows
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0].run_lines, [475])


if __name__ == '__main__':
    unittest.main()
