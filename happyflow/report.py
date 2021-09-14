import trace
from collections import Counter
from happyflow.utils import *


class Report:

    def __init__(self, sut, flow_result):
        self.sut = sut
        self.flow_result = flow_result

    def sut_code(self):
        with open(self.sut.filename) as f:
            content = f.readlines()
            line_number = 0
            print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
            for line_code in content:
                line_number += 1
                if self.sut.has_line(line_number):
                    print(line_number, line_code.rstrip())

    def sut_run_code(self):
        with open(self.sut.filename) as f:
            content = f.readlines()
            line_number = 0
            print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
            for line_code in content:
                line_number += 1
                if self.sut.has_line(line_number):
                    line_run_count = self._run_count_for_line(line_number)
                    print(line_number, line_run_count, line_code.rstrip())

    def sut_most_common_flow(self):
        flow = self.most_common_flow()
        self._sut_common_flow(flow, 'Most')

    def sut_least_common_flow(self):
        flow = self.least_common_flow()
        self._sut_common_flow(flow, 'Least')


    def sut_code_state(self):

        state_result = self.flow_result.flows[0].state_result

        with open(self.sut.filename) as f:
            content = f.readlines()
            line_number = 0
            print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
            for line_code in content:
                line_number += 1
                if self.sut.has_line(line_number):

                    states = state_result.states_for_line(line_number)

                    line_run_count = self._run_count_for_line(line_number)
                    main_str = f'{line_number} {line_run_count} {line_code.rstrip()}'
                    main_str = main_str.ljust(50)
                    print(main_str, '|=>', states)

    def _sut_common_flow(self, flow, msg):

        flow_lines = flow[0]
        flow_count = flow[1]

        with open(self.sut.filename) as f:
            content = f.readlines()
            line_number = 0
            print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
            print(f'{msg} common flow |{flow_count}|: {flow_lines}')
            print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
            for line_code in content:
                line_number += 1
                if self.sut.has_line(line_number):

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
