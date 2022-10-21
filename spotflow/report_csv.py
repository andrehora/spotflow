import os
from spotflow.utils import write_csv, ensure_dir

REPORT_DIR = 'spotflow_csv_report'
INDEX_FILE = 'index.csv'


class CSVCodeReport:

    def __init__(self, monitored_method, report_dir=None):
        self.monitored_method = monitored_method
        # self.trace_info = trace_info

        self.report_dir = report_dir
        if not self.report_dir:
            self.report_dir = REPORT_DIR
        ensure_dir(self.report_dir)

    def report(self):

        content = []
        line = ['pos', 'call_count', 'call_ratio', 'run_count', 'not_run_count']
        content.append(line)

        for flow in self.monitored_method.flows:
            line = [flow.pos, flow.info.call_count, flow.info.call_ratio,
                    flow.info.run_count, flow.info.not_run_count]
            content.append(line)

        pyfile = os.path.join(self.report_dir, self.monitored_method.info.full_name + '.csv')
        write_csv(pyfile, content)


class CSVIndexReport:

    def __init__(self, monitored_system, report_dir=None):
        self.monitored_system = monitored_system

        self.report_dir = report_dir
        if not self.report_dir:
            self.report_dir = REPORT_DIR

        ensure_dir(self.report_dir)

    def report(self):

        content = []
        line = ['full_name',
                'coverage_ratio', 'run_lines_count', 'executable_lines_count',
                'total_tests', 'total_calls', 'total_exceptions',
                'total_flows', 'top_flow_calls', 'top_flow_ratio']
        content.append(line)

        for monitored_method in self.monitored_system:

            line = [monitored_method.info.full_name,

                    monitored_method.info.coverage_ratio,
                    monitored_method.info.run_lines_count,
                    monitored_method.info.executable_lines_count,

                    monitored_method.info.total_tests,
                    monitored_method.info.total_calls,
                    monitored_method.info.total_exceptions,

                    monitored_method.info.total_flows,
                    monitored_method.info.top_flow_calls,
                    monitored_method.info.top_flow_ratio]

            content.append(line)

        index_file = os.path.join(self.report_dir, INDEX_FILE)
        write_csv(index_file, content)
