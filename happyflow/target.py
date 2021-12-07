from happyflow.utils import line_intersection, get_code_lines, get_html_lines, find_executable_linenos, \
    build_from_func_or_method, escape, read_file_lines


class TargetMethod:

    _executable_lines = {}
    _code_lines = {}

    def __init__(self, module_name, class_name, name, full_name, filename):
        self.module_name = module_name
        self.class_name = class_name
        self.name = name
        self.full_name = full_name
        self.filename = filename
        self.start_line = None
        self.end_line = None
        self.info = None

    def executable_lines(self):
        exec_lines = self.ensure_executable_lines_for_file()
        my_lines = range(self.start_line, self.end_line + 1)
        return line_intersection(exec_lines, my_lines)

    def ensure_executable_lines_for_file(self):
        if self.filename not in TargetMethod._executable_lines:
            TargetMethod._executable_lines[self.filename] = find_executable_linenos(self.filename)
        return TargetMethod._executable_lines[self.filename]

    def executable_lines_count(self):
        return len(self.executable_lines())

    def loc(self):
        return self.end_line - self.start_line

    def line_is_executable(self, lineno):
        return lineno in self.executable_lines()

    def line_is_entity_definition(self, lineno):
        return lineno == self.start_line

    def has_lineno(self, lineno):
        return lineno in range(self.start_line, self.end_line + 1)

    def get_code(self):
        return ''.join(self.get_code_lines())

    def get_code_lines(self):
        code_lines = self.ensure_code_lines_for_file()
        return get_code_lines(self, code_lines)

    def ensure_code_lines_for_file(self):
        if self.filename not in TargetMethod._code_lines:
            TargetMethod._code_lines[self.filename] = read_file_lines(self.filename)
        return TargetMethod._code_lines[self.filename]

    def get_html_lines(self):
        return get_html_lines(self.get_code())

    def get_code_line_at_lineno(self, n):
        return self.get_code_lines()[n-1]

    def get_html_line_at_lineno(self, n):
        return self.get_html_lines()[n-1]

    def summary(self):
        return f'{self.full_name} (lines: {self.start_line}-{self.end_line})'

    def full_name_escaped(self):
        return escape(self.full_name)

    def is_method(self):
        return self.class_name is not None

    def is_func(self):
        return not self.is_method()

    def __str__(self):
        return self.full_name

    def __iter__(self):
        return iter([self])

    @staticmethod
    def build(func_or_method):
        return build_from_func_or_method(func_or_method, TargetMethod)
