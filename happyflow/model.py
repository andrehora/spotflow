from happyflow.utils import obj_value, obj_type
from happyflow.info import *


class MonitoredSystem:

    def __init__(self):
        self.monitored_methods = {}

    def all_methods(self):
        return list(self.monitored_methods.values())

    def all_calls(self):
        calls = []
        for mth in self.all_methods():
            calls.extend(mth.calls)
        return calls

    def _update_flows_and_info(self):
        for method in self.monitored_methods.values():
            method._compute_flows()
            method._update_call_info()

    def __getitem__(self, key):
        return self.monitored_methods[key]

    def __setitem__(self, key, value):
        self.monitored_methods[key] = value

    def __contains__(self, key):
        return key in self.monitored_methods

    def __len__(self):
        return len(self.monitored_methods)

    def __repr__(self):
        return repr(self.monitored_methods)

    def __iter__(self):
        return iter(self.monitored_methods.values())


class CallContainer:

    def __init__(self, calls):
        self.calls = calls

    def add_call(self, call):
        self.calls.append(call)

    def all_distinct_run_lines(self):
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

    def yield_states(self):
        values = []
        for call in self.calls:
            if call.call_state:
                for yield_state in call.call_state.yield_states:
                    values.append(yield_state.value)
        return values

    def return_states(self):
        values = []
        for call in self.calls:
            if call.call_state and call.call_state.has_return():
                value = call.call_state.return_state.value
                values.append(value)
        return values

    def exception_states(self):
        values = []
        for call in self.calls:
            if call.call_state and call.call_state.has_exception():
                value = call.call_state.exception_state.value
                values.append(value)
        return values

    def call_stack(self):
        cs = []
        for call in self.calls:
            cs.append(call.call_stack)
        return cs

    def callers(self):
        return sorted(set(map(lambda each: each[-2], self.call_stack())))

    def tests(self):
        return sorted(set(map(lambda each: each[0], self.call_stack())))

    def _select_calls_by_lines(self, distinct_lines):
        calls = []
        for call in self.calls:
            if tuple(call.distinct_run_lines()) == tuple(distinct_lines):
                calls.append(call)
        return calls


class MonitoredMethod(CallContainer):

    def __init__(self, method_info):
        super().__init__(calls=[])
        self.info = method_info
        self.method_name = method_info.name
        self.flows = []
        self.run_lines = {}
        self._calls_by_id = {}

    def distinct_run_lines(self):
        return self.run_lines.keys()

    def first_run_line(self):
        return self.calls[0].run_lines[0]

    def _add_run_line(self, lineno):
        line_freq = self.run_lines.get(lineno, 0)
        self.run_lines[lineno] = line_freq + 1

    def _get_call_from_id(self, call_id):
        return self._calls_by_id.get(call_id, None)

    def _add_call(self, call_state, call_stack, call_id):
        call = MethodCall(call_state, call_stack, self)
        super().add_call(call)
        self._calls_by_id[call_id] = call
        return call

    def _add_flow(self, flow_pos, distinct_run_lines, flow_calls):
        flow = MethodFlow(flow_pos, distinct_run_lines, flow_calls, self)
        self.flows.append(flow)
        return flow

    def _compute_flows(self):
        most_common_run_lines = Analysis(self).most_common_run_lines()
        flow_pos = 0
        for run_lines in most_common_run_lines:
            flow_pos += 1
            distinct_run_lines = run_lines[0]

            flow_calls = self._select_calls_by_lines(distinct_run_lines)
            flow = self._add_flow(flow_pos, distinct_run_lines, flow_calls)
            flow._update_flow_info()

    def _update_call_info(self):
        self.info._update_call_info(self)


class MethodFlow(CallContainer):

    def __init__(self, pos, distinct_run_lines, calls, monitored_method):
        super().__init__(calls)
        self.pos = pos
        self.distinct_run_lines = distinct_run_lines
        self.monitored_method = monitored_method
        self.info = None
        self._found_first_run_line = False

    def _update_flow_info(self):
        lineno = 0
        self.info = FlowInfo(self)
        self._found_first_run_line = False

        for lineno_entity in range(self.monitored_method.info.start_line, self.monitored_method.info.end_line+1):
            lineno += 1

            line_status = self._get_line_status(lineno_entity)
            line_type, line_state = self._get_line_state(lineno_entity)
            line_info = LineInfo(lineno, lineno_entity, line_status, line_type, line_state, self.monitored_method.info)

            self.info._append(line_info)
            self.info._update_run_status(line_info)

    def _get_line_status(self, current_line):

        if current_line in self.distinct_run_lines:
            self._found_first_run_line = True
            return RunStatus.RUN

        # _find_executable_linenos of trace returns method/function definitions as executable lines (?).
        # We should flag those definitions as not executable lines (NOT_EXEC). Otherwise, the definitions would impact
        # on the flows, coverage, etc. The solution for now is flagging all first lines as not executable until we
        # find the first run line. This way, the definitions are flagged as not executable lines...
        if not self._found_first_run_line:
            return RunStatus.NOT_EXEC

        if current_line not in self.distinct_run_lines:
            if not self.monitored_method.info.line_is_executable(current_line):
                return RunStatus.NOT_EXEC

        return RunStatus.NOT_RUN

    def _get_line_state(self, current_line, n=0):
        call = self.calls[n]
        return call.get_line_state(current_line)


class MethodCall:

    def __init__(self, call_state, call_stack, monitored_method):
        self.call_state = call_state
        self.call_stack = call_stack
        self.monitored_method = monitored_method
        self.run_lines = []

    def distinct_run_lines(self):
        return sorted(list(set(self.run_lines)))

    def get_line_state(self, lineno):

        if self.monitored_method.info.start_line == lineno:
            return self.line_arg_state()

        if lineno in self.monitored_method.info.return_lines:
            return self.line_return_state()

        states = self.call_state.states_for_line(lineno)
        if states:
            return self.line_var_states(states)
        return '', ''

    def line_arg_state(self):
        arg_str = ''
        for arg in self.call_state.arg_states:
            if arg.name != 'self':
                arg_str += str(arg)
        return LineType.ARG, arg_str

    def line_return_state(self):
        return_state = self.call_state.return_state
        return LineType.RETURN, str(return_state)

    def line_var_states(self, states):
        return LineType.VAR, states

    def _add_run_line(self, lineno):
        self.run_lines.append(lineno)

    def __eq__(self, other):
        return other == self.run_lines


class CallState:

    def __init__(self):
        self.var_states = {}
        self.arg_states = []
        self.yield_states = []
        self.return_state = None
        self.exception_state = None

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

    def get_yield_states(self):
        if len(self.yield_states) <= 1:
            return self.yield_states
        # Remove the last element. This one is saved as an implicit return
        return self.yield_states[:-1]

    def has_argument(self):
        return len(self.arg_states) > 0

    def has_return(self):
        return self.return_state is not None

    def has_exception(self):
        return self.exception_state is not None

    def has_yield(self):
        return len(self.yield_states) > 0

    def _save_arg_states(self, argvalues, lineno):
        for arg in argvalues.args:
            obj = argvalues.locals[arg]
            arg_state = ArgState(arg, obj_value(obj), obj_type(obj), lineno)
            self.arg_states.append(arg_state)

        if argvalues.varargs:
            obj = argvalues.locals[argvalues.varargs]
            arg_state = ArgState(argvalues.varargs, obj_value(obj), obj_type(obj), lineno)
            self.arg_states.append(arg_state)

        if argvalues.keywords:
            obj = argvalues.locals[argvalues.keywords]
            arg_state = ArgState(argvalues.keywords, obj_value(obj), obj_type(obj), lineno)
            self.arg_states.append(arg_state)

    def _save_var_states(self, argvalues, lineno, inline):
        for arg in argvalues.locals:
            obj = argvalues.locals[arg]
            value = obj_value(obj)
            type = obj_type(obj)
            self._save_var_state(name=arg, value=value, type=type, lineno=lineno, inline=inline)

    def _save_var_state(self, name, value, type, lineno, inline):
        self.var_states[name] = self.var_states.get(name, VarStateHistory(name, []))
        self.var_states[name].add_var_state(name, value, type, lineno, inline)

    def _save_yield_state(self, value, type, lineno):
        self.yield_states.append(YieldState(value, type, lineno))

    def _save_return_state(self, value, type, lineno):
        self.return_state = ReturnState(value, type, lineno)

    def _save_exception_state(self, value, type, lineno):
        self.exception_state = ExceptionState(value, type, lineno)


class VarStateHistory:

    def __init__(self, name, states):
        self.name = name
        self.states = states

    def add_var_state(self, name, value, type, lineno, inline):
        value_has_changed = self.detect_value_has_changed(value)
        new_state = VarState(name, value, type, lineno, inline, value_has_changed)
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


class State:

    def __init__(self, value, type, lineno):
        self.value = value
        self.type = type
        self.lineno = lineno


class VarState(State):

    def __init__(self, name, value, type, lineno, inline, value_has_changed=False):
        super().__init__(value, type, lineno)
        self.name = name
        self.inline = inline
        self.value_has_changed = value_has_changed

    def __str__(self):
        return f'{self.name}={self.value}'


class ArgState(State):

    def __init__(self, name, value, type, lineno):
        super().__init__(value, type, lineno)
        self.name = name
        self.lineno = lineno

    def __str__(self):
        return f'{self.name}={self.value}'


class ReturnState(State):

    def __init__(self, value, type, lineno=0):
        super().__init__(value, type, lineno)

    def __str__(self):
        return f'{self.value}'

    def __eq__(self, other):
        return self.value == other


class YieldState(State):

    def __init__(self, value, type, lineno=0):
        super().__init__(value, type, lineno)

    def __str__(self):
        return f'{self.value}'

    def __eq__(self, other):
        return self.value == other


class ExceptionState(State):

    def __init__(self, value, type, lineno=0):
        super().__init__(value, type, lineno)

    def __str__(self):
        return f'{self.value}'

    def __eq__(self, other):
        return self.value == other
