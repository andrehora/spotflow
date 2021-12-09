import os
from happyflow.utils import write_csv, ensure_dir

REPORT_DIR = 'report_csv'
INDEX_FILE = 'index.csv'


class CSVCodeReport:

    def __init__(self, method_run, report_dir=None):
        self.method_run = method_run
        # self.trace_info = trace_info

        self.report_dir = report_dir
        if not self.report_dir:
            self.report_dir = REPORT_DIR
        ensure_dir(self.report_dir)

    def report(self):

        content = []
        line = ['pos', 'call_count', 'call_ratio', 'run_count', 'not_run_count']
        content.append(line)

        for flow in self.method_run.flows:
            line = [flow.pos, flow.info.call_count, flow.info.call_ratio,
                    flow.info.run_count, flow.info.not_run_count]
            content.append(line)

        pyfile = os.path.join(self.report_dir, self.method_run.method_info.full_name + '.csv')
        write_csv(pyfile, content)


class CSVIndexReport:

    def __init__(self, flow_result, report_dir=None):
        self.flow_result = flow_result

        self.report_dir = report_dir
        if not self.report_dir:
            self.report_dir = REPORT_DIR

        ensure_dir(self.report_dir)

    def report(self):

        content = []
        line = ['full_name', 'statements_count', 'total_flows', 'total_tests', 'total_calls',
                'top_flow_calls', 'top_flow_ratio']
        content.append(line)

        for method_run in self.flow_result:

            line = [method_run.method_info.full_name, method_run.info.statements_count, method_run.info.total_flows,
                    method_run.info.total_tests, method_run.info.total_calls, method_run.info.top_flow_calls,
                    method_run.info.top_flow_ratio]
            content.append(line)

        index_file = os.path.join(self.report_dir, INDEX_FILE)
        write_csv(index_file, content)
