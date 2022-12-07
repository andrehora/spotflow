from spotflow.utils import line_intersection, get_html_lines, find_executable_linenos, get_metadata, escape, ratio

executable_lines_for_file = {}


class MethodInfo:

    def __init__(self, module_name, class_name, name, full_name, filename, code=''):
        self.module_name = module_name
        self.class_name = class_name
        self.name = name
        self.full_name = full_name
        self.filename = filename
        self.code = code

        self.start_line = None
        self.end_line = None
        self.info = None

        self.code_lines = None
        self.html_lines = None

        # Updated in collector
        self.return_lines = set()
        self.yield_lines = set()
        self.exception_lines = set()
        self.control_flow_lines = set()
        self.other_lines = set()

    def is_method(self):
        return self.class_name is not None

    def is_func(self):
        return not self.is_method()

    def loc(self):
        return self.end_line - self.start_line

    def has_return(self):
        return len(self.return_lines) > 0

    def has_yield(self):
        return len(self.yield_lines) > 0

    def has_exception(self):
        return len(self.exception_lines) > 0

    def executable_lines(self):
        exec_lines = self._ensure_executable_lines_for_file()
        my_lines = range(self.start_line, self.end_line + 1)
        return line_intersection(exec_lines, my_lines)

    def get_code_lines(self):
        if not self.code_lines:
            self.code_lines = self.code.splitlines()
        return self.code_lines

    def get_html_lines(self):
        if not self.html_lines:
            self.html_lines = get_html_lines(self.code)
        return self.html_lines

    def get_code_line_at_lineno(self, n):
        return self.get_code_lines()[n-1]

    def get_html_line_at_lineno(self, n):
        return self.get_html_lines()[n-1]

    def full_name_escaped(self):
        return escape(self.full_name)

    def summary(self):
        return f'{self.full_name} (lines: {self.start_line}-{self.end_line})'

    def _has_lineno(self, lineno):
        return lineno in range(self.start_line, self.end_line + 1)

    def _ensure_executable_lines_for_file(self):
        if self.filename not in executable_lines_for_file:
            executable_lines_for_file[self.filename] = find_executable_linenos(self.filename)
        return executable_lines_for_file[self.filename]

    def _line_is_executable(self, lineno):
        return lineno in self.executable_lines()

    def _executable_lines_without_def(self, monitored_method):
        exec_lines = self.executable_lines()
        first_run_line = monitored_method._get_first_run_line()
        first_run_line_index = exec_lines.index(first_run_line)
        return exec_lines[first_run_line_index:]

    def _update_call_info(self, monitored_method):
        self.run_lines_count = len(monitored_method.run_lines)
        # self.executable_lines_count = len(self._executable_lines_without_def(monitored_method))
        self.executable_lines_count = len(self.executable_lines()) - 1
        self.coverage_ratio = ratio(self.run_lines_count, self.executable_lines_count)

        self.total_calls = len(monitored_method.calls)
        self.total_tests = len(monitored_method.tests())
        self.total_exceptions = len(monitored_method.exception_states())

        # self.total_flows = len(monitored_method.flows)
        # self.top_flow_calls = monitored_method.flows[0].info.call_count
        # self.top_flow_ratio = monitored_method.flows[0].info.call_ratio

    def __str__(self):
        return self.full_name

    def __iter__(self):
        return iter([self])

    @staticmethod
    def build(func_or_method):
        try:
            module_name, class_name, name, filename, start_line, end_line, full_name, code = get_metadata(func_or_method)
            method_info = MethodInfo(module_name, class_name, name, full_name, filename, code)
            method_info.start_line = start_line
            method_info.end_line = end_line
            return method_info
        except Exception:
            return None
