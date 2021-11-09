import trace
import types
from happyflow.utils import find_func_or_method_from_frame
from happyflow.utils import line_intersection, get_code_lines, get_html_lines
from happyflow.utils import function_metadata, method_metadata


class TargetBaseEntity:

    def __init__(self, name, full_name, filename):
        self.name = name
        self.full_name = full_name
        self.filename = filename

    def __str__(self):
        return self.full_name

    def is_target(self):
        return False

    def loc(self):
        pass

    def executable_lines(self):
        pass


class TargetEntity(TargetBaseEntity):
    start_line = 0
    end_line = 0

    def __iter__(self):
        return iter([self])

    def is_target(self):
        return True

    def executable_lines(self):
        executable_lines = trace._find_executable_linenos(self.filename)
        # remove the target_entity definition, eg, def, class
        return tuple(self.intersection(executable_lines)[1:])

    def intersection(self, other_lines):
        my_lines = range(self.start_line, self.end_line + 1)
        return line_intersection(my_lines, other_lines)

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

    @staticmethod
    def build_from_func(func_or_method):

        target_entity = None

        if isinstance(func_or_method, types.MethodType):
            module_name, class_name, name, filename, start_line, end_line, full_name = method_metadata(func_or_method)
            target_entity = TargetMethod(module_name, class_name, name, full_name, filename)

        if isinstance(func_or_method, types.FunctionType):
            module_name, name, filename, start_line, end_line, full_name = function_metadata(func_or_method)
            target_entity = TargetFunction(module_name, name, full_name, filename)

        target_entity.start_line = start_line
        target_entity.end_line = end_line

        return target_entity

    @staticmethod
    def build_from_frame(frame):
        func_or_method = find_func_or_method_from_frame(frame)
        if func_or_method:
            return TargetEntity.build_from_func(func_or_method)
        return None


class TargetMethod(TargetEntity):

    def __init__(self, module_name, class_name, name, full_name, filename=''):
        super().__init__(name, full_name, filename)
        self.module_name = module_name
        self.class_name = class_name


class TargetFunction(TargetEntity):

    def __init__(self, module_name, name, full_name, filename=''):
        super().__init__(name, full_name, filename)
        self.module_name = module_name




