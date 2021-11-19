from happyflow.utils import ratio
from happyflow.analysis import Analysis
from happyflow.report_html import HTMLCodeReport, HTMLIndexReport
from happyflow.report_txt import TextReport


class Report:

    def __init__(self, trace_result):
        self.trace_result = trace_result.filter(trace_result.has_flows)
        self.summary = []

    def html_report(self, report_dir):
        for entity_info in self.get_report():
            HTMLCodeReport(entity_info, report_dir).report()
        HTMLIndexReport(self.summary, report_dir).report()

    def txt_report(self):
        Report.txt(self.trace_result)

    def csv_report(self):
        pass

    def get_report(self):
        count = 0
        print(f'Report size: {len(self.trace_result)}')
        for entity_result in self.trace_result.values():
            count += 1
            print(f'{count}. {entity_result.target_entity.full_name}')
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
            target_run_lines = run_lines[0]

            flow_result = entity_result.flow_by_lines(target_run_lines)
            flow_info = self.get_flow_info(entity_info, flow_result)
            flow_info.pos = flow_pos

            entity_info.append(flow_info)

        self.summary.append(EntitySummary(entity_info))
        return entity_info

    def get_flow_info(self, entity_info, flow_result):

        lineno = 0
        lineno_entity = entity_info.target_entity.start_line - 1

        analysis = Analysis(entity_info.target_entity, flow_result)
        flow_info = FlowInfo()
        flow_info.call_count = analysis.number_of_calls()
        flow_info.call_ratio = ratio(flow_info.call_count, entity_info.total_calls)
        flow_info.arg_values = analysis.most_common_args_pretty()
        return_values = analysis.most_common_return_values_pretty()
        if return_values:
            flow_info.return_values = return_values

        flow = flow_result.flows[0]

        for code, html in zip(entity_info.target_entity.get_code_lines(), entity_info.target_entity.get_html_lines()):

            lineno += 1
            lineno_entity += 1

            run_status = self.line_run_status(entity_info, flow.run_lines, lineno_entity, entity_info.target_entity.start_line)
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

    def line_run_status(self, entity_info, flow_lines, current_line, start_line):

        if current_line in flow_lines: #or current_line == start_line:
            return RunStatus.RUN

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

    @staticmethod
    def txt(trace_result):
        for entity_name in trace_result:
            entity_result = trace_result[entity_name]
            report = TextReport(entity_result.target_entity, entity_result)
            report.show_most_common_args_and_return_values(show_code=True)


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
        # self.name = entity_info.target_entity.name
        self.full_name = entity_info.target_entity.full_name
        self.total_flows = entity_info.total_flows
        self.total_calls = entity_info.total_calls
        self.total_tests = entity_info.total_tests
        self.top_flow_calls = entity_info.flows_data[0].call_count
        self.top_flow_ratio = entity_info.flows_data[0].call_ratio
        self.statements_count = entity_info.target_entity.executable_lines_count()
