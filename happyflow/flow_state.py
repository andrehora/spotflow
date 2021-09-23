class FlowResult:

    def __init__(self, sut):
        self.sut = sut
        self.sut_name = sut.name
        self.test_names = []
        self.flows = []

    def add(self, test_name, flow, state_result=None):
        self.test_names.append(test_name)
        flow = Flow(test_name, flow, state_result)
        self.flows.append(flow)

    def number_of_tests(self):
        return len(self.test_names)


class Flow:

    def __init__(self, test_name, run_lines, state_result=None):
        self.test_name = test_name
        self.run_lines = run_lines
        self.state_result = state_result

    def __eq__(self, other):
        return other == self.run_lines

    def distinct_lines(self):
        return sorted(list(set(self.run_lines)))


class StateResult:

    def __init__(self, name):
        self.sut_name = name
        self.vars = {}

        self.args = None
        self.return_value = None

    def add(self, name, value, line, inline):
        self.vars[name] = self.vars.get(name, VarStateHistory(name, []))
        self.vars[name].add(name, value, line, inline)

    def is_line_return_value(self, line_number):
        return line_number == self.return_value.line

    def states_for_line(self, line_number):
        states = []
        for var in self.vars:
            var_states = ''
            if var != 'self':
                state_history = self.vars[var]
                for state in state_history.states:
                    if state.inline == line_number:
                        if str(state) not in var_states and state.value_has_changed:
                            var_states += str(state) + ' '
            if var_states:
                states.append(var_states)
        return states

    def state_diff_between_two_lines(self, line_number1, line_number2):
        list1 = self.states_for_line(line_number1)
        list2 = self.states_for_line(line_number2)
        return self.diff(list1, list2)

    def diff(self, list1, list2):
        second = set(list2)
        return [item for item in list1 if item not in second]


class VarStateHistory:

    def __init__(self, name, states):
        self.name = name
        self.states = states

    def add(self, name, value, line, inline):
        value_has_changed = False
        if len(self.states) == 0:
            value_has_changed = True
            # inline = line
        else:
            last_state = self.get_last()
            # inline = last_state.line
            if last_state.value != value:
                value_has_changed = True

        new_state = VarState(name, value, line, inline, value_has_changed)
        self.states.append(new_state)

    def get_last(self):
        return self.states[-1]

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


class VarState:

    def __init__(self, name, value, line, inline, value_has_changed=False):
        self.name = name
        self.value = value
        self.line = line
        self.inline = inline
        self.value_has_changed = value_has_changed

    def __str__(self):
        return f'{self.name}={self.value}'


class ArgState:

    def __init__(self, name, value, line):
        self.name = name
        self.value = value
        self.line = line

    def __str__(self):
        return f'{self.name}={self.value}'


class ReturnState:

    def __init__(self, value, line=0):
        self.value = value
        self.line = line

    def __str__(self):
        return f'{self.value}'

    def __eq__(self, other):
        return self.value == other
