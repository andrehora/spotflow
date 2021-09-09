import trace
from happyflow.utils import line_intersection


class SUT:
    start_line = 0
    end_line = 0
    filename = ''

    def composite_flows(self, trace_result):
        return trace_result.composite_sut_flows(self)

    def atomic_flows(self, trace_result):
        return trace_result.atomic_sut_flows(self)

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

    def __str__(self):
        return self.full_name()


class SUTClass(SUT):

    def __init__(self, module_name, name, filename=''):
        self.module_name = module_name
        self.name = name
        self.filename = filename
        self.methods = []

    def add_method(self, method):
        self.methods.append(method)

    # def composite_flows(self, trace_result):
    #     flows = []
    #     for method in self.methods:
    #         flow = method.composite_flows(trace_result)
    #         flows.append(flow)
    #     return flows
    #
    # def atomic_flows(self, trace_result):
    #     flows = []
    #     for method in self.methods:
    #         flow = method.atomic_flows(trace_result)
    #         flows.append(flow)
    #     return flows

    def full_name(self):
        return f'{self.module_name}.{self.name}'


class SUTMethod(SUT):

    def __init__(self, module_name, name, clazz, filename=''):
        self.module_name = module_name
        self.name = name
        self.clazz = clazz
        self.filename = filename

    def full_name(self):
        return f'{self.module_name}.{self.clazz.name}.{self.name}'


class SUTFunction(SUT):

    def __init__(self, module_name, name, filename=''):
        self.module_name = module_name
        self.name = name
        self.filename = filename

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

    def add_class(self, module_name, class_name, start_line, end_line, filename):
        c = SUTClass(module_name, class_name)
        c.start_line = start_line
        c.end_line = end_line
        c.filename = filename
        self.suts.append(c)
        self.suts_map[str(c)] = c
        return c

    def add_method(self, module_name, method_name, start_line, end_line, clazz, filename):
        m = SUTMethod(module_name, method_name, clazz)
        m.start_line = start_line
        m.end_line = end_line
        m.filename = filename
        clazz.add_method(m)
        self.suts_map[str(m)] = m
        return m

    def add_function(self, module_name, function_name, start_line, end_line, filename):
        f = SUTFunction(module_name, function_name)
        f.start_line = start_line
        f.end_line = end_line
        f.filename = filename
        self.suts.append(f)
        self.suts_map[str(f)] = f
        return f

    def run(self, result):
        for sut in self.suts:
            sut.run(result)


class SUTFlowResult:

    def __init__(self, sut):
        self.sut = sut
        self.sut_name = sut.name
        self.test_names = []
        self.flows = []

    def add(self, test_name, flow, state_result=None):
        self.test_names.append(test_name)
        flow = SUTFlow(test_name, flow, state_result)
        self.flows.append(flow)

    def number_of_tests(self):
        return len(self.test_names)


class SUTFlow:

    def __init__(self, test_name, run_lines, state_result=None):
        self.test_name = test_name
        self.run_lines = run_lines
        self.state_result = state_result

    def __eq__(self, other):
        return other == self.run_lines

    def distinct_lines(self):
        return sorted(list(set(self.run_lines)))


class SUTStateResult:

    def __init__(self, name):
        self.sut_name = name
        self.vars = {}

    def add(self, name, value, line):
        self.vars[name] = self.vars.get(name, SUTVarStateHistory(name, []))
        self.vars[name].add(name, value, line)


class SUTVarStateHistory:

    def __init__(self, name, states):
        self.name = name
        self.states = states

    def add(self, name, value, line):
        state = SUTVarState(name, value, line)
        self.states.append(state)

    def first_last(self):
        if len(self.states) == 1:
            return self.states[0], self.states[0]
        return self.states[0], self.states[-1]

    def distinct_values_str(self):
        str_values = {}
        for state in self.states:
            if str(state.value) not in str_values:
                str_values[str(state.value)] = None
        return str_values.keys()

    def distinct_sequential_values(self):
        distinct = []
        b = None
        for state in self.states:
            if state.value != b:
                distinct.append(state.value)
            b = state.value
        return distinct

    def distinct_values(self):
        str_values = {}
        for state in self.states:
            if state.value not in str_values:
                str_values[state.value] = None
        return str_values.keys()

    def __str__(self):
        return f'name: {self.name}, values: {len(self.states)}'


class SUTVarState:

    def __init__(self, name, value, line):
        self.name = name
        self.value = value
        self.line = line


