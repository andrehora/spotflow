from happyflow.utils import *


class FlowResult:

    def __init__(self, target_entity):
        self.target_entity = target_entity
        self.target_entity_name = target_entity.name
        self.source_entity_names = []
        self.flows = []

    def flow_result_by_lines(self, lines):
        target_flows = []
        for flow in self.flows:
            if tuple(flow.distinct_lines()) == tuple(lines):
                target_flows.append(flow)
        flow_result = FlowResult(self.target_entity)
        flow_result.flows = target_flows
        return flow_result

    def add(self, source_entity_name, flow, state_result=None):
        self.source_entity_names.append(source_entity_name)
        flow = Flow(source_entity_name, flow, state_result)
        self.flows.append(flow)

    def number_of_sources(self):
        return len(self.source_entity_names)

    def distinct_lines(self):
        lines = []
        for flow in self.flows:
            lines.append(tuple(flow.distinct_lines()))
        return lines

    def args(self):
        args_and_values = {}
        for flow in self.flows:
            if flow.state_result and flow.state_result.args:
                for arg in flow.state_result.args:
                    if arg.name != 'self':
                        value = clear_element(arg.value)
                        if arg.name in args_and_values:
                            args_and_values[arg.name].append(value)
                        else:
                            args_and_values[arg.name] = [value]
        return args_and_values

    def return_values(self):
        values = []
        for flow in self.flows:
            if flow.state_result and flow.state_result.has_return():
                value = flow.state_result.return_value.value
                value = clear_element(value)
                values.append(value)
        return values


class Flow:

    def __init__(self, source_entity_name, run_lines, state_result=None):
        self.source_entity_name = source_entity_name
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

    def has_return(self):
        return self.return_value and self.return_value.has_return

    def add(self, name, value, line, inline):
        self.vars[name] = self.vars.get(name, VarStateHistory(name, []))
        self.vars[name].add(name, value, line, inline)

    def is_line_return_value(self, line_number):
        if self.has_return():
            return line_number == self.return_value.line
        return False

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

    def __init__(self, value, line=0, has_return=False):
        self.value = value
        self.line = line
        self.has_return = has_return

    def __str__(self):
        return f'{self.value}'

    def __eq__(self, other):
        return self.value == other
