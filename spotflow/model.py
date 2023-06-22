from spotflow.utils import obj_value, obj_type


class MonitoredProgram:
    def __init__(self):
        self.monitored_methods = {}

    def all_methods(self):
        return list(self.monitored_methods.values())

    def all_calls(self):
        calls = []
        for mth in self.all_methods():
            calls.extend(mth.calls)
        return calls

    def show_summary(self):
        print("============= Result =============")
        print("MonitoredProgram")
        print("- methods: " + str(len(self.all_methods())))
        print("- calls: " + str(len(self.all_calls())))
        for m in self.all_methods():
            m.show_summary()
            for call in m.calls:
                call.show_summary()

    def show_calls(self):
        sorted_methods = sorted(self.all_methods(), key=lambda mth: len(mth.calls), reverse=True)
        print("rank, method_name, number_of_calls")
        count = 0
        for method in sorted_methods:
            count += 1
            print(f"{count}, {method.full_name}, {len(method.calls)}")

    def show_pprint(self):
        from spotflow.report import pprint_report
        try:
            pprint_report(self)
            return True
        except Exception as e:
            return False

    def _update_info(self):
        for method in self.monitored_methods.values():
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

    def call_stack(self):
        cs = []
        for call in self.calls:
            cs.append(call.call_stack)
        return cs

    def callers(self):
        return sorted(set(map(lambda each: each[-2], self.call_stack())))

    def tests(self):
        tests = set()
        for call in self.calls:
            for call_name in call.call_stack:
                if ".test_" in call_name:
                    tests.add(call_name)
        return tests

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
                    if arg.name != "self":
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

    def _add_call(self, call):
        self.calls.append(call)


class MonitoredMethod(CallContainer):
    def __init__(self, method_info):
        super().__init__(calls=[])
        self.info = method_info
        self.name = method_info.name
        self.full_name = method_info.full_name
        self.run_lines = {}
        self.calls_by_id = {}

    def distinct_run_lines(self):
        return self.run_lines.keys()

    def show_summary(self):
        print("MonitoredMethod")
        print("- name: " + self.name)
        print("- calls: " + str(len(self.calls)))

    def _get_first_run_line(self):
        return self.calls[0].run_lines[0]

    def _add_run_line(self, lineno):
        line_freq = self.run_lines.get(lineno, 0)
        self.run_lines[lineno] = line_freq + 1

    def _get_call_from_id(self, call_id):
        return self.calls_by_id.get(call_id, None)

    def _add_call(self, call_state, call_stack, call_id):
        call = MethodCall(call_state, call_stack, self)
        super()._add_call(call)
        self.calls_by_id[call_id] = call
        return call

    def _update_call_info(self):
        self.info._update_call_info(self)

    def __str__(self):
        return f"MonitoredMethod: {self.full_name} (calls: {len(self.calls)})"


class MethodCall:
    def __init__(self, call_state, call_stack, monitored_method):
        self.call_state = call_state
        self.call_stack = call_stack
        self.monitored_method = monitored_method
        self.run_lines = []


    def path_info(self):
        from spotflow.info import PathInfo
        return PathInfo(self.monitored_method, self)

    def is_called_by_test(self):
        return self._find_test_name_in_stack()[0]
    
    def test_fullname(self):
        return self._find_test_name_in_stack()[1]
    
    def test_name(self):
        return self._find_test_name_in_stack()[2]
    
    def _find_test_name_in_stack(self):
        for full_name in self.call_stack:
            if '.' in full_name:
                last_name = full_name.split('.')[-1]
                if 'test_' in last_name:
                    return True, full_name, last_name
            else: 
                if 'test_' in full_name:
                    return True, full_name, full_name
        return False, '', ''

    def is_directly_called_from_test(self):
        if len(self.call_stack) <= 1:
            return False
        caller = self.call_stack[-2]
        return ".test_" in caller

    def is_started_in_test(self):
        test_name = self.call_stack[0]
        return ".test_" in test_name

    def distinct_run_lines(self):
        return sorted(list(set(self.run_lines)))

    def show_summary(self):
        print("MethodCall")
        print("- distinct_run_lines: " + str(self.distinct_run_lines()))
        print("- run_lines: " + str(self.run_lines))
        self.call_state.show_summary()

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

    def has_argument(self):
        return len(self.arg_states) > 0 and self.arg_states[0].name != "self"

    def has_var(self):
        return len(self.var_states) > 0

    def has_return(self):
        return self.return_state is not None

    def has_exception(self):
        return self.exception_state is not None

    def has_yield(self):
        return len(self.yield_states) > 0

    def return_type(self, t):
        return self.return_state and self.return_state.type == t

    def get_yield_states(self):
        if len(self.yield_states) <= 1:
            return self.yield_states
        # Remove the last element. This one is saved as an implicit return
        return self.yield_states[:-1]

    def show_summary(self):
        if self.has_argument():
            print("ArgState")
            for arg in self.arg_states:
                print("- " + str(arg))
        if self.has_var():
            print("VarStateHistory")
            for var in self.var_states:
                print("- " + str(self.var_states[var]))
        if self.has_return():
            print("ReturnState: " + str(self.return_state))
        if self.has_exception():
            print("ExceptionState: " + str(self.exception_state))

    def _states_for_line(self, lineno):
        states = []
        for var in self.var_states:
            var_states = ""
            if var != "self":
                call_state = self.var_states[var]
                for state in call_state.states:
                    if state.inline == lineno:
                        if str(state) not in var_states and state.value_has_changed:
                            var_states += str(state) + " "
            if var_states:
                states.append(var_states.strip())
        return states

    def _save_arg_states(self, argvalues, lineno):
        for arg in argvalues.args:
            obj = argvalues.locals[arg]
            arg_state = ArgState(arg, obj_value(obj), obj_type(obj), lineno)
            self.arg_states.append(arg_state)

        if argvalues.varargs:
            obj = argvalues.locals[argvalues.varargs]
            arg_state = ArgState(
                argvalues.varargs, obj_value(obj), obj_type(obj), lineno
            )
            self.arg_states.append(arg_state)

        if argvalues.keywords:
            obj = argvalues.locals[argvalues.keywords]
            arg_state = ArgState(
                argvalues.keywords, obj_value(obj), obj_type(obj), lineno
            )
            self.arg_states.append(arg_state)

    def _save_var_states(self, argvalues, lineno, inline):
        for arg in argvalues.locals:
            obj = argvalues.locals[arg]
            value = obj_value(obj)
            type = obj_type(obj)
            self._save_var_state(
                name=arg, value=value, type=type, lineno=lineno, inline=inline
            )

    def _save_var_state(self, name, value, type, lineno, inline):
        self.var_states[name] = self.var_states.get(name, VarStateHistory(name, []))
        self.var_states[name]._add_var_state(name, value, type, lineno, inline)

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

    def get_last_state(self):
        return self.states[-1]

    def first_last_state(self):
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

    def _add_var_state(self, name, value, type, lineno, inline):
        value_has_changed = self._detect_value_has_changed(value)
        new_state = VarState(name, value, type, lineno, inline, value_has_changed)
        self.states.append(new_state)

    def _detect_value_has_changed(self, new_value):
        if not self.states:
            return True
        last_state = self.get_last_state()
        try:
            if last_state.value != new_value:
                return True
            return False
        except Exception as e:
            return False

    def __str__(self):
        values = self.distinct_sequential_values()
        values_str = ", ".join(map(str, values))
        return f"{self.name}: {values_str}"


class State:
    def __init__(self, value, type, lineno):
        self.value = value
        self.type = type
        self.lineno = lineno

    def is_primitive(self):
        return self.type in ["int", "float", "complex", "str", "bool", "NoneType"]


class VarState(State):
    def __init__(self, name, value, type, lineno, inline, value_has_changed=False):
        super().__init__(value, type, lineno)
        self.name = name
        self.inline = inline
        self.value_has_changed = value_has_changed

    def __str__(self):
        return f"{self.name}: {self.value}"


class ArgState(State):
    def __init__(self, name, value, type, lineno):
        super().__init__(value, type, lineno)
        self.name = name
        self.lineno = lineno

    def __str__(self):
        return f"{self.name}: {self.value}"


class ReturnState(State):
    def __init__(self, value, type, lineno=0):
        super().__init__(value, type, lineno)

    def __str__(self):
        return f"{self.value}"

    def __eq__(self, other):
        return self.value == other


class YieldState(State):
    def __init__(self, value, type, lineno=0):
        super().__init__(value, type, lineno)

    def __str__(self):
        return f"{self.value}"

    def __eq__(self, other):
        return self.value == other


class ExceptionState(State):
    def __init__(self, value, type, lineno=0):
        super().__init__(value, type, lineno)

    def __str__(self):
        return f"{self.value}"

    def __eq__(self, other):
        return self.value == other
