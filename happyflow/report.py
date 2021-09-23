import trace
from collections import Counter
from happyflow.utils import *


class Report:

    def __init__(self, target_entity, flow_result):
        self.target_entity = target_entity
        self.flow_result = flow_result

    def sut_code(self):
        with open(self.target_entity.filename) as f:
            content = f.readlines()
            line_number = 0
            print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
            for line_code in content:
                line_number += 1
                if self.target_entity.has_line(line_number):
                    print(line_number, line_code.rstrip())

    def sut_run_code(self):
        with open(self.target_entity.filename) as f:
            content = f.readlines()
            line_number = 0
            print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
            for line_code in content:
                line_number += 1
                if self.target_entity.has_line(line_number):
                    line_run_count = self._run_count_for_line(line_number)
                    print(line_number, line_run_count, line_code.rstrip())

    def sut_most_common_flow(self):
        flow = self.most_common_flow()
        self._sut_common_flow(flow, 'Most')

    def sut_least_common_flow(self):
        flow = self.least_common_flow()
        self._sut_common_flow(flow, 'Least')

    def sut_code_state(self, state_summary=False):

        flow = self.flow_result.flows[0]

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
                    elif states:
                        separator = '🟡 '
                        states_str = f'{separator}{separator.join(states)}'
                        print(code_str, states_str)
                    elif state_result.is_line_return_value(current_line):
                        separator = '🟢 '
                        return_value = state_result.return_value
                        return_str = f'{separator}{return_value}'
                        print(code_str, return_str)
                    else:
                        print(code_str)

    def show_state_summary(self, state_result):
        print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        for arg in state_result.args:
            if arg.name != 'self':
                arg_summary = f'🔴 {arg.name}: {str(arg.value)}'
                print(arg_summary)


        for var in state_result.vars:
            if var != 'self':
                state_history = state_result.vars[var]
                values = state_history.distinct_sequential_values()
                values_str = ' -> '.join(map(str, values))
                var_summary = f'🟡 {var}: {values_str}'
                print(var_summary)

        if state_result.return_value is not None:
            return_summary = f'🟢 {state_result.return_value}'
            print(return_summary)

    def _sut_common_flow(self, flow, msg):

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

    def most_common_flow(self):
        run_lines = self._run_lines_as_tuple()
        return Counter(run_lines).most_common(1)[0]

    def least_common_flow(self):
        run_lines = self._run_lines_as_tuple()
        return Counter(run_lines).most_common()[-1]

    def _run_count_for_line(self, line_number):

        if not self.target_entity.line_is_executable(line_number):
            return ''

        run_count = 0
        for flow in self.flow_result.flows:
            if line_number in flow.distinct_lines():
                run_count += 1
        return run_count

    def _run_lines_as_tuple(self):
        result = []
        for flow in self.flow_result.flows:
            result.append(tuple(flow.distinct_lines()))
        return result

    # def update_counts_with_executable_line(self):
    #     for filename in self.run_files_and_lines:
    #         executable_lines = trace._find_executable_linenos(filename)
    #         for exec_line in executable_lines:
    #             key = (filename, exec_line)
    #             self.counts[key] = self.counts.get(key, 0)
    #
    # def get_counts(self, filename, line_number):
    #     return self.counts.get((filename, line_number), -1)
    #
    # def annotate_file(self, filename):
    #     with open(filename) as f:
    #         content = f.readlines()
    #         line_number = 0
    #         for line_code in content:
    #             line_number += 1
    #             exec_count = self.get_counts(filename, line_number)
    #             print(line_number, exec_count, line_code.rstrip())


# from happyflow.sut_loader import SUTLoader
# from happyflow.tracer import TraceRunner
#
# sut = SUTLoader.find_sut('message._parseparam')
# trace_result = TraceRunner.trace('tests.stub_test.TestComplexFlow', sut)
# flow_result = sut.local_flows(trace_result)
#
# report = Report(sut, flow_result)
# report.sut_least_common_flow()
#
# for flow in flow_result.flows:
#     print(flow.run_lines)
