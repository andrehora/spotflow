from tests.unit.stub_sut import *


class TestFoo:

    def test_foo(self):
        pass


class TestSimpleCall:

    def __init__(self):
        self.bs = SimpleCall()

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

    def run_all(self):
        self.test_simple_if_true()
        self.test_simple_if_false()
        self.test_simple_if_else_true()
        self.test_simple_if_else_false()
        self.test_simple_if_else_true_and_false()
        self.test_loop()
        self.test_try_success()
        self.test_try_fail()


class TestComplexCall:

    def __init__(self):
        self.cs = ComplexCall()

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

    def run_all(self):
        self.test_single_call_to_sut_bom_dia()
        self.test_single_call_to_sut_boa_tarde()
        self.test_single_call_to_sut_boa_noite()
        self.test_multiple_call_to_sut()
        self.test_sut_call_sut()


class TestChangeState:

    def __init__(self):
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
        ChangeState()

    def test_keep_var_state(self):
        self.states.keep_var_state()


class TestReturnValue:

    def __init__(self):
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

    def test_explicit_return_state(self):
        self.ret.explicit_return_state()

    def test_explicit_return_none(self):
        self.ret.explicit_return_none()

    def test_explicit_return(self):
        self.ret.explicit_return()

    def test_implicit_return(self):
        self.ret.implicit_return()


class TestExceptions:

    def __init__(self):
        self.ex = Exceptions()

    def test_zero_division(self):
        try:
            self.ex.zero_division()
        except:
            pass

    def test_raise_generic_exception(self):
        try:
            self.ex.raise_generic_exception()
        except:
            pass

    def test_raise_specific_exception(self):
        try:
            self.ex.raise_specific_exception()
        except Exception:
            pass

    def test_raise_exception_line_1(self):
        try:
            self.ex.raise_distinct_exception(first_line=True)
        except Exception:
            pass

    def test_raise_exception_line_2(self):
        try:
            self.ex.raise_distinct_exception(second_line=True)
        except Exception:
            pass

    def test_raise_exception_line_3(self):
        try:
            self.ex.raise_distinct_exception(third_line=True)
        except Exception:
            pass

    def test_raise_no_exception(self):
        try:
            self.ex.raise_distinct_exception()
        except Exception:
            pass

    def test_calls_with_exceptions(self):
        try:
            self.ex.raise_distinct_exception(first_line=True)
        except Exception:
            pass

        try:
            self.ex.raise_distinct_exception(second_line=True)
        except Exception:
            pass

        try:
            self.ex.raise_distinct_exception(third_line=True)
        except Exception:
            pass


class TestGenerator:

    def __init__(self):
        self.g = Generators()

    def test_no_generator(self):
        self.g.no_generator()

    def test_call_generator_1(self):
        self.g.call_generator_1()

    def test_call_generator_2(self):
        self.g.call_generator_2()

    def test_call_generator_3(self):
        self.g.call_generator_3()

    def test_call_generator_4(self):
        self.g.call_generator_4()

    def test_has_generator_1(self):
        self.g.has_generator_1()

    def test_has_generator_2(self):
        self.g.has_generator_2()

    def test_has_generator_3(self):
        self.g.has_generator_3()

    def test_has_generator_4(self):
        self.g.has_generator_4()

    def run_all(self):
        self.test_no_generator()
        self.test_call_generator_1()
        self.test_call_generator_2()
        self.test_call_generator_3()
        self.test_call_generator_4()
        self.test_has_generator_1()
        self.test_has_generator_2()
        self.test_has_generator_3()
        self.test_has_generator_4()


class TestGeneratorExpression:

    def __init__(self):
        self.ge = GeneratorExpression()

    def test_generator_expression_1(self):
        self.ge.generator_expression_1()

    def test_generator_expression_2(self):
        self.ge.generator_expression_2()


class TestComprehension:

    def __init__(self):
        self.c = Comprehension()

    def test_listcomp_1(self):
        self.c.listcomp_1()

    def test_listcomp_2(self):
        self.c.listcomp_2()

    def test_setcomp_1(self):
        self.c.setcomp_1()

    def test_setcomp_2(self):
        self.c.setcomp_2()

    def test_dictcomp(self):
        self.c.dictcomp()


class TestLocalMethod:

    def __init__(self):
        self.lm = LocalMethod()

    def test_has_local_method_1(self):
        self.lm.has_local_method_1()

    def test_has_local_method_2(self):
        self.lm.has_local_method_2()

    def test_has_local_method_3(self):
        self.lm.has_local_method_3()

    def test_has_local_method_4(self):
        self.lm.has_local_method_4()


class TestLocalFunction:

    def test_has_local_function_1(self):
        has_local_function_1()

    def test_has_local_function_2(self):
        has_local_function_2()

    def test_has_local_function_3(self):
        has_local_function_3()

    def test_has_local_function_4(self):
        has_local_function_4()


class TestLocalClass:

    def test_has_local_class_1(self):
        HasLocalClass().LocalClass1().local()

    def test_has_local_class_2(self):
        HasLocalClass().has_local_class()

    def test_has_local_class_3(self):
        has_local_class()


class TestSuper:

    def test_super_init_a(self):
        ClassA(123)

    def test_super_init_b(self):
        ClassB(123)

    def test_super_init_c(self):
        ClassC(123)

    def test_super_init_d(self):
        ClassD(123)

    def test_super_foobar_a(self):
        ClassA(123).foobar(123)

    def test_super_foobar_b(self):
        ClassB(123).foobar(123)

    def test_super_foobar_c(self):
        ClassC(123).foobar(123)


class TestOverride:

    def test_base_class_main(self):
        BaseClass().main()

    def test_base_class_show(self):
        BaseClass().show()

    def test_base_class_report(self):
        BaseClass().report()

    def test_override_show(self):
        OverrideShow().main()

    def test_override_main(self):
        OverrideMain().main()

    def test_override_main_and_report(self):
        OverrideMainAndReport().main()


class TestMoreSuper:

    def test_super_1(self):
        ClassSuper1()

    def test_super_2(self):
        ClassSuper2()

    def test_super_3(self):
        ClassSuper3()


class TestFuncRunner:

    def test_run_decorator_once(self):
        FuncRunner().run_decorator_once()

    def test_run_decorator_twice(self):
        FuncRunner().run_decorator_twice()

    def test_run_call_func(self):
        FuncRunner().run_call_func()


class TestRecursion:

    def test_basic_recursion(self):
        Recursion().run_basic_recursion()

    def test_fib_recursive_3(self):
        Recursion().fib_recursive(3)


class TestClassWithManyCalls:

    def test_method_called_many_times(self):
        ClassWithManyCalls().call_method_many_times()

    def test_call_methods(self):
        ClassWithManyCalls().call_methods()


class TestClassWithExternalDependency:

    def test_call_external_dependencies(self):
        ClassWithExternalDependency().call_external_dependencies()
