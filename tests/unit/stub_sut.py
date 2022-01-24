class SimpleCall:

    def simple_if(self, enter=True):
        if enter:
            a = 123

    def simple_if_else(self, enter=True):
        if enter:
            a = 123
        else:
            a = 456

    def loop(self):
        l = range(1, 3)
        for each in l:
            a = 123

    def try_success(self):
        try:
            a = 123
        except:
            a = 456

    def try_fail(self):
        try:
            1/0
        except:
            a = 123


class ComplexCall:

    def hello(self, hour):
        #intentional nested ifs
        if hour >= 12:
            if hour >= 18:
                return 'boa noite'
            return 'boa tarde'
        return 'bom dia'

    def func(self):
        self.f1()
        self.f2()
        self.f3()

    def f1(self):
        a = 1

    def f2(self):
        a = 2

    def f3(self):
        a = 3


class ChangeState:

    def change_var_state(self):
        a = 1
        a = 2
        a = 3

    def change_arg_state(self, a=0):
        a = 1
        a = 2
        a = 3

    def change_var_state_with_conditional(self, enter_if=True):
        a = 1
        if enter_if:
            a = 100
        else:
            a = 200

    def change_multiple_vars_states(self):
        a = 1
        b = 10

        a += 1    # a=2
        b += 100  # b=110

    def change_list_state(self):
        a = []
        a.append(1)
        a.append(2)
        a.append(3)
        a.remove(3)
        a.remove(2)
        a.remove(1)

    def change_var_state_with_loop(self):
        a = 0
        for i in range(1, 5):
            a = i

    def __init__(self):
        self.inst_var = 'default'

    def change_instance_var(self):
        self.inst_var = 'foo'
        self.inst_var = 'new foo'

    def keep_var_state(self):
        a = 1
        a = 1
        a = 1


def function_with_3_lines():
    a = 123
    a = 123
    a = 123


class Calculator:

    def __init__(self, n=0):
        self.total = n

    def add(self, n):
        self.total += n

    def subtract(self, n):
        self.total -= n

    def __str__(self):
        return f'Calc:{self.total}'

    def __eq__(self, other):
        if not other:
            return False
        return self.total == other.total


class ReturnValue:

    def __init__(self):
        self.n = 0
        self.str = ''
        self.list = []

    def simple_return(self):
        return 100

    def simple_return_with_arg(self, msg, name):
        return msg + ' ' + name

    def change_return_0(self, a, b):
        return a + b

    def change_return_1(self):
        a = 1
        b = 2
        return a + b

    def change_return_2(self):
        a = 1
        b = 2
        return a + b + 1

    def change_return_3(self):
        a = 'a'
        l = 'l'
        return f'{a} and {l}'

    def change_return_4(self):
        a = []
        a.append(1)
        a.append(2)
        a.append(3)
        return a

    def change_return_5(self):
        result = 0
        for each in range(1, 5):
            result += each
        return result

    def multiple_return(self, enter=True):
        if enter:
            return 'enter is true'
        return 'enter is false'

    def change_attribute_0(self, new_n):
        self.n = new_n
        return self.n

    def change_attribute_1(self):
        self.n = 100
        return self.n + 1

    def change_attribute_2(self):
        self.str = 'FOO'
        return self.str.lower()

    def change_attribute_3(self):
        self.list = [1, 2, 3, 4, 5]
        return len(self.list)

    def change_obj_1(self):
        calc = Calculator()
        calc.add(5)
        calc.add(5)
        calc.subtract(1)
        return calc.total

    def change_obj_2(self, add1, add2, sub):
        calc = Calculator()
        calc.add(add1)
        calc.add(add2)
        calc.subtract(sub)
        return calc.total

    def change_obj_3(self):
        calc = Calculator()
        calc.add(5)
        calc.add(5)
        calc.subtract(1)
        return calc

    def explicit_return_state(self):
        return 123

    def explicit_return_none(self):
        return None

    def explicit_return(self):
        return

    def implicit_return(self):
        a = 123


class Exceptions:

    def zero_division(self):
        10 / 0

    def raise_generic_exception(self):
        raise Exception

    def raise_specific_exception(self):
        raise TypeError

    def raise_distinct_exception(self, first_line=False, second_line=False, third_line=False):
        self.raise_here(first_line)
        self.raise_here(second_line)
        self.raise_here(third_line)

    def raise_here(self, yes):
        if yes:
            raise Exception


class Generators:

    def no_generator(self):
        return

    def call_generator_1(self):
        g = self.has_generator_1()
        next(g)

    def call_generator_2(self):
        g = self.has_generator_2()
        next(g)
        next(g)

    def call_generator_3(self):
        g = self.has_generator_3()
        next(g)
        next(g)
        next(g)
        next(g)

    def has_generator_1(self):
        yield

    def has_generator_2(self):
        yield 100
        yield 200

    def has_generator_3(self):
        for each in range(1, 4):
            yield each
            if each == 3:
                yield 10

    def call_generator_4(self):
        g = self.has_generator_4()
        next(g)
        next(g)

    def has_generator_4(self):
        yield 100
        yield 200
        yield 300 # not called


class GeneratorExpression:

    def generator_expression_1(self):
        g = (x for x in range(1, 10))

    def generator_expression_2(self):
        g = (x for x in range(1, 10))
        next(g)
        next(g)
        next(g)


class Comprehension:

    def listcomp_1(self):
        g = [x for x in range(1, 10)]

    def listcomp_2(self):
        s = sum([x for x in range(1, 10)])

    def setcomp_1(self):
        g = {x for x in range(1, 10)}

    def setcomp_2(self):
        s = sum({x for x in range(1, 10)})

    def dictcomp(self):
        g = {x: x for x in range(1, 10)}


class LocalMethod:

    def has_local_method_1(self):
        x = 100
        y = 200

        def local_method():
            return

    def has_local_method_2(self):
        x = 100
        y = 200

        def local_method():
            return

        local_method()
        local_method()

    def has_local_method_3(self):
        x = 100
        y = 200

        def local_method_1():
            return

        def local_method_2():
            return

        local_method_1()
        local_method_2()

    def has_local_method_4(self):
        x = 100
        y = 200

        def local_method_1():

            def local_method_2():
                return

            local_method_2()
            return

        local_method_1()


def has_local_function_1():
    x = 100
    y = 200

    def local_function():
        return


def has_local_function_2():
    x = 100
    y = 200

    def local_function():
        return

    local_function()
    local_function()


def has_local_function_3():
    x = 100
    y = 200

    def local_function_1():
        return

    def local_function_2():
        return

    local_function_1()
    local_function_2()


def has_local_function_4():
    x = 100
    y = 200

    def local_function_1():

        def local_function_2():
            return

        local_function_2()
        return

    local_function_1()


class ClassA:

    def __init__(self, value):
        self.value = value
        self.a = 321

    def foobar(self, x):
        self.value = x


class ClassB(ClassA):

    def __init__(self, value):
        super().__init__(value)
        self.b = 321

    def foobar(self, x):
        super().foobar(x)
        y = x
        z = y


class ClassC(ClassB):

    def __init__(self, value):
        super().__init__(value)
        self.c = None

    def foobar(self, x):
        super().foobar(x)
        k = x


class ClassD(ClassB):

    def __init__(self, value):
        super(ClassD, self).__init__(value)
        self.c = None

    def foobar(self, x):
        super().foobar(x)
        k = x


class BaseClass:

    def main(self):
        self.show()

    def show(self):
        return

    def report(self):
        return


class OverrideShow(BaseClass):

    def show(self):
        return


class OverrideMain(BaseClass):

    def main(self):
        self.report()


class OverrideMainAndReport(BaseClass):

    def main(self):
        self.report()

    def report(self):
        self.show()


class ClassSuper1:

    def __init__(self):
        self.foobar()
        self.a = 1
        self.b = 2

    def foobar(self):
        self.a = 2
        self.b = 2


class ClassSuper2(ClassSuper1):

    def __init__(self):
        super().__init__()


class ClassSuper3(ClassSuper2):

    def foobar(self):
        super().foobar()


class HasLocalClass:

    class LocalClass1:

        def local(self):
            return 'me 1'

    def has_local_class(self):

        class LocalClass2:
            def local(self):
                return 'me 2'

        return LocalClass2().local()


def has_local_class():

    class LocalClass3:
        def local(self):
            return 'me 3'

    return LocalClass3().local()


class FuncRunner:

    def decorator(self, func):
        def inner():
            func()
        return inner

    def func_to_be_run(self):
        return

    def run_decorator_once(self):
        run_func = self.decorator(self.func_to_be_run)
        run_func()

    def run_decorator_twice(self):
        run_func = self.decorator(self.func_to_be_run)
        run_func()
        run_func()

    def call_func_three_times(self, func):
        func()
        func()
        func()

    def run_call_func(self):
        self.call_func_three_times(self.func_to_be_run)


class Recursion:

    def basic_recursion(self, n):
        if n == 1:
            return
        self.basic_recursion(n-1)

    def run_basic_recursion(self):
        self.basic_recursion(3)

    def fib_recursive(self, n):
        def fib_recursive_term(i):
            if i < 0:
                raise Exception("n is negative")
            if i < 2:
                return i
            return fib_recursive_term(i - 1) + fib_recursive_term(i - 2)

        if n < 0:
            raise Exception("n is negative")
        return [fib_recursive_term(i) for i in range(n + 1)]


class ClassWithManyCalls:

    def call_method_many_times(self):
        for index in range(1, 101):
            self.method_called_many_times(index)

    def method_called_many_times(self, index):
        return index

    def call_methods(self):
        self.with_arg_123(123)
        self.return_123()
        try:
            self.with_exception()
        except ZeroDivisionError:
            pass

    def with_arg_123(self, arg1):
        pass

    def return_123(self):
        return 123

    def with_exception(self):
        1/0


class ClassWithExternalDependency:

    def call_external_dependencies(self):
        self.str_split('abc def')
        self.time_time()
        self.os_isdir()
        self.os_realpath()
        self.inspect_ismethod()

    def str_split(self, txt):
        # Built-in functions are not monitored
        return txt.split()

    def time_time(self):
        # Built-in functions are not monitored
        import time
        return time.time()

    def os_isdir(self):
        import os
        return os.path.isdir("dir")

    def os_realpath(self):
        import os
        return os.path.realpath(__file__)

    def inspect_ismethod(self):
        import inspect
        return inspect.ismethod(None)
