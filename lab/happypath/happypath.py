from spotflow.model import CallContainer
from spotflow.info import Analysis, PathInfo
from spotflow.utils import ratio
from lab.happypath import report


def spotflow_post(monitored_program, *args):

    compute_paths(monitored_program)

    output_dir = args[0]
    rep = report.Report(monitored_program)
    # rep.html_report(output_dir)
    rep.csv_report(output_dir)


def compute_paths(monitored_program):

    for monitored_method in monitored_program.all_methods():
        paths = compute_paths_for_method(monitored_method)

        monitored_method.info.paths = paths
        monitored_method.info.total_paths = len(paths)

        monitored_method.info.top1_path_calls = paths[0].call_count
        monitored_method.info.top1_path_ratio = paths[0].call_ratio
        monitored_method.info.top1_path_run_lines = len(paths[0].distinct_run_lines)
        monitored_method.info.top1_path_run_lines_ratio = paths[0].run_lines_ratio

        monitored_method.info.top2_path_calls = -1
        monitored_method.info.top2_path_ratio = -1
        monitored_method.info.top2_path_run_lines = -1
        monitored_method.info.top2_path_run_lines_ratio = -1

        if len(paths) >= 2:
            monitored_method.info.top2_path_calls = paths[1].call_count
            monitored_method.info.top2_path_ratio = paths[1].call_ratio
            monitored_method.info.top2_path_run_lines = len(paths[1].distinct_run_lines)
            monitored_method.info.top2_path_run_lines_ratio = paths[1].run_lines_ratio


def compute_paths_for_method(monitored_method):

    most_common_run_lines = Analysis(monitored_method).most_common_run_lines()
    path_pos = 0
    paths = []
    for run_lines in most_common_run_lines:
        path_pos += 1
        distinct_run_lines = run_lines[0]

        equivalent_calls = select_equivalent_calls(monitored_method, distinct_run_lines)
        path = MethodPath(path_pos, distinct_run_lines, equivalent_calls, monitored_method)
        paths.append(path)

    return paths


def select_equivalent_calls(monitored_method, distinct_lines):
    calls = []
    for call in monitored_method.calls:
        if tuple(call.distinct_run_lines()) == tuple(distinct_lines):
            calls.append(call)
    return calls


class MethodPath(CallContainer):

    def __init__(self, pos, distinct_run_lines, calls, monitored_method):
        super().__init__(calls)
        self.pos = pos
        self.distinct_run_lines = distinct_run_lines
        self.monitored_method = monitored_method
        self.path_info = PathInfo(self.monitored_method, self.calls[0])

        self.call_count = len(self.calls)

        total_calls = len(self.monitored_method.calls)
        self.call_ratio = ratio(self.call_count, total_calls)

        run_lines_count = len(self.distinct_run_lines)
        executable_lines_count = self.monitored_method.info.executable_lines_count
        self.run_lines_ratio = ratio(run_lines_count, executable_lines_count)

        self.arg_values = Analysis(self).most_common_args_pretty()
        self.return_values = Analysis(self).most_common_return_values_pretty()
        self.yield_values = Analysis(self).most_common_yield_values_pretty()
        self.exception_values = Analysis(self).most_common_exception_values_pretty()
