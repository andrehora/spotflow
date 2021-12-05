from happyflow.utils import ratio
from happyflow.analysis import Analysis


class Report:

    def __init__(self, flow_result):
        self.flow_result = flow_result.filter(flow_result.has_calls)
        self.summary = []

    def html_report(self, report_dir):
        from happyflow.report_html import HTMLCodeReport, HTMLIndexReport
        for entity_info in self.get_report():
            HTMLCodeReport(entity_info, report_dir).report()
        HTMLIndexReport(self.summary, report_dir).report()

    def csv_report(self, report_dir):
        from happyflow.report_csv import CSVCodeReport, CSVIndexReport
        for entity_info in self.get_report():
            CSVCodeReport(entity_info, report_dir).report()
        CSVIndexReport(self.summary, report_dir).report()

    def txt_report(self):
        from happyflow.report_txt import TextReport
        for entity_info in self.get_report():
            TextReport(entity_info).report()

    def get_report(self):
        count = 0
        print(f'Report size: {len(self.flow_result)}')
        for method_trace in self.flow_result.values():
            count += 1
            # print(f'{count}. {entity_result.target_method.full_name}')
            entity_info = self.get_entity_info(method_trace)
            yield entity_info

    def get_entity_info(self, method_trace):

        entity_info = EntityInfo(method_trace)
        if not method_trace.calls:
            return entity_info

        analysis = Analysis(method_trace)
        most_common_run_lines = analysis.most_common_run_lines()
        entity_info.total_flows = len(most_common_run_lines)

        flow_pos = 0
        for run_lines in most_common_run_lines:
            flow_pos += 1
            distinct_lines = run_lines[0]

            grouped_method_trace = method_trace.group_by_run_lines(distinct_lines)
            flow_info = self.get_flow_info(entity_info, grouped_method_trace)
            flow_info.pos = flow_pos

            entity_info.append(flow_info)

        self.summary.append(EntitySummary(entity_info))
        return entity_info

    def get_flow_info(self, entity_info, method_trace):

        lineno = 0
        lineno_entity = entity_info.target_method.start_line - 1

        analysis = Analysis(method_trace)
        flow = Flow()
        flow.call_count = analysis.number_of_calls()
        flow.call_ratio = ratio(flow.call_count, entity_info.total_calls)
        flow.arg_values = analysis.most_common_args_pretty()
        return_values = analysis.most_common_return_values_pretty()
        if return_values:
            flow.return_values = return_values

        call = method_trace.calls[0]
        self._found_first_run_line = False

        for code, html in zip(entity_info.target_method.get_code_lines(), entity_info.target_method.get_html_lines()):

            lineno += 1
            lineno_entity += 1

            run_status = self.line_run_status(entity_info, call.run_lines, lineno_entity)
            state = self.get_state(entity_info, call, lineno_entity)

            line_info = LineInfo(lineno, lineno_entity, run_status, code.rstrip(), html, state)
            flow.append(line_info)
            flow.update_run_status(line_info)

        return flow

    def get_state(self, entity_info, flow, lineno_entity):

        states = flow.call_state.states_for_line(lineno_entity)

        if entity_info.target_method.line_is_entity_definition(lineno_entity):
            return self.arg_state(flow)
        elif flow.call_state.is_return_value(lineno_entity):
            return self.return_state(flow)
        elif states:
            return self.var_states(states)
        return ''

    def line_run_status(self, entity_info, flow_lines, current_line):

        if current_line in flow_lines:
            self._found_first_run_line = True
            return RunStatus.RUN

        # _find_executable_linenos of trace returns method/function definitions as executable lines (?).
        # We should flag those definitions as not executable lines (NOT_EXEC). Otherwise, the definitions
        # would impact on the flows. The solution for now is flagging all first lines as not executable
        # until we find the first run line. This way, the definitions are flagged as not executable lines...
        if not self._found_first_run_line:
            return RunStatus.NOT_EXEC

        if current_line not in flow_lines:
            if not entity_info.target_method.line_is_executable(current_line):
                return RunStatus.NOT_EXEC
            return RunStatus.NOT_RUN

    def arg_state(self, flow):
        arg_str = ''
        # separator = '# '
        for arg in flow.call_state.arg_states:
            if arg.name != 'self':
                arg_str += str(arg)
        return StateStatus.ARG, arg_str

    def return_state(self, flow):
        return_state = flow.call_state.return_state
        return StateStatus.RETURN, str(return_state)

    def var_states(self, states):
        return StateStatus.VAR, states


class StateStatus:
    ARG = 'arg'
    RETURN = 'return'
    VAR = 'var'


class RunStatus:
    NOT_RUN = 0
    RUN = 1
    NOT_EXEC = 2


class LineInfo:

    def __init__(self, lineno, lineno_entity, run_status, code, html, state):
        self.lineno = lineno
        self.lineno_entity = lineno_entity
        self.run_status = run_status
        self.code = code
        self.html = html
        self.state = state

    def is_run(self):
        return self.run_status == RunStatus.RUN

    def is_not_run(self):
        return self.run_status == RunStatus.NOT_RUN

    def is_not_exec(self):
        return self.run_status == RunStatus.NOT_EXEC


class Flow:

    def __init__(self):
        self.pos = 0
        self.lines_data = []

        self.run_count = 0
        self.not_run_count = 0
        self.not_exec_count = 0

        self.call_count = None
        self.call_ratio = None

        self.arg_values = None
        self.return_values = None

    def __len__(self):
        return len(self.lines_data)

    def __getitem__(self, position):
        return self.lines_data[position]

    def append(self, other):
        self.lines_data.append(other)

    def update_run_status(self, line_data):

        if line_data.is_run():
            self.run_count += 1
        if line_data.is_not_run():
            self.not_run_count += 1
        if line_data.is_not_exec():
            self.not_exec_count += 1


class EntityInfo:

    def __init__(self, method_trace):
        self.target_method = method_trace.target_method
        self.calls_data = []
        self.total_flows = 0
        self.total_calls = len(method_trace.calls)
        self.total_tests = len(method_trace.call_stack_tests())

    def __len__(self):
        return len(self.calls_data)

    def __getitem__(self, position):
        return self.calls_data[position]

    def append(self, other):
        self.calls_data.append(other)


class EntitySummary:

    def __init__(self, entity_info):
        self.full_name = entity_info.target_method.full_name
        self.full_name_escaped = entity_info.target_method.full_name_escaped()
        self.total_flows = entity_info.total_flows
        self.total_calls = entity_info.total_calls
        self.total_tests = entity_info.total_tests
        self.top_flow_calls = entity_info.calls_data[0].call_count
        self.top_flow_ratio = entity_info.calls_data[0].call_ratio
        self.statements_count = entity_info.target_method.executable_lines_count()
