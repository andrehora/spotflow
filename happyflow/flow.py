class FlowResult:

    def __init__(self):
        self.entity_flows = {}

    def __getitem__(self, key):
        return self.entity_flows[key]

    def __setitem__(self, key, value):
        self.entity_flows[key] = value

    def __contains__(self, key):
        return key in self.entity_flows

    def __len__(self):
        return len(self.entity_flows)

    def __repr__(self):
        return repr(self.entity_flows)

    def __iter__(self):
        return iter(self.entity_flows)

    def values(self):
        return self.entity_flows.values()

    def filter(self, filter_func):
        self.entity_flows = {k: v for k, v in self.entity_flows.items() if filter_func(k, v)}
        return self

    def has_flows(self, entity_name, entity_result):
        return entity_result.flows


class EntityFlowContainer:

    def __init__(self, target_entity):
        self.target_entity = target_entity
        self.target_entity_name = target_entity.name
        self._flows = {}
        self.flows = []

    def add_flow(self, run_lines, state_history, callers, flow_id):
        flow = Flow(run_lines, state_history, callers)
        self.flows.append(flow)
        self._flows[flow_id] = flow

    def flow_by_lines(self, lines):
        target_flows = []
        for flow in self.flows:
            if tuple(flow.distinct_lines()) == tuple(lines):
                target_flows.append(flow)
        flow_container = EntityFlowContainer(self.target_entity)
        flow_container.flows = target_flows
        return flow_container

    def get_flow_from_id(self, flow_id):
        return self._flows.get(flow_id, None)

    def distinct_lines(self):
        lines = []
        for flow in self.flows:
            lines.append(tuple(flow.distinct_lines()))
        return lines

    def arg_states(self):
        args_and_values = {}
        for flow in self.flows:
            if flow.state_history and flow.state_history.arg_states:
                for arg in flow.state_history.arg_states:
                    if arg.name != 'self':
                        value = arg.value
                        args_and_values[arg.name] = args_and_values.get(arg.name, [])
                        args_and_values[arg.name].append(value)
        return args_and_values

    def return_states(self):
        values = []
        for flow in self.flows:
            if flow.state_history and flow.state_history.has_return():
                value = flow.state_history.return_state.value
                values.append(value)
        return values

    def callers(self):
        cs = []
        for flow in self.flows:
            cs.append(flow.callers)
        return cs

    def callers_tests(self):
        return set(map(lambda each: each[0], self.callers()))


class Flow:

    def __init__(self, run_lines, state_history, callers):
        self.run_lines = run_lines
        self.state_history = state_history
        self.callers = callers

    def __eq__(self, other):
        return other == self.run_lines

    def distinct_lines(self):
        return sorted(list(set(self.run_lines)))


class StateHistory:

    def __init__(self):
        self.vars = {}
        self.arg_states = None
        self.yield_states = []
        self.return_state = None
        self.exception_state = None

    def get_yield_states(self):
        if len(self.yield_states) <= 1:
            return self.yield_states
        # Remove the last element. This one saved as an implicit return
        return self.yield_states[:-1]

    def add_var_state(self, name, value, lineno, inline):
        self.vars[name] = self.vars.get(name, VarStateHistory(name, []))
        self.vars[name].add(name, value, lineno, inline)

    def add_yield_state(self, value, lineno):
        self.yield_states.append(YieldState(value, lineno))

    def add_return_state(self, value, lineno):
        self.return_state = ReturnState(value, lineno)

    def is_return_value(self, lineno):
        if self.has_return():
            return lineno == self.return_state.lineno
        return False

    def has_return(self):
        return self.return_state  # and self.return_state.has_explicit_return

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

    def add(self, name, value, lineno, inline):
        value_has_changed = self.detect_value_has_changed(value)
        # if value_has_changed:
        new_state = VarState(name, value, lineno, inline, value_has_changed)
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

    def __init__(self, name, value, lineno, inline, value_has_changed=False):
        self.name = name
        self.value = value
        self.lineno = lineno
        self.inline = inline
        self.value_has_changed = value_has_changed

    def __str__(self):
        return f'{self.name}={self.value}'


class ArgState:

    def __init__(self, name, value, lineno):
        self.name = name
        self.value = value
        self.lineno = lineno

    def __str__(self):
        return f'{self.name}={self.value}'


class ReturnState:

    def __init__(self, value, lineno=0):
        self.value = value
        self.lineno = lineno

    def __str__(self):
        return f'{self.value}'

    def __eq__(self, other):
        return self.value == other


class YieldState:

    def __init__(self, value, lineno=0):
        self.value = value
        self.lineno = lineno

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


