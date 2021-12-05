from happyflow.utils import *

REPORT_DIR = 'report_csv'
INDEX_FILE = 'index.csv'


class CSVCodeReport:

    def __init__(self, entity_info, report_dir=None):
        self.entity_info = entity_info

        self.report_dir = report_dir
        if not self.report_dir:
            self.report_dir = REPORT_DIR
        ensure_dir(self.report_dir)

    def report(self):

        content = []
        line = ['pos', 'call_count', 'call_ratio', 'run_count', 'not_run_count']
        content.append(line)

        for flow_data in self.entity_info:
            line = [flow_data.pos, flow_data.call_count, flow_data.call_ratio,
                    flow_data.run_count, flow_data.not_run_count]
            content.append(line)

        pyfile = os.path.join(self.report_dir, self.entity_info.target_method.full_name + '.csv')
        write_csv(pyfile, content)


class CSVIndexReport:

    def __init__(self, summary, report_dir=None):
        self.summary = summary

        self.report_dir = report_dir
        if not self.report_dir:
            self.report_dir = REPORT_DIR

        ensure_dir(self.report_dir)

    def report(self):

        content = []
        line = ['full_name', 'statements_count', 'total_flows', 'total_tests', 'total_calls',
                'top_flow_calls', 'top_flow_ratio']
        content.append(line)

        for entity in self.summary:
            line = [entity.full_name, entity.statements_count, entity.total_flows, entity.total_tests,
                    entity.total_calls, entity.top_flow_calls, entity.top_flow_ratio]
            content.append(line)

        index_file = os.path.join(self.report_dir, INDEX_FILE)
        write_csv(index_file, content)
