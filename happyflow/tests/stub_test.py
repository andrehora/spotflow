import unittest
from happyflow.tests.stub_sut import *


class TestFoo(unittest.TestCase):

    def test_foo(self):
        pass


class TestSimpleFlow(unittest.TestCase):

    def setUp(self):
        self.bs = SimpleFlow()

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


class TestComplexFlow(unittest.TestCase):

    def setUp(self):
        self.cs = ComplexFlow()

    def test_single_call_to_sut_bom_dia(self):
        self.cs.hello(10)

    def test_single_call_to_sut_boa_tarde(self):
        self.cs.hello(14)

    def test_single_call_to_sut_boa_noite(self):
        self.cs.hello(20)

    def test_multiple_call_to_sut(self):
        self.cs.hello(10)
        self.cs.hello(14)
        self.cs.hello(20)

    def test_sut_call_sut(self):
        self.cs.func()


class TestChangeState(unittest.TestCase):

    def setUp(self):
        self.states = ChangeState()

    def test_change_var_state(self):
        self.states.change_var_state()

    def test_change_arg_state(self):
        self.states.change_arg_state()

    def test_change_var_state_with_conditional_true(self):
        self.states.change_var_state_with_conditional(True)

    def test_change_var_state_with_conditional_false(self):
        self.states.change_var_state_with_conditional(False)

    def test_change_multiple_vars_states(self):
        self.states.change_multiple_vars_states()

    def test_change_list_state(self):
        self.states.change_list_state()

    def test_change_var_state_with_loop(self):
        self.states.change_var_state_with_loop()

    def test_change_instance_var(self):
        self.states.change_instance_var()

    def test_init(self):
        pass
