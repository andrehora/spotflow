import trace
from happyflow.utils import line_intersection


class SUT:

    def __init__(self, name, filename):
        self.name = name
        self.filename = filename

    def __str__(self):
        return self.full_name()


class SUTSourceEntity(SUT):
    start_line = 0
    end_line = 0

    def global_flows(self, trace_result):
        return trace_result.global_sut_flows(self)

    def local_flows(self, trace_result):
        return trace_result.local_sut_flows(self)

    def executable_lines(self):
        executable_lines = trace._find_executable_linenos(self.filename)
        # remove the SUT definition, eg, def, class
        return self.intersection(executable_lines)[1:]

    def intersection(self, other_lines):
        my_lines = range(self.start_line, self.end_line + 1)
        return line_intersection(my_lines, other_lines)

    def loc(self):
        return self.end_line - self.start_line

    def full_name(self):
        pass

    def summary(self):
        return f'{self.full_name()} (lines: {self.start_line}-{self.end_line})'


class SUTModule(SUT):

    def __init__(self, name, filename=''):
        super().__init__(name, filename)
        self.suts = []

    def add_sut(self, func_or_method):
        self.suts.append(func_or_method)

    def full_name(self):
        return f'{self.name}'


class SUTClass(SUTSourceEntity):

    def __init__(self, module_name, name, filename=''):
        super().__init__(name, filename)
        self.module_name = module_name
        self.suts = []

    def add_sut(self, method):
        self.suts.append(method)

    def full_name(self):
        return f'{self.module_name}.{self.name}'


class SUTMethod(SUTSourceEntity):

    def __init__(self, module_name, class_name, name, filename=''):
        super().__init__(name, filename)
        self.module_name = module_name
        self.class_name = class_name

    def full_name(self):
        return f'{self.module_name}.{self.class_name}.{self.name}'


class SUTFunction(SUTSourceEntity):

    def __init__(self, module_name, name, filename=''):
        super().__init__(name, filename)
        self.module_name = module_name

    def full_name(self):
        return f'{self.module_name}.{self.name}'


class SUTContainer:

    def __init__(self):
        self.suts = []
        self.suts_map = {}

    def full_name(self):
        return 'SUTContainer'

    def __str__(self):
        return f'suts: {len(self.suts)}'

    def get(self, sut_name):
        return self.suts_map[sut_name]

    def add_module(self, module_name, filename):
        m = SUTModule(module_name)
        m.filename = filename
        self.suts.append(m)
        self.suts_map[str(m)] = m
        return m

    def add_class(self, module_name, class_name, start_line, end_line, filename):
        c = SUTClass(module_name, class_name)
        c.start_line = start_line
        c.end_line = end_line
        c.filename = filename
        self.suts_map[str(c)] = c
        return c

    def add_method(self, module_name, method_name, start_line, end_line, clazz, module, filename):
        m = SUTMethod(module_name, clazz.name, method_name)
        m.start_line = start_line
        m.end_line = end_line
        m.filename = filename

        clazz.add_sut(m)
        module.add_sut(m)

        self.suts.append(m)
        self.suts_map[str(m)] = m
        return m

    def add_function(self, module_name, function_name, start_line, end_line, module, filename):
        f = SUTFunction(module_name, function_name)
        f.start_line = start_line
        f.end_line = end_line
        f.filename = filename

        module.add_sut(f)

        self.suts.append(f)
        self.suts_map[str(f)] = f
        return f

    def run(self, result):
        for sut in self.suts:
            sut.run(result)



