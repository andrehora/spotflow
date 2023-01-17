import os
from spotflow.utils import write_csv, full_filename, full_dir, ensure_dir


REPORT_DIR = 'happypath_csv'
INDEX_FILE = 'index.csv'


class CSVCodeReport:

    def __init__(self, monitored_method, report_dir=None):
        self.monitored_method = monitored_method

        self.report_dir = report_dir
        if not self.report_dir:
            self.report_dir = REPORT_DIR

    def report(self):

        content = []
        line = ['pos', 'call_count', 'call_ratio', 'run_count', 'not_run_count']
        content.append(line)

        for path in self.monitored_method.info.paths:
            line = [path.pos, path.call_count, path.call_ratio,
                    path.path_info.run_count, path.path_info.not_run_count]
            content.append(line)

        self.report_dir = full_dir(self.report_dir, __file__)
        ensure_dir(self.report_dir)

        pyfile = os.path.join(self.report_dir, self.monitored_method.info.full_name + '.csv')
        write_csv(pyfile, content)


class CSVIndexReport:

    def __init__(self, monitored_program, report_dir=None):
        self.monitored_program = monitored_program

        self.report_dir = report_dir
        if not self.report_dir:
            self.report_dir = REPORT_DIR

    def report(self):

        content = []
        line = ['full_name', "is_generator",
                'coverage_ratio', 'run_lines_count', 'executable_lines_count',
                'total_tests', 'total_calls', 'total_exceptions', 'total_paths',
                'top1_path_calls', 'top1_path_ratio', 'top1_path_run_lines', 'top1_path_run_lines_ratio',
                'top2_path_calls', 'top2_path_ratio', 'top2_path_run_lines', 'top2_path_run_lines_ratio']

        content.append(line)

        for monitored_method in self.monitored_program:

            line = [

                    monitored_method.info.full_name,
                    monitored_method.info.is_generator_func,

                    monitored_method.info.coverage_ratio,
                    monitored_method.info.run_lines_count,
                    monitored_method.info.executable_lines_count,

                    monitored_method.info.total_tests,
                    monitored_method.info.total_calls,
                    monitored_method.info.total_exceptions,
                    monitored_method.info.total_paths,

                    monitored_method.info.top1_path_calls,
                    monitored_method.info.top1_path_ratio,
                    monitored_method.info.top1_path_run_lines,
                    monitored_method.info.top1_path_run_lines_ratio,

                    monitored_method.info.top2_path_calls,
                    monitored_method.info.top2_path_ratio,
                    monitored_method.info.top2_path_run_lines,
                    monitored_method.info.top2_path_run_lines_ratio,

                    ]

            content.append(line)

        self.report_dir = full_dir(self.report_dir, __file__)
        ensure_dir(self.report_dir)

        index_file = os.path.join(self.report_dir, INDEX_FILE)
        write_csv(index_file, content)
