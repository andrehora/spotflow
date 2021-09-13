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