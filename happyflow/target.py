from happyflow.utils import line_intersection, get_code_lines, get_html_lines, find_executable_linenos, build_from_func_or_method


class TargetEntity:
    _executable_lines = {}

    def __init__(self, name, full_name, filename):
        self.name = name
        self.full_name = full_name
        self.filename = filename
        self.start_line = None
        self.end_line = None

        self.info = None

    def executable_lines(self):
        exec_lines = self.ensure_executable_lines_for_file(self.filename)
        my_lines = range(self.start_line, self.end_line + 1)
        return line_intersection(exec_lines, my_lines)

    def ensure_executable_lines_for_file(self, filename):
        if self.filename not in TargetEntity._executable_lines:
            TargetEntity._executable_lines[filename] = find_executable_linenos(filename)
        return TargetEntity._executable_lines[filename]

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
        return get_code_lines(self)

    def get_html_lines(self):
        return get_html_lines(self.get_code())

    def summary(self):
        return f'{self.full_name()} (lines: {self.start_line}-{self.end_line})'

    def __str__(self):
        return self.full_name

    def __iter__(self):
        return iter([self])

    @staticmethod
    def build(func_or_method):
        try:
            return build_from_func_or_method(func_or_method, TargetFunction, TargetMethod)
        except Exception as e:
            print(e)
            return None


class TargetFunction(TargetEntity):

    def __init__(self, module_name, name, full_name, filename=''):
        super().__init__(name, full_name, filename)
        self.module_name = module_name


class TargetMethod(TargetEntity):

    def __init__(self, module_name, class_name, name, full_name, filename=''):
        super().__init__(name, full_name, filename)
        self.module_name = module_name
        self.class_name = class_name





