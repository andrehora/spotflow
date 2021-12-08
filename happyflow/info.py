from collections import Counter
from happyflow.utils import ratio


class RunInfo:

    def __init__(self, method_trace):
        self.full_name = method_trace.target_method.full_name
        self.full_name_escaped = method_trace.target_method.full_name_escaped()
        self.total_calls = len(method_trace.calls)
        self.total_tests = len(method_trace.call_stack_tests())
        self.statements_count = method_trace.target_method.executable_lines_count()

        self.total_flows = len(method_trace.flows)
        self.top_flow_calls = method_trace.flows[0].info.call_count
        self.top_flow_ratio = method_trace.flows[0].info.call_ratio

        self.has_exception = method_trace.has_exception


class FlowInfo:

    def __init__(self, method_flow, method_trace):
        self.lines = []

        self.run_count = 0
        self.not_run_count = 0
        self.not_exec_count = 0

        self.call_count = len(method_flow.calls)
        self.call_ratio = ratio(self.call_count, len(method_trace.calls))

        self.arg_values = Analysis(method_flow).most_common_args_pretty()
        self.return_values = Analysis(method_flow).most_common_return_values_pretty()

    def append(self, other):
        self.lines.append(other)

    def update_run_status(self, line_info):
        if line_info.is_run():
            self.run_count += 1
        if line_info.is_not_run():
            self.not_run_count += 1
        if line_info.is_not_exec():
            self.not_exec_count += 1

    def __len__(self):
        return len(self.lines)

    def __getitem__(self, position):
        return self.lines[position]


class LineInfo:

    def __init__(self, lineno, lineno_entity, run_status, state, target_method):
        self.lineno = lineno
        self.lineno_entity = lineno_entity
        self.run_status = run_status
        self.state = state
        self.target_method = target_method

    def code(self):
        return self.target_method.get_code_line_at_lineno(self.lineno)

    def html(self):
        return self.target_method.get_html_line_at_lineno(self.lineno)

    def is_run(self):
        return self.run_status == RunStatus.RUN

    def is_not_run(self):
        return self.run_status == RunStatus.NOT_RUN

    def is_not_exec(self):
        return self.run_status == RunStatus.NOT_EXEC


class StateStatus:
    ARG = 'arg'
    RETURN = 'return'
    VAR = 'var'


class RunStatus:
    NOT_RUN = 0
    RUN = 1
    NOT_EXEC = 2


class Analysis:

    def __init__(self, call_container):
        self.call_container = call_container

    def number_of_distinct_flows(self):
        return len(set(self.call_container.distinct_run_lines()))

    def number_of_calls(self):
        return len(self.call_container.calls)

    def most_common_run_lines(self):
        lines = self.call_container.distinct_run_lines()
        return self._most_common(lines)

    def most_common_args(self):
        args = self.call_container.arg_states()
        args_count = {}

        for arg in args:
            args_count[arg] = self._most_common(args[arg])

        return args_count

    def most_common_args_pretty(self):
        return self.pretty_args(self.most_common_args())

    def most_common_return_values(self):
        values = self.call_container.return_states()
        return self._most_common(values)

    def most_common_return_values_pretty(self):
        return self.pretty_return_values(self.most_common_return_values())

    def _most_common(self, elements, n=10):
        try:
            return Counter(elements).most_common(n)
        except TypeError:
            return []

    def pretty_args(self, args, max_len=150):
        result = []
        for arg_name in args:
            arg_value = {}
            arg_value['name'] = arg_name
            values = ''
            for value in args[arg_name]:
                value_str = value[0]
                count = value[1]
                values += f'{value_str} ({count}) '
            arg_value['value'] = self.clear_values(values, max_len)
            result.append(arg_value)
        return result

    def pretty_return_values(self, return_values, max_len=150):
        values = ''
        for value in return_values:
            values += f'{value[0]} ({value[1]}) '
        if values:
            return self.clear_values(values, max_len)
        return None

    def clear_values(self, values, max_len):
        # values = values.rstrip(', ')
        if len(values) >= max_len:
            values = f'{values[0:max_len]}...'
        return values