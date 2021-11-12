class TraceResult:

    def __init__(self):
        self.results = {}

    def __getitem__(self, key):
        return self.results[key]

    def __setitem__(self, key, value):
        self.results[key] = value

    def __contains__(self, key):
        return key in self.results

    def __len__(self):
        return len(self.results)

    def __repr__(self):
        return repr(self.results)

    def __iter__(self):
        return iter(self.results)

    def filter(self, filter_func):
        self.results = {k: v for k, v in self.results.items() if filter_func(k, v)}
        return self

    def has_flows(self, entity_name, entity_result):
        return entity_result.flows


class EntityTraceResult:

    def __init__(self, target_entity):
        self.target_entity = target_entity
        self.target_entity_name = target_entity.name
        self.flows = []

    def flow_result_by_lines(self, lines):
        target_flows = []
        for flow in self.flows:
            if tuple(flow.distinct_lines()) == tuple(lines):
                target_flows.append(flow)
        flow_result = EntityTraceResult(self.target_entity)
        flow_result.flows = target_flows
        return flow_result

    def add(self, flow_lines, state_result=None):
        flow = Flow(flow_lines, state_result)
        self.flows.append(flow)

    def get_last_flow(self):
        return self.flows[-1]

    def distinct_lines(self):
        lines = []
        for flow in self.flows:
            lines.append(tuple(flow.distinct_lines()))
        return lines

    def arg_states(self):
        args_and_values = {}
        for flow in self.flows:
            if flow.state_result and flow.state_result.arg_states:
                for arg in flow.state_result.arg_states:
                    if arg.name != 'self':
                        value = arg.value
                        args_and_values[arg.name] = args_and_values.get(arg.name, [])
                        args_and_values[arg.name].append(value)
        return args_and_values

    def return_states(self):
        values = []
        for flow in self.flows:
            if flow.state_result and flow.state_result.has_return():
                value = flow.state_result.return_state.value
                values.append(value)
        return values


class Flow:

    def __init__(self, run_lines, state_result=None):
        self.run_lines = run_lines
        self.state_result = state_result

    def __eq__(self, other):
        return other == self.run_lines

    def distinct_lines(self):
        return sorted(list(set(self.run_lines)))


class StateResult:

    def __init__(self, name):
        self.target_entity_name = name
        self.vars = {}

        self.arg_states = None
        self.return_state = None
        self.exception_state = None

    def has_return(self):
        return self.return_state and self.return_state.has_return

    def add(self, name, value, line, inline):
        self.vars[name] = self.vars.get(name, VarStateHistory(name, []))
        self.vars[name].add(name, value, line, inline)

    def is_return_value(self, line_number):
        if self.has_return():
            return line_number == self.return_state.line
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
                states.append(var_states.strip())
        return states


class VarStateHistory:

    def __init__(self, name, states):
        self.name = name
        self.states = states

    def add(self, name, value, line, inline):
        value_has_changed = self.detect_value_has_changed(value)
        # if value_has_changed:
        new_state = VarState(name, value, line, inline, value_has_changed)
        self.states.append(new_state)

    def detect_value_has_changed(self, new_value):
        if not self.states:
            return True
        last_state = self.get_last_state()
        try:
            if last_state.value != new_value:
                return True
            return False
        except Exception as e:
            # print(e)
            return False

    def get_last_state(self):
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


class ExceptionState:

    def __init__(self, value, line=0):
        self.value = value
        self.line = line

    def __str__(self):
        return f'{self.value}'

    def __eq__(self, other):
        return self.value == other


