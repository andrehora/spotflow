import os
from happyflow.utils import write_csv, ensure_dir

REPORT_DIR = 'report_csv'
INDEX_FILE = 'index.csv'


class CSVCodeReport:

    def __init__(self, traced_method, report_dir=None):
        self.traced_method = traced_method
        # self.trace_info = trace_info

        self.report_dir = report_dir
        if not self.report_dir:
            self.report_dir = REPORT_DIR
        ensure_dir(self.report_dir)

    def report(self):

        content = []
        line = ['pos', 'call_count', 'call_ratio', 'run_count', 'not_run_count']
        content.append(line)

        for flow in self.traced_method.flows:
            line = [flow.pos, flow.info.call_count, flow.info.call_ratio,
                    flow.info.run_count, flow.info.not_run_count]
            content.append(line)

        pyfile = os.path.join(self.report_dir, self.traced_method.info.full_name + '.csv')
        write_csv(pyfile, content)


class CSVIndexReport:

    def __init__(self, traced_system, report_dir=None):
        self.traced_system = traced_system

        self.report_dir = report_dir
        if not self.report_dir:
            self.report_dir = REPORT_DIR

        ensure_dir(self.report_dir)

    def report(self):

        content = []
        line = ['full_name', 'statements_count', 'total_flows', 'total_tests', 'total_calls',
                'top_flow_calls', 'top_flow_ratio']
        content.append(line)

        for traced_method in self.traced_system:

            line = [traced_method.info.full_name, traced_method.info.statements_count, traced_method.info.total_flows,
                    traced_method.info.total_tests, traced_method.info.total_calls, traced_method.info.top_flow_calls,
                    traced_method.info.top_flow_ratio]
            content.append(line)

        index_file = os.path.join(self.report_dir, INDEX_FILE)
        write_csv(index_file, content)
