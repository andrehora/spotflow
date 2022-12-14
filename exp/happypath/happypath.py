from spotflow.model import CallContainer
from spotflow.utils import ratio
from exp.happypath import report
from collections import Counter


def spotflow_post(monitored_program, *args):

    compute_paths(monitored_program)

    dir = args[0]
    rep = report.Report(monitored_program)
    rep.html_report(dir)


def compute_paths(monitored_program):

    for monitored_method in monitored_program.all_methods():
        flows = compute_paths_for_method(monitored_method)

        monitored_method.flows = flows
        monitored_method.info.total_flows = len(monitored_method.flows)
        monitored_method.info.top_flow_calls = monitored_method.flows[0].path_info.call_count
        monitored_method.info.top_flow_ratio = monitored_method.flows[0].path_info.call_ratio


def compute_paths_for_method(monitored_method):

    most_common_run_lines = Analysis(monitored_method).most_common_run_lines()
    flow_pos = 0
    flows = []
    for run_lines in most_common_run_lines:
        flow_pos += 1
        distinct_run_lines = run_lines[0]

        flow_calls = select_calls_by_lines(monitored_method, distinct_run_lines)
        flow = create_path(flow_pos, distinct_run_lines, flow_calls, monitored_method)
        flows.append(flow)

    return flows


def select_calls_by_lines(monitored_method, distinct_lines):
    calls = []
    for call in monitored_method.calls:
        if tuple(call.distinct_run_lines()) == tuple(distinct_lines):
            calls.append(call)
    return calls


def create_path(flow_pos, distinct_run_lines, flow_calls, monitored_method):
    flow = MethodPath(flow_pos, distinct_run_lines, flow_calls, monitored_method)
    flow.update_path_info()
    return flow


class MethodPath(CallContainer):

    def __init__(self, pos, distinct_run_lines, calls, monitored_method):
        super().__init__(calls)
        self.pos = pos
        self.distinct_run_lines = distinct_run_lines
        self.monitored_method = monitored_method
        self.path_info = PathInfo(self.monitored_method, self.calls[0])

        self.call_count = len(self.calls)
        total_calls = len(self.monitored_method.calls)
        self.call_ratio = ratio(self.call_count, total_calls)

        self.arg_values = Analysis(self).most_common_args_pretty()
        self.return_values = Analysis(self).most_common_return_values_pretty()
        self.yield_values = Analysis(self).most_common_yield_values_pretty()
        self.exception_values = Analysis(self).most_common_exception_values_pretty()


class PathInfo:

    def __init__(self, monitored_method, call):
        self.monitored_method = monitored_method
        self.call = call
        self.distinct_run_lines = self.call.distinct_run_lines()

        self.lines = []
        self.run_count = 0
        self.not_run_count = 0
        self.not_exec_count = 0

        self._found_first_run_line = False
        self.create_lines()

    def create_lines(self):
        lineno = 0

        for lineno_entity in range(self.monitored_method.info.start_line, self.monitored_method.info.end_line+1):
            lineno += 1

            line_status = self.get_line_status(lineno_entity)
            line_type, line_state = self.get_line_state(lineno_entity)
            line_info = LineInfo(lineno, lineno_entity, line_status, line_type, line_state, self.monitored_method.info)

            self.lines.append(line_info)
            self.update_run_status(line_info)

    def get_line_status(self, current_line):

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
            if not self.monitored_method.info._line_is_executable(current_line):
                return RunStatus.NOT_EXEC

        return RunStatus.NOT_RUN

    def get_line_state(self, lineno):

        if self.monitored_method.info.start_line == lineno:
            return self.line_arg_state()

        if lineno in self.monitored_method.info.return_lines:
            return self.line_return_state()

        states = self.call.call_state._states_for_line(lineno)
        if states:
            return self.line_var_states(states)
        return '', ''

    def line_arg_state(self):
        arg_str = ''
        for arg in self.call.call_state.arg_states:
            if arg.name != 'self':
                arg_str += str(arg)
        return LineType.ARG, arg_str

    def line_return_state(self):
        return_state = self.call.call_state.return_state
        return LineType.RETURN, str(return_state)

    def line_var_states(self, states):
        return LineType.VAR, states

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

    def __init__(self, lineno, lineno_entity, run_status, type, state, method_info):
        self.lineno = lineno
        self.lineno_entity = lineno_entity
        self.run_status = run_status
        self.type = type
        self.state = state
        self.method_info = method_info

    def code(self):
        return self.method_info.get_code_line_at_lineno(self.lineno)

    def html(self):
        return self.method_info.get_html_line_at_lineno(self.lineno)

    def is_run(self):
        return self.run_status == RunStatus.RUN

    def is_not_run(self):
        return self.run_status == RunStatus.NOT_RUN

    def is_not_exec(self):
        return self.run_status == RunStatus.NOT_EXEC

    def is_arg(self):
        return self.type == LineType.ARG

    def is_return(self):
        return self.type == LineType.RETURN

    def is_var(self):
        return self.type == LineType.VAR


class LineType:
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

    def number_of_calls(self):
        return len(self.call_container.calls)

    def most_common_run_lines(self):
        lines = self.call_container.all_distinct_run_lines()
        return self.most_common(lines)

    def most_common_arg_values(self):
        args = self.call_container.arg_states()
        args_count = {}

        for arg in args:
            args_count[arg] = self.most_common(args[arg])

        return args_count

    def most_common_return_values(self):
        values = self.call_container.return_states()
        return self.most_common(values)

    def most_common_yield_values(self):
        values = self.call_container.yield_states()
        return self.most_common(values)

    def most_common_exception_values(self):
        values = self.call_container.exception_states()
        return self.most_common(values)

    def most_common_args_pretty(self):
        return self.pretty_args(self.most_common_arg_values())

    def most_common_return_values_pretty(self):
        return self.pretty_return_values(self.most_common_return_values())

    def most_common_yield_values_pretty(self):
        return self.pretty_return_values(self.most_common_yield_values())

    def most_common_exception_values_pretty(self):
        return self.pretty_return_values(self.most_common_exception_values())

    def most_common(self, elements, n=10):
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
