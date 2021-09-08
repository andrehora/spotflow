import unittest
from happyflow.tests.stub_sut import *


class TestFoo(unittest.TestCase):

    def test_foo(self):
        pass


class TestStubBasicFlow(unittest.TestCase):

    def setUp(self):
        self.bs = StubBasicFlow()

    def test_simple_if_true(self):
        self.bs.simple_if(True)

    def test_simple_if_false(self):
        self.bs.simple_if(False)

    def test_simple_if_else_true(self):
        self.bs.simple_if_else(True)

    def test_simple_if_else_false(self):
        self.bs.simple_if_else(False)

    def test_simple_if_else_true_and_false(self):
        self.bs.simple_if_else(True)
        self.bs.simple_if_else(False)

    def test_loop(self):
        self.bs.loop()

    def test_try_success(self):
        self.bs.try_success()

    def test_try_fail(self):
        self.bs.try_fail()


class TestStubComplexFlow(unittest.TestCase):

    def setUp(self):
        self.cs = StubComplexFlow()

    def test_single_call_to_sut_bom_dia(self):
        hello = self.cs.hello(10)
        self.assertEqual(hello, 'bom dia')

    def test_single_call_to_sut_boa_tarde(self):
        hello = self.cs.hello(14)
        self.assertEqual(hello, 'boa tarde')

    def test_single_call_to_sut_boa_noite(self):
        hello = self.cs.hello(20)
        self.assertEqual(hello, 'boa noite')

    def test_multiple_call_to_sut(self):
        hello = self.cs.hello(10)
        self.assertEqual(hello, 'bom dia')

        hello = self.cs.hello(14)
        self.assertEqual(hello, 'boa tarde')

        hello = self.cs.hello(20)
        self.assertEqual(hello, 'boa noite')

    def test_sut_call_sut(self):
        self.cs.func()


class TestStubState(unittest.TestCase):

    def setUp(self):
        self.states = StubState()

    def test_change_var_state(self):
        self.states.change_var_state()

    def test_change_arg_state(self):
        self.states.change_arg_state()

    def test_change_var_state_with_conditional_true(self):
        self.states.change_var_state_with_conditional(True)

    def test_change_var_state_with_conditional_false(self):
        self.states.change_var_state_with_conditional(False)
