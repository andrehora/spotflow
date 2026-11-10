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
            return 1
        return self.basic_recursion(n-1) + 1

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


class ClassSuper:

    def __init__(self):
        self.a = 1


class ClassSuperWithDependency(ClassSuper):

    def __init__(self):
        Dependency().foo()
        super().__init__()
        Dependency().bar()


class Dependency:

    def foo(self):
        x = 1

    def bar(self):
        y = 1


class ClassSuperOldStyle1:

    def __init__(self):
        self.foobar()
        self.a = 1
        self.b = 2

    def foobar(self):
        self.a = 3
        self.b = 4


class ClassSuperOldStyle2(ClassSuperOldStyle1):

    def __init__(self):
        ClassSuperOldStyle1.__init__(self)


class ClassSuperOldStyle3(ClassSuperOldStyle2):

    def foobar(self):
        ClassSuperOldStyle2.foobar(self)


class ClassSuperWithDependencyOldStyle(ClassSuper):

    def __init__(self):
        Dependency().foo()
        ClassSuper.__init__(self)
        Dependency().bar()


class HasSideEffectProperty:

    reads = 0

    def __init__(self, items):
        self.items = self.to_list(items)

    @staticmethod
    def to_list(items):
        return list(items)

    @property
    def length(self):
        HasSideEffectProperty.reads += 1
        return len(self.items)


def has_local_static_method_and_func_attr():

    def local_callback(x):
        return x

    class LocalClass4:

        def __init__(self):
            self.local_callback = local_callback

        @staticmethod
        def local_static(x):
            return x

        def run(self):
            return self.local_static(1) + self.local_callback(2)

    return LocalClass4().run()


import functools


class HasDescriptors:

    def __init__(self):
        self._value = 1

    @classmethod
    def class_method(cls, x):
        return x + 1

    @staticmethod
    def static_method(x):
        return x + 2

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    @functools.cached_property
    def cached_value(self):
        return self._value + 10


class SubHasDescriptors(HasDescriptors):
    pass


def call_descriptors():
    obj = HasDescriptors()
    HasDescriptors.class_method(1)
    obj.class_method(2)
    HasDescriptors.static_method(1)
    obj.static_method(2)
    obj.value = 5
    obj.value
    obj.cached_value


def call_inherited_descriptors():
    obj = SubHasDescriptors()
    SubHasDescriptors.class_method(1)
    SubHasDescriptors.static_method(1)
    obj.value = 5
    obj.value
    obj.cached_value


def target_one(x):
    return x + 1


def target_two(x):
    return x + 2


class HasTargets:

    def target_method(self, x):
        return x + 3


def call_targets():
    target_one(1)
    target_two(1)
    target_two(2)
    HasTargets().target_method(1)


def prefix(x):
    return x


def prefix_longer(x):
    return x


class Prefix:

    def run(self):
        return 1


class PrefixLonger:

    def run(self):
        return 2


def call_prefixes():
    prefix(1)
    prefix_longer(1)
    Prefix().run()
    PrefixLonger().run()


import asyncio
import contextlib


class ExitKinds:

    def return_raises(self, x):
        return int(x)

    def name_starts_with_return(self):
        returned = 5
        returned += 1

    def name_starts_with_yield(self):
        yielded = 5
        yielded += 1

    def inline_return(self, a):
        if a: return 1
        return 2

    def inline_return_or_implicit(self, a):
        if a: return 1

    def inline_def(self): return 7

    def return_in_with(self):
        with contextlib.nullcontext():
            return 5

    def return_in_finally(self):
        try:
            return 6
        finally:
            x = 1

    def multi_line_return(self, a):
        return dict(
            a=a,
        )

    def return_none_in_expression(self, a):
        return a if a else None

    def call_lambdas(self):
        value = lambda: 3
        none = lambda: None
        return value(), none()

    def assigned_yield(self):
        x = yield 1
        y = yield 2

    def yield_in_expression(self):
        x = [(yield 1)]

    def inline_yield(self, a):
        if a: yield 1

    def yield_then_return(self):
        yield 1
        return 9

    def yield_then_statement(self):
        yield 1
        x = 2

    def yield_from(self):
        yield from [1, 2]
        x = yield from self.yield_then_return()

    def closed(self):
        yield 1
        yield 2

    def thrown(self):
        yield 1
        yield 2

    def yield_then_raise(self):
        yield 1
        raise KeyError('k')

    async def coroutine_inner(self):
        await asyncio.sleep(0)
        return 4

    async def coroutine(self):
        value = await self.coroutine_inner()
        return value

    async def async_generator(self):
        yield 1
        await asyncio.sleep(0)
        yield 2

    async def use_async_generator(self):
        return [value async for value in self.async_generator()]

    def genexpr_in_return(self, items):
        return ' '.join(str(item) for item in items)

    def genexpr_in_assign(self, items):
        total = sum(item for item in items)
        return total

    def genexpr_in_yield(self, items):
        yield sum(item for item in items)

    def run_closed(self):
        gen = self.closed()
        next(gen)
        gen.close()

    def run_thrown(self):
        gen = self.thrown()
        next(gen)
        try:
            gen.throw(ValueError('v'))
        except ValueError:
            pass


class ControlFlow:

    def names_start_with_keywords(self):
        formatted = 1
        iffy = 2
        while_loop = 3
        elif_count = 4
        return formatted + iffy + while_loop + elif_count

    def statements(self, a):
        if a == 1:
            a += 1
        elif a == 2:
            a += 2
        else:
            a += 3
        while a < 10:
            a += 5
        for i in range(2):
            a += i
        return a

    def inline_if(self, a):
        if a: a += 1
        return a

    def multi_line_if(self, a, b):
        if (a and
                b):
            a += 1
        return a

    def expressions(self, a):
        x = 1 if a else 2
        y = [i for i in range(2) if i]
        z = a and x
        return x, y, z

    def nested(self, items):
        for item in items:
            if item:
                while item:
                    item -= 1
        return items

    async def async_for(self, values):
        async for value in values:
            pass

    def not_run(self, a):
        if a:
            for i in range(2):
                pass
        return a


async def async_values():
    yield 1
