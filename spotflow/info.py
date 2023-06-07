from spotflow.utils import (
    line_intersection,
    find_executable_linenos,
    get_metadata,
    escape
)
from collections import Counter

executable_lines_for_file = {}


class MethodInfo:
    def __init__(
        self,
        module_name,
        class_name,
        name,
        full_name,
        filename,
        is_generator_func=False,
        code="",
    ):
        self.module_name = module_name
        self.class_name = class_name
        self.name = name
        self.full_name = full_name
        self.filename = filename
        self.is_generator_func = is_generator_func
        self.code = code

        self.start_line = None
        self.end_line = None
        self.info = None

        self.code_lines = None
        self.html_lines = None # need to be set manually

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

    def get_code_line_at_lineno(self, n):
        return self.get_code_lines()[n - 1]

    def get_html_line_at_lineno(self, n):
        # need to be set manually
        return self.html_lines[n - 1]

    def full_name_escaped(self):
        return escape(self.full_name)

    def summary(self):
        return f"{self.full_name} (lines: {self.start_line}-{self.end_line})"

    def _has_lineno(self, lineno):
        return lineno in range(self.start_line, self.end_line + 1)

    def _ensure_executable_lines_for_file(self):
        if self.filename not in executable_lines_for_file:
            executable_lines_for_file[self.filename] = find_executable_linenos(
                self.filename
            )
        return executable_lines_for_file[self.filename]

    def _line_is_executable(self, lineno):
        return lineno in self.executable_lines()

    def _executable_lines_without_def(self, monitored_method):
        exec_lines = self.executable_lines()
        first_run_line = monitored_method._get_first_run_line()
        first_run_line_index = exec_lines.index(first_run_line)
        return exec_lines[first_run_line_index:]

    def _update_call_info(self, monitored_method):
        self.run_lines_count = len(monitored_method.distinct_run_lines())
        self.executable_lines_count = len(self.executable_lines()) - 1

        self.total_calls = len(monitored_method.calls)
        self.total_tests = len(monitored_method.tests())
        self.total_exceptions = len(monitored_method.exception_states())

    def __str__(self):
        return self.full_name

    def __iter__(self):
        return iter([self])

    @staticmethod
    def build(func_or_method):
        try:
            (
                module_name,
                class_name,
                name,
                filename,
                start_line,
                end_line,
                full_name,
                is_generator_func,
                code,
            ) = get_metadata(func_or_method)

            method_info = MethodInfo(
                module_name,
                class_name,
                name,
                full_name,
                filename,
                is_generator_func,
                code,
            )
            method_info.start_line = start_line
            method_info.end_line = end_line
            return method_info
        except Exception:
            return None


class PathInfo:
    def __init__(self, monitored_method, call):
        self.monitored_method = monitored_method
        self.call = call
        self.distinct_run_lines = self.call.distinct_run_lines()

        self.lines = []
        self.run_count = 0
        self.not_run_count = 0
        self.not_exec_count = 0

        self._found_first_run_line = False
        self.create_lines()

    def create_lines(self):
        lineno = 0

        for lineno_entity in range(
            self.monitored_method.info.start_line,
            self.monitored_method.info.end_line + 1,
        ):
            lineno += 1

            line_status = self.get_line_status(lineno_entity)
            line_type, line_state = self.get_line_state(lineno_entity)
            line_info = LineInfo(
                lineno,
                lineno_entity,
                line_status,
                line_type,
                line_state,
                self.monitored_method.info,
            )

            self.lines.append(line_info)
            self.update_run_status(line_info)

    def get_line_status(self, current_line):
        if current_line in self.distinct_run_lines:
            self._found_first_run_line = True
            return RunStatus.RUN

        # _find_executable_linenos of trace returns method/function definitions as executable lines (?).
        # We should flag those definitions as not executable lines (NOT_EXEC). Otherwise, the definitions would impact
        # on the paths, coverage, etc. The solution for now is flagging all first lines as not executable until we
        # find the first run line. This way, the definitions are flagged as not executable lines...
        if not self._found_first_run_line:
            return RunStatus.NOT_EXEC

        if current_line not in self.distinct_run_lines:
            if not self.monitored_method.info._line_is_executable(current_line):
                return RunStatus.NOT_EXEC

        return RunStatus.NOT_RUN

    def get_line_state(self, lineno):
        if self.monitored_method.info.start_line == lineno:
            return self.line_arg_state()

        if lineno in self.monitored_method.info.return_lines:
            return self.line_return_state()

        states = self.call.call_state._states_for_line(lineno)
        if states:
            return self.line_var_states(states)
        return "", ""

    def line_arg_state(self):
        arg_str = ""
        for arg in self.call.call_state.arg_states:
            if arg.name != "self":
                arg_str += str(arg)
        return LineType.ARG, arg_str

    def line_return_state(self):
        return_state = self.call.call_state.return_state
        return LineType.RETURN, str(return_state)

    def line_var_states(self, states):
        return LineType.VAR, states

    def update_run_status(self, line_info):
        if line_info.is_run():
            self.run_count += 1
        if line_info.is_not_run():
            self.not_run_count += 1
        if line_info.is_not_exec():
            self.not_exec_count += 1

    def __len__(self):
        return len(self.lines)

    def __getitem__(self, position):
        return self.lines[position]


class LineInfo:
    def __init__(self, lineno, lineno_entity, run_status, type, state, method_info):
        self.lineno = lineno
        self.lineno_entity = lineno_entity
        self.run_status = run_status
        self.type = type
        self.state = state
        self.method_info = method_info

    def code(self):
        return self.method_info.get_code_line_at_lineno(self.lineno)

    def html(self):
        return self.method_info.get_html_line_at_lineno(self.lineno)

    def is_run(self):
        return self.run_status == RunStatus.RUN

    def is_not_run(self):
        return self.run_status == RunStatus.NOT_RUN

    def is_not_exec(self):
        return self.run_status == RunStatus.NOT_EXEC

    def is_arg(self):
        return self.type == LineType.ARG

    def is_return(self):
        return self.type == LineType.RETURN

    def is_var(self):
        return self.type == LineType.VAR


class LineType:
    ARG = "arg"
    RETURN = "return"
    VAR = "var"


class RunStatus:
    NOT_RUN = 0
    RUN = 1
    NOT_EXEC = 2


class Analysis:
    def __init__(self, call_container):
        self.call_container = call_container

    def number_of_calls(self):
        return len(self.call_container.calls)

    def most_common_run_lines(self):
        lines = self.call_container.all_distinct_run_lines()
        return self.most_common(lines)

    def most_common_arg_values(self):
        args = self.call_container.arg_states()
        args_count = {}

        for arg in args:
            args_count[arg] = self.most_common(args[arg])

        return args_count

    def most_common_return_values(self):
        values = self.call_container.return_states()
        return self.most_common(values)

    def most_common_yield_values(self):
        values = self.call_container.yield_states()
        return self.most_common(values)

    def most_common_exception_values(self):
        values = self.call_container.exception_states()
        return self.most_common(values)

    def most_common_args_pretty(self):
        return self.pretty_args(self.most_common_arg_values())

    def most_common_return_values_pretty(self):
        return self.pretty_return_values(self.most_common_return_values())

    def most_common_yield_values_pretty(self):
        return self.pretty_return_values(self.most_common_yield_values())

    def most_common_exception_values_pretty(self):
        return self.pretty_return_values(self.most_common_exception_values())

    def most_common(self, elements, n=10):
        try:
            return Counter(elements).most_common(n)
        except TypeError:
            return []

    def pretty_args(self, args, max_len=150):
        result = []
        for arg_name in args:
            arg_value = {}
            arg_value["name"] = arg_name
            values = ""
            for value in args[arg_name]:
                value_str = value[0]
                count = value[1]
                values += f"{value_str} ({count}) "
            arg_value["value"] = self.clear_values(values, max_len)
            result.append(arg_value)
        return result

    def pretty_return_values(self, return_values, max_len=150):
        values = ""
        for value in return_values:
            values += f"{value[0]} ({value[1]}) "
        if values:
            return self.clear_values(values, max_len)
        return None

    def clear_values(self, values, max_len):
        # values = values.rstrip(', ')
        if len(values) >= max_len:
            values = f"{values[0:max_len]}..."
        return values
