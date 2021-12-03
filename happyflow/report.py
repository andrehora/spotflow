from happyflow.utils import ratio
from happyflow.analysis import Analysis


class Report:

    def __init__(self, flow_result):
        self.flow_result = flow_result.filter(flow_result.has_flows)
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
        for entity_result in self.flow_result.values():
            count += 1
            # print(f'{count}. {entity_result.target_entity.full_name}')
            entity_info = self.get_entity_info(entity_result)
            yield entity_info

    def get_entity_info(self, entity_result):

        entity_info = EntityInfo(entity_result)
        if not entity_result.flows:
            return entity_info

        analysis = Analysis(entity_result.target_entity, entity_result)
        most_common_run_lines = analysis.most_common_run_lines()
        entity_info.total_flows = len(most_common_run_lines)

        flow_pos = 0
        for run_lines in most_common_run_lines:
            flow_pos += 1
            distinct_lines = run_lines[0]

            flow_container = entity_result.flow_by_lines(distinct_lines)
            flow_info = self.get_flow_info(entity_info, flow_container)
            flow_info.pos = flow_pos

            entity_info.append(flow_info)

        self.summary.append(EntitySummary(entity_info))
        return entity_info

    def get_flow_info(self, entity_info, flow_container):

        lineno = 0
        lineno_entity = entity_info.target_entity.start_line - 1

        analysis = Analysis(entity_info.target_entity, flow_container)
        flow_info = FlowInfo()
        flow_info.call_count = analysis.number_of_calls()
        flow_info.call_ratio = ratio(flow_info.call_count, entity_info.total_calls)
        flow_info.arg_values = analysis.most_common_args_pretty()
        return_values = analysis.most_common_return_values_pretty()
        if return_values:
            flow_info.return_values = return_values

        flow = flow_container.flows[0]
        self._found_first_run_line = False

        for code, html in zip(entity_info.target_entity.get_code_lines(), entity_info.target_entity.get_html_lines()):

            lineno += 1
            lineno_entity += 1

            run_status = self.line_run_status(entity_info, flow.run_lines, lineno_entity)
            state = self.get_state(entity_info, flow, lineno_entity)

            line_info = LineInfo(lineno, lineno_entity, run_status, code.rstrip(), html, state)
            flow_info.append(line_info)
            flow_info.update_run_status(line_info)

        return flow_info

    def get_state(self, entity_info, flow, lineno_entity):

        states = flow.state_history.states_for_line(lineno_entity)

        if entity_info.target_entity.line_is_entity_definition(lineno_entity):
            return self.arg_state(flow)
        elif flow.state_history.is_return_value(lineno_entity):
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
            if not entity_info.target_entity.line_is_executable(current_line):
                return RunStatus.NOT_EXEC
            return RunStatus.NOT_RUN

    def arg_state(self, flow):
        arg_str = ''
        # separator = '# '
        for arg in flow.state_history.arg_states:
            if arg.name != 'self':
                arg_str += str(arg)
        return StateStatus.ARG, arg_str

    def return_state(self, flow):
        return_state = flow.state_history.return_state
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


class FlowInfo:

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

    def __init__(self, entity_result):
        self.target_entity = entity_result.target_entity
        self.flows_data = []
        self.total_flows = 0
        self.total_calls = len(entity_result.flows)
        self.total_tests = len(entity_result.callers_tests())

    def __len__(self):
        return len(self.flows_data)

    def __getitem__(self, position):
        return self.flows_data[position]

    def append(self, other):
        self.flows_data.append(other)


class EntitySummary:

    def __init__(self, entity_info):
        self.full_name = entity_info.target_entity.full_name
        self.full_name_escaped = entity_info.target_entity.full_name_escaped()
        self.total_flows = entity_info.total_flows
        self.total_calls = entity_info.total_calls
        self.total_tests = entity_info.total_tests
        self.top_flow_calls = entity_info.flows_data[0].call_count
        self.top_flow_ratio = entity_info.flows_data[0].call_ratio
        self.statements_count = entity_info.target_entity.executable_lines_count()
