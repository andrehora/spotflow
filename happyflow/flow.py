from happyflow.utils import obj_value
from happyflow.info import *


class FlowResult:

    def __init__(self):
        self.method_traces = {}

    def compute_flows(self):
        for method_trace in self.method_traces.values():
            method_trace.compute_flows()

    def filter(self, filter_func):
        self.method_traces = {k: v for k, v in self.method_traces.items() if filter_func(k, v)}
        return self

    def has_calls(self, entity_name, method_trace):
        return method_trace.calls

    def __getitem__(self, key):
        return self.method_traces[key]

    def __setitem__(self, key, value):
        self.method_traces[key] = value

    def __contains__(self, key):
        return key in self.method_traces

    def __len__(self):
        return len(self.method_traces)

    def __repr__(self):
        return repr(self.method_traces)

    def __iter__(self):
        return iter(self.method_traces.values())


class CallContainer:

    def __init__(self, calls):
        self.calls = calls

    def group_by_distinct_run_lines(self, distinct_lines):
        calls = []
        for call in self.calls:
            if tuple(call.distinct_run_lines()) == tuple(distinct_lines):
                calls.append(call)
        call_container = CallContainer(self.target_method)
        call_container.calls = calls
        return call_container

    def distinct_run_lines(self):
        lines = []
        for call in self.calls:
            lines.append(tuple(call.distinct_run_lines()))
        return lines

    def arg_states(self):
        args_and_values = {}
        for call in self.calls:
            if call.call_state and call.call_state.arg_states:
                for arg in call.call_state.arg_states:
                    if arg.name != 'self':
                        value = arg.value
                        args_and_values[arg.name] = args_and_values.get(arg.name, [])
                        args_and_values[arg.name].append(value)
        return args_and_values

    def return_states(self):
        values = []
        for call in self.calls:
            if call.call_state and call.call_state.has_return():
                value = call.call_state.return_state.value
                values.append(value)
        return values

    def call_stack(self):
        cs = []
        for call in self.calls:
            cs.append(call.call_stack)
        return cs

    def call_stack_tests(self):
        return set(map(lambda each: each[0], self.call_stack()))


class MethodTrace(CallContainer):

    def __init__(self, target_method):
        super().__init__(calls=[])
        self.target_method = target_method
        self.target_method_name = target_method.name
        self.flows = []
        self._calls = {}
        self.info = None

    def add_call(self, run_lines, call_state, call_stack, call_id):
        call = MethodCall(run_lines, call_state, call_stack)
        self.calls.append(call)
        self._calls[call_id] = call
        return call

    def add_flow(self, flow_pos, distinct_run_lines, calls):
        flow = MethodFlow(flow_pos, distinct_run_lines, calls)
        self.flows.append(flow)
        return flow

    def _get_call_from_id(self, call_id):
        return self._calls.get(call_id, None)

    def compute_flows(self):
        most_common_run_lines = Analysis(self).most_common_run_lines()
        flow_pos = 0
        for run_lines in most_common_run_lines:
            flow_pos += 1
            distinct_run_lines = run_lines[0]

            call_container = self.group_by_distinct_run_lines(distinct_run_lines)
            flow = self.add_flow(flow_pos, distinct_run_lines, call_container.calls)
            flow.update_flow_info(self)

        self.info = TraceInfo(self)


class MethodFlow(CallContainer):

    def __init__(self, pos, distinct_run_lines, calls):
        super().__init__(calls)
        self.pos = pos
        self.distinct_run_lines = distinct_run_lines
        self.info = None

    def update_flow_info(self, method_trace):

        lineno = 0
        lineno_entity = method_trace.target_method.start_line - 1
        self.info = FlowInfo(self, method_trace)

        self._found_first_run_line = False
        for code, html in zip(method_trace.target_method.get_code_lines(), method_trace.target_method.get_html_lines()):

            lineno += 1
            lineno_entity += 1

            line_status = self.get_line_status(method_trace.target_method, lineno_entity)
            line_state = self.get_line_state(method_trace.target_method, lineno_entity)
            line_info = LineInfo(lineno, lineno_entity, line_status, code.rstrip(), html, line_state)

            self.info.append(line_info)
            self.info.update_run_status(line_info)

    def get_line_status(self, target_method, current_line):

        if current_line in self.distinct_run_lines:
            self._found_first_run_line = True
            return RunStatus.RUN

        # _find_executable_linenos of trace returns method/function definitions as executable lines (?).
        # We should flag those definitions as not executable lines (NOT_EXEC). Otherwise, the definitions
        # would impact on the flows. The solution for now is flagging all first lines as not executable
        # until we find the first run line. This way, the definitions are flagged as not executable lines...
        if not self._found_first_run_line:
            return RunStatus.NOT_EXEC

        if current_line not in self.distinct_run_lines:
            if not target_method.line_is_executable(current_line):
                return RunStatus.NOT_EXEC
            return RunStatus.NOT_RUN

    def get_line_state(self, target_method, lineno_entity, n=0):

        call = self.calls[n]

        states = call.call_state.states_for_line(lineno_entity)

        if target_method.line_is_entity_definition(lineno_entity):
            return self.arg_state(call)
        elif call.call_state.line_has_return_value(lineno_entity):
            return self.return_state(call)
        elif states:
            return self.var_states(states)
        return ''

    def arg_state(self, call):
        arg_str = ''
        for arg in call.call_state.arg_states:
            if arg.name != 'self':
                arg_str += str(arg)
        return StateStatus.ARG, arg_str

    def return_state(self, call):
        return_state = call.call_state.return_state
        return StateStatus.RETURN, str(return_state)

    def var_states(self, states):
        return StateStatus.VAR, states


class MethodCall:

    def __init__(self, run_lines, call_state, call_stack):
        self.run_lines = run_lines
        self.call_stack = call_stack
        self.call_state = call_state

    def __eq__(self, other):
        return other == self.run_lines

    def distinct_run_lines(self):
        return sorted(list(set(self.run_lines)))


class CallState:

    def __init__(self):
        self.arg_states = []
        self.var_states = {}
        self.yield_states = []
        self.return_state = None
        self.exception_state = None

    def save_arg_states(self, argvalues, lineno):
        for arg in argvalues.args:
            value = obj_value(argvalues.locals[arg])
            arg_state = ArgState(arg, value, lineno)
            self.arg_states.append(arg_state)

        if argvalues.varargs:
            value = obj_value(argvalues.locals[argvalues.varargs])
            arg_state = ArgState(argvalues.varargs, value, lineno)
            self.arg_states.append(arg_state)

        if argvalues.keywords:
            value = obj_value(argvalues.locals[argvalues.keywords])
            arg_state = ArgState(argvalues.keywords, value, lineno)
            self.arg_states.append(arg_state)

    def save_var_states(self, argvalues, lineno, inline):
        for arg in argvalues.locals:
            value = obj_value(argvalues.locals[arg])
            self._save_var_state(name=arg, value=value, lineno=lineno, inline=inline)

    def _save_var_state(self, name, value, lineno, inline):
        self.var_states[name] = self.var_states.get(name, VarStateHistory(name, []))
        self.var_states[name].add_var_state(name, value, lineno, inline)

    def save_yield_state(self, value, lineno):
        self.yield_states.append(YieldState(value, lineno))

    def save_return_state(self, value, lineno):
        self.return_state = ReturnState(value, lineno)

    def save_exception_state(self, value, lineno):
        self.exception_state = ExceptionState(value, lineno)

    def get_yield_states(self):
        if len(self.yield_states) <= 1:
            return self.yield_states
        # Remove the last element. This one is saved as an implicit return
        return self.yield_states[:-1]

    def states_for_line(self, lineno):
        states = []
        for var in self.var_states:
            var_states = ''
            if var != 'self':
                call_state = self.var_states[var]
                for state in call_state.states:
                    if state.inline == lineno:
                        if str(state) not in var_states and state.value_has_changed:
                            var_states += str(state) + ' '
            if var_states:
                states.append(var_states.strip())
        return states

    def line_has_return_value(self, lineno):
        if self.has_return():
            return lineno == self.return_state.lineno
        return False

    def has_return(self):
        return self.return_state is not None


class VarStateHistory:

    def __init__(self, name, states):
        self.name = name
        self.states = states

    def add_var_state(self, name, value, lineno, inline):
        value_has_changed = self.detect_value_has_changed(value)
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
            return False

    def get_last_state(self):
        return self.states[-1]

    def first_last(self):
        if len(self.states) == 1:
            return self.states[0], self.states[0]
        return self.states[0], self.states[-1]

    def distinct_values(self):
        values = {}
        for state in self.states:
            if state.value not in values:
                values[state.value] = None
        return values.keys()

    def distinct_sequential_values(self):
        values = []
        b = None
        for state in self.states:
            if state.value != b:
                values.append(state.value)
            b = state.value
        return values

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
