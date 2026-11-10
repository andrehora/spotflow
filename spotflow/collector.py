import ast
import dis
import functools
import inspect
import itertools
import linecache
import sys
from spotflow.utils import obj_value, obj_type, get_full_name, is_method_or_func, get_module_names, find_start_end_lines, get_code_filename
from spotflow.model import CallState, MonitoredMethod, MonitoredProgram
from spotflow.info import MethodInfo
from spotflow.finder import find_test, find_test_id
from spotflow.tracer import PyTracer


def get_frame_id(frame):

    # If we are dealing with comprehensions and generator expressions
    # then we should get the enclosing frame id, not the current one.
    # This is done to avoid novel flows being created to listcomp and genexpr...
    if is_compr_or_genexpr(frame):
        return get_frame_id(frame.f_back)
    return frame_id(frame)

def frame_id(frame):
    return id(frame)


def is_compr_or_genexpr(frame):
    return frame.f_code.co_name in ["<listcomp>", "<setcomp>", "<dictcomp>", "<genexpr>"]


_RESUME = dis.opmap["RESUME"]


def is_frame_start(frame):
    # Whether a "call" event is the start of a function call (True) or a
    # generator/coroutine being re-entered (False). On a "call" event, the
    # frame is at a RESUME instruction: the low two bits of its oparg are 0
    # at the start of the function, and 1, 2 or 3 after a yield, yield from
    # or await. Higher bits are flags.
    code = frame.f_code.co_code
    lasti = frame.f_lasti
    return code[lasti] == _RESUME and code[lasti + 1] & 3 == 0


def get_next_mro_class(current_class):
    mro_classes = current_class.__mro__
    current_class_index = mro_classes.index(current_class)
    return mro_classes[current_class_index + 1]


def has_superclass(current_class):
    # Why 3? At least: current_class, superclass, and object
    return len(current_class.__mro__) >= 3


def resolve_method_for_frame(current_class, frame):
    
    current_method_name = frame.f_code.co_name
    lineno = frame.f_lineno
    method = inspect.getattr_static(current_class, current_method_name, None)
    start_line, end_line = find_start_end_lines(method)
    # Check if it getting the correct method
    if lineno in range(start_line, end_line+1):
        return method
    # If not, try the next super class
    next_class = get_next_mro_class(current_class)
    return resolve_method_for_frame(next_class, frame)


_RETURN_VALUE = dis.opmap["RETURN_VALUE"]
_YIELD_VALUE = dis.opmap["YIELD_VALUE"]
_CO_AWAITS = inspect.CO_COROUTINE | inspect.CO_ASYNC_GENERATOR

RETURN = "return"
YIELD = "yield"
_RETURN_NOT_NONE = "return, if the value is not None"

# What a frame does at an instruction: (id(code), offset) -> (code, kind).
# The kind is RETURN, YIELD, _RETURN_NOT_NONE or None. The key has the id of
# the code, since the hash of a code is slow (see Collector.frame_cache).
_exit_kinds = {}

# filename -> SourceInfo
_source_infos = {}


def get_exit_kind(frame, arg):
    # What a "return" event is: a return (RETURN), a yield (YIELD) or neither
    # (None). The event also happens when a coroutine is suspended in an await,
    # when an exception leaves the frame and, without a return statement, at
    # the end of the function. This is found from the instruction the frame is
    # at, and not from the text of the line: a line can start with "return" and
    # raise an exception, and a return or yield can be anywhere in a line.
    #
    # The events of a generator expression are monitored as events of the
    # method it is in (see get_frame_id). The values it yields are not yielded
    # or returned by the method.
    if is_compr_or_genexpr(frame):
        return None

    code = frame.f_code
    key = id(code), frame.f_lasti
    cached = _exit_kinds.get(key)
    if cached is None:
        cached = _exit_kinds[key] = code, find_exit_kind(frame)
    kind = cached[1]
    if kind == _RETURN_NOT_NONE:
        return RETURN if arg is not None else None
    return kind


def find_exit_kind(frame):

    code = frame.f_code
    lasti = frame.f_lasti
    opcode = code.co_code[lasti]

    if opcode == _YIELD_VALUE:
        # The oparg is 1 in a yield from or await, and 0 in a yield. Coroutines
        # and async generators have no yield from: it is an await.
        if code.co_code[lasti + 1] and code.co_flags & _CO_AWAITS:
            return None
        return YIELD

    if opcode != _RETURN_VALUE:
        # An exception is leaving the frame
        return None

    # The end of a function without a return statement also returns (None).
    # A lambda has no return statement: its body is what it returns.
    if code.co_name == "<lambda>" or is_in_return_statement(frame):
        return RETURN

    # The instruction may still be of a return statement, when it runs after
    # the code that leaves a with or try block. It is, if it returns a value.
    return _RETURN_NOT_NONE


def is_in_return_statement(frame):

    code = frame.f_code
    position = next(itertools.islice(code.co_positions(), frame.f_lasti // 2, None), None)
    if position is None or None in position:
        return False
    lineno, end_lineno, col_offset, end_col_offset = position
    start = lineno, col_offset
    end = end_lineno, end_col_offset
    for return_start, return_end in get_return_statements(frame):
        if return_start <= start and end <= return_end:
            return True
    return False


def get_return_statements(frame):
    return get_source_info(frame).return_statements


def line_has_control_flow(frame):
    return frame.f_lineno in get_source_info(frame).control_flow_lines


class SourceInfo:
    """What the collector needs from the source code of a file, found once from its AST."""

    def __init__(self, source):

        # Positions of the return statements: [(start, end)]
        self.return_statements = []

        # Lines of the headers of the if, elif, while and for statements. The
        # header is the condition of an if or while, and the iterable of a for.
        # The text of a line is not enough to find them: the line
        # "formatted = 1" starts with "for".
        self.control_flow_lines = set()

        try:
            tree = ast.parse(source)
        except (SyntaxError, ValueError):
            return

        for node in ast.walk(tree):
            if isinstance(node, ast.Return):
                start = node.lineno, node.col_offset
                end = node.end_lineno, node.end_col_offset
                self.return_statements.append((start, end))
            elif isinstance(node, (ast.If, ast.While)):
                self.control_flow_lines.update(range(node.lineno, node.test.end_lineno + 1))
            elif isinstance(node, (ast.For, ast.AsyncFor)):
                self.control_flow_lines.update(range(node.lineno, node.iter.end_lineno + 1))


def get_source_info(frame):

    filename = get_code_filename(frame.f_code, frame.f_globals)
    if filename not in _source_infos:
        source = "".join(linecache.getlines(filename, frame.f_globals))
        _source_infos[filename] = SourceInfo(source)
    return _source_infos[filename]


# Names of the arguments of a code: id(code) -> (code, inspect.Arguments)
_code_args = {}


def get_arg_values(frame):
    # As inspect.getargvalues, but the names of the arguments are found once
    # for each code, and not in every call
    code = frame.f_code
    cached = _code_args.get(id(code))
    if cached is None:
        cached = _code_args[id(code)] = code, inspect.getargs(code)
    args, varargs, varkw = cached[1]
    return inspect.ArgInfo(args, varargs, varkw, frame.f_locals)


def update_method_info(method_info, frame, event, arg):

    # A line can be of several kinds: the line of a return statement is first
    # seen in a "line" event, and it can also raise an exception.
    lineno = frame.f_lineno

    if event == "line":
        if lineno in method_info.other_lines or lineno in method_info.control_flow_lines:
            return
        if line_has_control_flow(frame):
            method_info.control_flow_lines.add(lineno)
        else:
            method_info.other_lines.add(lineno)

    elif event == "return":
        exit_kind = get_exit_kind(frame, arg)
        if exit_kind == RETURN:
            method_info.return_lines.add(lineno)
        elif exit_kind == YIELD:
            method_info.yield_lines.add(lineno)

    elif event == "exception":
        method_info.exception_lines.add(lineno)


def find_local_func(entity_name, local_elements):

    # 1st: check the locals
    if entity_name in local_elements:
        func = local_elements[entity_name]
        if inspect.isfunction(func) and entity_name == func.__name__:
            if "<locals>" in func.__qualname__:
                return func

    # 2nd: check the local values
    for func in local_elements.values():
        if inspect.isfunction(func) and entity_name == func.__name__:
            if "<locals>" in func.__qualname__:
                return func

    # 3rd: check the self, if any
    if "self" in local_elements:
        # Static lookup: must not run properties or other descriptors
        # of the monitored program
        obj = local_elements["self"]
        member = inspect.getattr_static(obj, entity_name, None)
        func = None
        if isinstance(member, staticmethod):
            func = member.__func__
        elif entity_name in getattr(obj, "__dict__", {}):
            func = member
        if inspect.isfunction(func) and "<locals>" in func.__qualname__:
            return func
    return None


def function_with_code(member, code):

    # The function that runs the code, from a class member: the function itself
    # or the one wrapped by a classmethod, staticmethod, property (getter,
    # setter or deleter) or cached_property.
    if isinstance(member, (classmethod, staticmethod)):
        candidates = [member.__func__]
    elif isinstance(member, property):
        candidates = [member.fget, member.fset, member.fdel]
    elif isinstance(member, functools.cached_property):
        candidates = [member.func]
    else:
        candidates = [member]
    for func in candidates:
        if inspect.isfunction(func) and func.__code__ is code:
            return func
    return None


def find_func_by_qualname(frame):

    # Follow the qualified name of the code from the module globals, e.g.,
    # "Class.method". This finds the functions that cannot be found from the
    # frame locals: static methods (no self or cls), class methods and
    # properties (not functions in the class). Static lookup: must not run
    # descriptors of the monitored program.
    code = frame.f_code
    names = code.co_qualname.split(".")
    if "<locals>" in names:
        return None
    member = frame.f_globals.get(names[0])
    for name in names[1:]:
        if member is None:
            return None
        member = inspect.getattr_static(member, name, None)
    return function_with_code(member, code)


def get_method_object(frame):

    try:
        method_name = frame.f_code.co_name

        func = find_func_by_qualname(frame)
        if func:
            return func

        # Method
        if "self" in frame.f_locals:

            # The most common case: simply get self class
            obj_class = frame.f_locals["self"].__class__

            method = inspect.getattr_static(obj_class, method_name, None)
            if has_superclass(obj_class):
                method = resolve_method_for_frame(obj_class, frame)

            return method
        
        if "cls" in frame.f_locals:
            obj_class = frame.f_locals["cls"]
            method = inspect.getattr_static(obj_class, method_name, None)
            return method

        # Function
        if method_name in frame.f_globals:
            func = frame.f_globals[method_name]
            return func

        # Local function
        local_func = find_local_func(method_name, frame.f_back.f_locals)
        if local_func:
            return local_func

        local_func = find_local_func(method_name, frame.f_locals)
        if local_func:
            return local_func

    except Exception as e:
        return None


def is_never_method(code):

    # Module code is never found by get_method_object: nothing is named
    # "<module>". This is known from the code, with no need to look for it
    # every time it is in a call stack.
    #
    # The other frames that are not found are looked for again each time,
    # since the result depends on more than their code:
    # - lambdas and local functions are found from the locals of the caller,
    #   so one can be found when called from one place and not from another;
    # - generator expressions are found from the method they are in (see
    #   Collector.find_enclosing_method_obj), after it is found.
    return code.co_name == "<module>"


def is_valid_method_name(frame, current_method_name):
        
    if is_compr_or_genexpr(frame):
        return True

    method_name_from_frame = frame.f_code.co_name
    method_name_from_current = current_method_name.split('.')[-1]
    return method_name_from_frame == method_name_from_current


def target_matches(target, method_full_name):

    # A target is a function or method, which matches its own full name, or a
    # name: of a method (module.Class.method), or of a class, module or package,
    # to match all the methods in it. A name only matches whole names: the
    # target "module.parse" does not match "module.parse_all".
    if is_method_or_func(target):
        return get_full_name(target) == method_full_name
    return method_full_name == target or method_full_name.startswith(target + ".")


# Whether the frames of a code can be monitored (see Collector.get_code_validity)
VALID = "valid"
INVALID = "invalid"
VALID_BY_CALLER = "valid by caller"


class Collector:

    def __init__(self):

        self.monitored_program = MonitoredProgram()
        self.target_method_full_names = None
        self.target_method_short_names = None
        self.file_names = None
        self.ignore_files = None
        self.module_names = None

        self.collect_arg_states = True
        self.collect_return_states = True
        self.collect_yield_states = True
        self.collect_exception_states = True

        self.target_methods_cache = {}
        self.matched_targets = {}
        # id(code) -> (code, method or function, its full name). The key is not the code:
        # the hash of a code is computed from its contents each time, which
        # is slow in every event. The code is kept in the value so that it
        # stays alive, and its id is not reused by another code.
        self.frame_cache = {}

        # Codes of the frames that were found to be tests: id(code) -> code
        self.test_codes = {}

        # Codes that are monitored (see monitor_event):
        # id(code) -> (code, method full name, method info, depends on caller)
        self.monitored_codes = {}

        # Codes that are never monitored: id(code) -> code
        self.ignored_codes = {}

        self.py_tracer = PyTracer(self)

    def start(self):
        self.init_target()
        self.init_test_codes()
        self.py_tracer.start_tracer()

    def stop(self):
        self.py_tracer.stop_tracer()
        self.monitored_program._update_info()

    def init_target(self):
        # The targets and files may have changed since the last start
        self.monitored_codes = {}
        self.ignored_codes = {}
        self.matched_targets = {}
        if self.target_method_full_names and not self.target_method_short_names:
            self.module_names = get_module_names(self.target_method_full_names)

    def init_test_codes(self):

        # The tests that are already running have no "call" event to be found
        # from. The frames are checked from the outermost one, as in the order
        # of their calls: pytest is seen before the test it is running.
        frames = []
        frame = sys._getframe()
        while frame is not None:
            frames.append(frame)
            frame = frame.f_back
        for frame in reversed(frames):
            if find_test(frame) is not None:
                self.test_codes[id(frame.f_code)] = frame.f_code

    def monitor_event(self, frame, event, arg):

        # Returns whether the frame is of a monitored method. If it is not, in
        # a "call" event, the tracer does not trace the other events of the frame.

        # Tests are found in any frame, since test code is usually not a target
        if event == "call":
            self.record_test(frame)

        # This runs in every event. Whether a code is monitored is found once
        # (see monitor_new_code): after that, it takes one lookup.
        code_id = id(frame.f_code)
        monitored = self.monitored_codes.get(code_id)
        if monitored is not None:
            _, current_method_name, method_info, depends_on_caller = monitored
            if depends_on_caller and not self.is_valid_caller(frame):
                return False
            self.monitor_method_event(method_info, frame, event, arg, current_method_name)
            return True

        if code_id in self.ignored_codes:
            return False

        return self.monitor_new_code(frame, event, arg)

    def monitor_new_code(self, frame, event, arg):

        # Finds whether the frame is of a monitored method and, if so, monitors
        # the event. The answer is kept when it is the same for all the frames
        # of the code. It is not when:
        # - the method is not found: it may be found in another frame (see
        #   is_never_method);
        # - the frame is of a generator expression: its method is the one of
        #   the frame that runs it;
        # - the frame is only valid because of its caller (see is_valid_caller).
        code = frame.f_code
        same_for_code = not is_compr_or_genexpr(frame)

        validity = self.get_code_validity(frame)
        if validity == INVALID:
            self.ignored_codes[id(code)] = code
            return False
        depends_on_caller = validity == VALID_BY_CALLER
        if depends_on_caller and not self.is_valid_caller(frame):
            return False

        current_method_name = self.get_method_full_name(frame)
        if not current_method_name:
            return False

        target_method = None
        is_target = is_valid_method_name(frame, current_method_name)
        if is_target and not self.target_method_short_names:
            if self.target_method_full_names:
                # An event is monitored once, even when several targets match it
                target_method = self.find_target(current_method_name)
                is_target = target_method is not None
            else:
                # Without targets, all the methods are monitored
                is_target = self.target_method_full_names is None and self.target_method_short_names is None
        if not is_target:
            if same_for_code:
                self.ignored_codes[id(code)] = code
            return False

        method_info = self.ensure_method_info(frame, current_method_name, target_method)
        if not method_info or current_method_name != method_info.full_name:
            return False

        if same_for_code:
            self.monitored_codes[id(code)] = code, current_method_name, method_info, depends_on_caller

        self.monitor_method_event(method_info, frame, event, arg, current_method_name)
        return True

    def find_target(self, current_method_name):

        # The first target that matches the method, or None
        if current_method_name not in self.matched_targets:
            target_method = None
            for target in self.target_method_full_names:
                if target_matches(target, current_method_name):
                    target_method = target
                    break
            self.matched_targets[current_method_name] = target_method
        return self.matched_targets[current_method_name]

    def monitor_method_event(self, method_info, frame, event, arg, current_method_name):

        update_method_info(method_info, frame, event, arg)

        # The call event is really a "start frame" event, and happens for
        # function calls and re-entering generators (see is_frame_start).
        if (event == "call" and is_frame_start(frame) and not is_compr_or_genexpr(frame)):

            monitored_methods = self.monitored_program.monitored_methods
            monitored_method = monitored_methods.get(current_method_name)
            if monitored_method is None:
                monitored_method = monitored_methods[current_method_name] = MonitoredMethod(method_info)

            call_state = CallState()
            callers = self.find_call_stack(frame)

            if self.collect_arg_states:
                call_state._save_arg_states(get_arg_values(frame), frame.f_lineno)

            frame_id = get_frame_id(frame)
            tests = self.monitored_program.tests
            call_tests = tuple(name for name in callers[:-1] if name in tests)
            monitored_method.add_call(call_state, callers, frame_id, call_tests)

        # Event is line, return, exception or call for re-entering generators
        else:

            lineno = frame.f_lineno
            monitored_method = self.monitored_program.monitored_methods.get(current_method_name)
            if monitored_method is not None:

                if not monitored_method.calls:
                    return

                frame_id = get_frame_id(frame)
                method_call = monitored_method._get_call_from_id(frame_id)
                if not method_call:
                    return

                current_call_state = method_call.call_state
                if event == "line":
                    method_call._add_run_line(lineno)
                    monitored_method._add_run_line(lineno)

                elif event == "return":
                    exit_kind = get_exit_kind(frame, arg)
                    if exit_kind == RETURN:
                        if self.collect_return_states:
                            current_call_state._save_return_state(obj_value(arg), obj_type(arg), lineno)
                    elif exit_kind == YIELD:
                        if self.collect_yield_states:
                            current_call_state._save_yield_state(obj_value(arg), obj_type(arg), lineno)

                elif event == "exception":
                    if self.collect_exception_states:
                        exception_name = arg[0].__name__
                        exception_type = obj_type(arg[0])
                        current_call_state._save_exception_state(exception_name, exception_type, lineno)

    def is_valid_frame(self, frame):

        validity = self.get_code_validity(frame)
        if validity == VALID_BY_CALLER:
            return self.is_valid_caller(frame)
        return validity == VALID

    def get_code_validity(self, frame):

        # Whether the frames of a code can be monitored, from the files and
        # the short names of the targets: VALID, INVALID or VALID_BY_CALLER
        # (not by itself, but each frame is valid if its caller is in a
        # target file).
        current_filename = get_code_filename(frame.f_code, frame.f_globals)
        current_method_name = frame.f_code.co_name

        if current_filename.startswith("<") or current_method_name == "<module>":
            return INVALID

        if self.target_method_short_names:
            for target_method_name in self.target_method_short_names:
                if target_method_name == current_method_name:
                    return VALID
            return INVALID

        if self.ignore_files:
            for ignore in self.ignore_files:
                if ignore in current_filename:
                    return INVALID

        if self.file_names:
            for filename in self.file_names:
                if filename in current_filename:
                    return VALID
            return VALID_BY_CALLER

        if self.module_names:
            for module_name in self.module_names:
                if module_name in current_filename:
                    return VALID
            return INVALID

        return VALID

    def is_valid_caller(self, frame):

        # With target files, the methods of other files are also monitored
        # when they are called from a target file
        back = frame.f_back
        if back is None:
            return False
        back_filename = get_code_filename(back.f_code, back.f_globals)
        for filename in self.file_names:
            if filename in back_filename:
                return True
        return False

    def get_method_full_name(self, frame):

        cached = self.frame_cache.get(id(frame.f_code))
        if cached is not None:
            return cached[2]

        method_obj = self.ensure_method_obj(frame)
        if method_obj:
            return get_full_name(method_obj)

        return None

    def ensure_method_obj(self, frame):

        if is_never_method(frame.f_code):
            return None

        if is_compr_or_genexpr(frame):
            return self.find_enclosing_method_obj(frame)

        # The method is the same for all the frames and lines of a code
        code = frame.f_code
        cached = self.frame_cache.get(id(code))
        if cached is not None:
            return cached[1]

        method_obj = get_method_object(frame)
        if (not method_obj or inspect.isbuiltin(method_obj) or not is_method_or_func(method_obj)):
            return None

        self.frame_cache[id(code)] = code, method_obj, get_full_name(method_obj)
        return method_obj

    def find_enclosing_method_obj(self, frame):

        # The events of a generator expression are monitored as events of the
        # method it is in. This is the method of the frame that is running the
        # generator expression, if it is also the one that has its code (a
        # generator expression can be run by other functions, e.g., when it is
        # returned).
        back = frame.f_back
        if back is None or frame.f_code not in back.f_code.co_consts:
            return None
        cached = self.frame_cache.get(id(back.f_code))
        return cached[1] if cached is not None else None

    def ensure_method_info(self, frame, current_entity_name, target_method):

        # Handle the special case in which 'target_method' is already method/function object
        if is_method_or_func(target_method):
            # Each target only matches its own frames. Otherwise, with several
            # targets, the info of one would be cached under the name of another.
            if not target_matches(target_method, current_entity_name):
                return None
            if current_entity_name in self.target_methods_cache:
                return self.target_methods_cache[current_entity_name]
            method_info = MethodInfo.build(target_method)
            self.target_methods_cache[current_entity_name] = method_info
            return method_info

        # Handle the other cases...
        if target_method and not target_matches(target_method, current_entity_name):
            return None

        if current_entity_name in self.target_methods_cache:
            return self.target_methods_cache[current_entity_name]

        method_obj = self.ensure_method_obj(frame)
        if not method_obj:
            return None
        method_info = MethodInfo.build(method_obj)
        if not method_info:
            return None

        self.target_methods_cache[current_entity_name] = method_info
        return method_info

    def record_test(self, frame):

        found = find_test(frame)
        if found is None:
            return
        self.test_codes[id(frame.f_code)] = frame.f_code
        test_id, func = found
        if test_id in self.monitored_program.tests:
            return
        test_info = MethodInfo.build(func)
        if test_info:
            self.monitored_program.tests[test_id] = test_info

    def find_call_stack(self, frame):

        # Test frames are named by their test id. Frames that cannot be named
        # (lambdas, comprehensions, module code) are skipped instead of ending
        # the stack, so that the test is still found above them.
        #
        # This runs for each monitored call and each frame above it, so it does
        # as little as possible per frame. Only the frames of a code that was
        # found to be a test are checked again, to get their test id: all the
        # frames had a "call" event, in which the tests are found (see
        # record_test), or were running at the start (see init_test_codes).
        frame_cache = self.frame_cache
        test_codes = self.test_codes
        call_stack = [frame.f_code.co_name]
        frame = frame.f_back
        while frame is not None:
            code_id = id(frame.f_code)
            name = None
            if code_id in test_codes:
                name = find_test_id(frame)
            if not name:
                cached = frame_cache.get(code_id)
                if cached is not None:
                    name = cached[2]
                else:
                    name = self.get_method_full_name(frame)
            if name:
                call_stack.append(name)
            frame = frame.f_back
        call_stack.reverse()
        return tuple(call_stack)
