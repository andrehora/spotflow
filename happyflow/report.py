import collections
from happyflow.analysis import Analysis
from happyflow.report_html import HTMLReport


class Report:

    def __init__(self, target_entity, flow_result):
        self.target_entity = target_entity
        self.flow_result = flow_result
        self.analysis = Analysis(self.target_entity, self.flow_result)

    def html_report(self):
        entity_data = self.get_entity_data()
        return HTMLReport(entity_data, self.analysis).report()

    def txt_report(self):
        pass

    def get_entity_data(self, flow_number=None):

        entity_data = EntityData.build_from(self.target_entity)

        if flow_number is not None:
            flow = self.flow_result.flows[flow_number]
            flow_data = self.get_flow_data(entity_data, flow)
            entity_data.append(flow_data)
            return entity_data

        most_common_flows = self.analysis.most_common_flow()
        entity_data.total_flows = len(most_common_flows)

        flow_pos = 0
        for flow in most_common_flows:
            flow_pos += 1
            target_flow_lines = flow[0]

            flow_result = self.flow_result.flow_result_by_lines(target_flow_lines)
            flow_data = self.get_flow_data(entity_data, flow_result)
            flow_data.pos = flow_pos

            entity_data.append(flow_data)

        return entity_data

    def get_flow_data(self, entity_data, flow_result):

        lineno = 0
        lineno_entity = entity_data.start_line - 1

        analysis = Analysis(self.target_entity, flow_result)

        flow_data = FlowData()
        flow_data.call_count = analysis.number_of_calls()
        flow_data.arg_values = analysis.most_common_args_pretty()
        return_values = analysis.most_common_return_values_pretty()
        if return_values:
            flow_data.return_values = return_values

        entity_data.total_calls += flow_data.call_count
        flow = flow_result.flows[0]

        for code, html in zip(entity_data.code_lines, entity_data.html_lines):

            lineno += 1
            lineno_entity += 1

            run_status = self.line_run_status(flow.run_lines, lineno_entity, entity_data.start_line)
            state = self.get_state(flow, lineno_entity)

            line_data = LineData(lineno, lineno_entity, run_status, code.rstrip(), html, state)
            flow_data.append(line_data)
            flow_data.update_run_status(line_data)

        return flow_data

    def get_state(self, flow, lineno_entity):

        states = flow.state_result.states_for_line(lineno_entity)

        if self.target_entity.line_is_entity_definition(lineno_entity):
            return self.arg_state(flow)
        elif flow.state_result.is_return_value(lineno_entity):
            return self.return_state(flow)
        elif states:
            return self.var_states(states)
        return ''

    def line_run_status(self, flow_lines, current_line, start_line):

        if current_line in flow_lines: #or current_line == start_line:
            return RunStatus.RUN

        if current_line not in flow_lines:
            if not self.target_entity.line_is_executable(current_line):
                return RunStatus.NOT_EXEC
            return RunStatus.NOT_RUN

    def arg_state(self, flow):
        arg_str = ''
        # separator = '# '
        for arg in flow.state_result.args:
            if arg.name != 'self':
                arg_str += str(arg)
        return StateStatus.ARG, arg_str

    def return_state(self, flow):
        return_state = flow.state_result.return_state
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


class LineData:

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


class FlowData:

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


class EntityData:

    def __init__(self, name, full_name, filename, start_line, end_line, code_lines, html_lines, exec_lines_count):
        self.name = name
        self.full_name = full_name
        self.filename = filename
        self.start_line = start_line
        self.end_line = end_line
        self.code_lines = code_lines
        self.html_lines = html_lines
        self.exec_lines_count = exec_lines_count

        self.flows_data = []
        self.total_flows = 0
        self.total_calls = 0

    def __len__(self):
        return len(self.flows_data)

    def __getitem__(self, position):
        return self.flows_data[position]

    def append(self, other):
        self.flows_data.append(other)

    @classmethod
    def build_from(cls, entity):
        return EntityData(entity.name, entity.full_name(), entity.filename,
                          entity.start_line, entity.end_line,
                          entity.get_code_lines(), entity.get_html_lines(),
                          len(entity.executable_lines()))