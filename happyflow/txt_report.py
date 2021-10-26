import collections
from happyflow.analysis import Analysis
from happyflow.utils import read_file_lines


class TextReport:

    def __init__(self, target_entity, flow_result):
        self.target_entity = target_entity
        self.flow_result = flow_result
        self.analysis = Analysis(self.target_entity, self.flow_result)

    def show_most_common_args_and_return_values(self, n=None, show_code=False):
        print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        print('Target entity:', self.target_entity)
        print('Executable lines:', len(self.target_entity.executable_lines()))
        print('Total flows:', self.analysis.number_of_flows(),  'Distinct:', self.analysis.number_of_distinct_flows())
        # exec_lines = self.target_entity.executable_lines()
        # print(f'Executable lines ({len(exec_lines)}): {exec_lines}')
        count = 0
        for flow in self.analysis.most_common_flow(n):
            count += 1
            target_flow_lines = flow[0]
            flow_result = self.flow_result.flow_result_by_lines(target_flow_lines)
            analysis = Analysis(self.target_entity, flow_result)

            print(f'=-=-=-=-=-=-=-= Flow {count} =-=-=-=-=-=-=-=')
            print('Total:', analysis.number_of_flows())
            print(f'Flow ({len(target_flow_lines)}): {target_flow_lines}')
            print('Args:', analysis.most_common_args())
            print('Return values:', analysis.most_common_return_values())

            if show_code:
                report = TextReport(self.target_entity, flow_result)
                report.show_code_state(state_summary=True, flow_number=0)

    def show_code(self):
        with open(self.target_entity.filename) as f:
            content = f.readlines()
            line_number = 0
            print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
            for line_code in content:
                line_number += 1
                if self.target_entity.has_line(line_number):
                    print(line_number, line_code.rstrip())

    def show_run_code(self):
        with open(self.target_entity.filename) as f:
            content = f.readlines()
            line_number = 0
            print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
            for line_code in content:
                line_number += 1
                if self.target_entity.has_line(line_number):
                    line_run_count = self._run_count_for_line(line_number)
                    print(line_number, line_run_count, line_code.rstrip())

    def show_most_common_flow(self):

        flow = self.analysis.most_common_flow()
        self._common_flow(flow, 'Most')

    def show_least_common_flow(self):
        flow = self.analysis.least_common_flow()
        self._common_flow(flow, 'Least')

    def show_code_state(self, state_summary=False, flow_number=0):

        flow = self.flow_result.flows[flow_number]

        state_result = flow.state_result
        flow_lines = flow.run_lines

        if state_summary:
            self.show_state_summary(state_result)
        print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        content = read_file_lines(self.target_entity.filename)
        current_line = 0
        for line_code in content:
            current_line += 1
            if self.target_entity.has_line(current_line):

                states = state_result.states_for_line(current_line)

                if current_line in flow_lines:
                    is_run = '✅'
                if current_line not in flow_lines:
                    is_run = '❌'
                if not self.target_entity.line_is_executable(current_line):
                    is_run = '⬜'

                line_number_str = str(current_line).ljust(2)
                is_run = is_run.ljust(3)

                code_str = f'{line_number_str} {is_run} {line_code.rstrip()}'
                code_str = code_str.ljust(50)

                if self.target_entity.is_entity_definition(current_line):
                    arg_summary = ''
                    separator = '🟢 '
                    for arg in state_result.args:
                        if arg.name != 'self':
                            arg_summary += f'{separator}{arg} '
                    if arg_summary:
                        print(code_str, arg_summary)
                    else:
                        print(code_str)
                elif state_result.is_return_value(current_line):
                    separator = '🔴 '
                    return_state = state_result.return_state
                    return_str = f'{separator}{return_state}'
                    print(code_str, return_str)
                elif states:
                    separator = '🟡 '
                    states_str = f'{separator}{separator.join(states)}'
                    print(code_str, states_str)
                else:
                    print(code_str)

    def show_state_summary(self, state_result):
        print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        for arg in state_result.args:
            if arg.name != 'self':
                arg_summary = f'🟢 IN {arg.name}: {str(arg.value)}'
                print(arg_summary)

        if state_result.has_return():
            return_summary = f'🔴 OUT {state_result.return_state}'
            print(return_summary)

        for var in state_result.vars:
            if var != 'self':
                state_history = state_result.vars[var]
                values = state_history.distinct_sequential_values()
                values_str = ' -> '.join(map(str, values))
                var_summary = f'🟡 {var}: {values_str}'
                print(var_summary)

    def _common_flow(self, flow, msg):

        flow_lines = flow[0]
        flow_count = flow[1]

        with open(self.target_entity.filename) as f:
            content = f.readlines()
            line_number = 0
            print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
            print(f'{msg} common flow |{flow_count}|: {flow_lines}')
            print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
            for line_code in content:
                line_number += 1
                if self.target_entity.has_line(line_number):

                    if line_number in flow_lines:
                        flag = 1
                    else:
                        flag = 0

                    print(line_number, flag, line_code.rstrip())

    def _run_count_for_line(self, line_number):

        if not self.target_entity.line_is_executable(line_number):
            return ''

        run_count = 0
        for flow in self.flow_result.flows:
            if line_number in flow.distinct_lines():
                run_count += 1
        return run_count

    def code_flows_and_states(self, flow_number=None):
        code_lines = read_file_lines(self.target_entity.filename)
        if flow_number is not None:
            flow = self.flow_result.flows[flow_number]
            return self.code_flow_and_state(code_lines, flow)

        for flow in self.flow_result.flows:
            self.code_flow_and_state(code_lines, flow)

    def code_flow_and_state(self, code_lines, flow):
        lineno_entity = 0
        lineno = 0
        entity_info = EntityInfo()
        for code in code_lines:
            lineno_entity += 1
            if self.target_entity.has_line(lineno_entity):

                lineno += 1
                run_status = self.line_run_status(flow.run_lines, lineno_entity)

                states = flow.state_result.states_for_line(lineno_entity)

                if self.target_entity.is_entity_definition(lineno_entity):
                    state = self.arg_state(flow)
                elif flow.state_result.is_return_value(lineno_entity):
                    state = self.return_state(flow)
                elif states:
                    state = self.var_states(states)
                else:
                    state = ''

                line_info = LineInfo(lineno, lineno_entity, run_status, code.rstrip(), state)
                entity_info.append(line_info)
        return entity_info


    def line_run_status(self, flow_lines, current_line):
        if not self.target_entity.line_is_executable(current_line):
            return 'N'
        if current_line in flow_lines:
            return 'T'
        if current_line not in flow_lines:
            return 'F'

    def arg_state(self, flow):
        arg_str = ''
        # separator = '# '
        for arg in flow.state_result.args:
            if arg.name != 'self':
                arg_str += str(arg)
        return 'arg', arg_str

    def return_state(self, flow):
        return_state = flow.state_result.return_state
        return 'return', str(return_state)

    def var_states(self, states):
        return 'var', states


LineInfo = collections.namedtuple('LineInfo', ['lineno', 'lineno_entity', 'run_status', 'code', 'state'])


class EntityInfo:

    def __init__(self):
        self.lines_info = []

    def __len__(self):
        return len(self.lines_info)

    def __getitem__(self, position):
        return self.lines_info[position]

    def append(self, other):
        self.lines_info.append(other)