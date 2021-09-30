from happyflow.analysis import Analysis


class TextReport:

    def __init__(self, target_entity, flow_result):
        self.target_entity = target_entity
        self.flow_result = flow_result
        self.analysis = Analysis(self.target_entity, self.flow_result)

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

        with open(self.target_entity.filename) as f:

            if state_summary:
                self.show_state_summary(state_result)
            print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')

            content = f.readlines()
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
                    if self.target_entity.line_is_definition(current_line):
                        arg_summary = ''
                        separator = '🔴 '
                        for arg in state_result.args:
                            if arg.name != 'self':
                                arg_summary += f'{separator}{arg} '
                        if arg_summary:
                            print(code_str, arg_summary)
                        else:
                            print(code_str)
                    elif state_result.is_line_return_value(current_line):
                        separator = '🟢 '
                        return_value = state_result.return_value
                        return_str = f'{separator}{return_value}'
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
                arg_summary = f'🔴 IN  {arg.name}: {str(arg.value)}'
                print(arg_summary)

        if state_result.has_return():
            return_summary = f'🟢 OUT {state_result.return_value}'
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

