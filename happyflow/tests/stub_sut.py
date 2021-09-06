class BasicStatements:

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


class ComplexStatements:

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


class ChangeStates:

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

        a += 1
        b += 10

    def change_list_state(self):
        a = []
        a.append(1)
        a.append(2)
        a.append(3)

    def change_var_state_with_loop(self):
        a = 0
        for i in range(1, 5):
            a = i


def function_with_3_lines():
    a = 123
    a = 123
    a = 123
