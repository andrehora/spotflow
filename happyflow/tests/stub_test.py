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

    def test_keep_var_state(self):
        self.states.keep_var_state()


class TestReturnValue(unittest.TestCase):

    def setUp(self):
        self.ret = ReturnValue()

    def test_simple_return_local(self):
        return_value = ReturnValue()
        return_value.simple_return()

    def test_simple_return_global(self):
        self.ret.simple_return()

    def test_simple_return_with_arg(self):
        self.ret.simple_return_with_arg('hello', 'world')

    def test_change_return_0(self):
        self.ret.change_return_0(100, 200)

    def test_change_return_1(self):
        self.ret.change_return_1()

    def test_change_return_2(self):
        self.ret.change_return_2()

    def test_change_return_3(self):
        self.ret.change_return_3()

    def test_change_return_4(self):
        self.ret.change_return_4()

    def test_change_return_5(self):
        self.ret.change_return_5()

    def test_multiple_return_true(self):
        self.ret.multiple_return(True)

    def test_multiple_return_false(self):
        self.ret.multiple_return(False)

    def test_change_attribute_0(self):
        self.ret.change_attribute_0(500)

    def test_change_attribute_1(self):
        self.ret.change_attribute_1()

    def test_change_attribute_2(self):
        self.ret.change_attribute_2()

    def test_change_attribute_3(self):
        self.ret.change_attribute_3()

    def test_change_obj_1(self):
        self.ret.change_obj_1()

    def test_change_obj_2(self):
        self.ret.change_obj_2(10, 10, 1)

    def test_change_obj_3(self):
        self.ret.change_obj_3()

    def test_explicit_return_value(self):
        self.ret.explicit_return_value()

    def test_explicit_return_none(self):
        self.ret.explicit_return_none()

    def test_explicit_return(self):
        self.ret.explicit_return()

    def test_implicit_return(self):
        self.ret.implicit_return()
