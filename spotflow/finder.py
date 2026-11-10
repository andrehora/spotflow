"""Find the tests that unittest and pytest run, from the frames being traced.

A frame is a test if it runs the function the test framework is running as a
test, whatever its name:

- unittest: the method of a TestCase named by TestCase._testMethodName.
  The id is the unittest id, module.Class.method.
- pytest: the function of the item that pytest_pyfunc_call is calling.
  The id is module.Class.name[params].

This finds camelCase names (testBasic), tests generated at runtime, decorated
tests, tests inherited by several TestCase classes (one id per class), and
parametrized pytest tests (one id per case). Helpers and nested functions are
not tests, even when their name starts with "test_".
"""

import unittest

# How many functions a decorated test can wrap (via __wrapped__)
_MAX_WRAPPED = 10

# How far a test frame can be from pytest's call, through decorator wrappers
_MAX_PYTEST_DEPTH = 10

# Code objects of the pytest test functions seen so far, so that only their
# frames look up the pytest item that runs them
_pytest_test_codes = set()


def find_test(frame):
    """(id, function) of a unittest or pytest test frame, or None."""
    # Runs inside the tracer, where any error would break the program under test
    try:
        return find_unittest_test(frame) or find_pytest_test(frame)
    except Exception:
        return None


def find_test_id(frame):
    """The id of a test frame, or None. See find_test."""
    test = find_test(frame)
    return test[0] if test else None


def get_test_method(test_case):
    """The function unittest runs for this TestCase (None while it is being created)."""
    method_name = getattr(test_case, "_testMethodName", None)
    if method_name is None:
        return None
    method = getattr(type(test_case), method_name, None)
    return getattr(method, "__func__", method)


def get_test_codes(func):
    """Code objects of a test function and of the functions it decorates (via __wrapped__)."""
    codes = []
    while func is not None and len(codes) < _MAX_WRAPPED:
        code = getattr(func, "__code__", None)
        if code is not None:
            codes.append(code)
        func = getattr(func, "__wrapped__", None)
    return codes


def find_unittest_test(frame):
    code = frame.f_code
    if not code.co_varnames or code.co_varnames[0] != "self":
        return None
    test_case = frame.f_locals.get("self")
    if not isinstance(test_case, unittest.TestCase):
        return None
    func = get_test_method(test_case)
    if code not in get_test_codes(func):
        return None
    return test_case.id(), func


def get_pytest_item(frame):
    """The pytest item if this frame is pytest calling a test function, or None.

    pytest calls each test function from its pytest_pyfunc_call hook (plugins
    such as pytest-asyncio implement the same hook, with the same argument).
    """
    code = frame.f_code
    if code.co_name != "pytest_pyfunc_call" or "pyfuncitem" not in code.co_varnames:
        return None
    return frame.f_locals.get("pyfuncitem")


def find_pytest_test(frame):
    item = get_pytest_item(frame)
    if item is not None:
        # Seen before the test function is called: remember its code objects
        _pytest_test_codes.update(get_test_codes(item.obj))
        return None

    code = frame.f_code
    if code not in _pytest_test_codes:
        return None
    outer = frame.f_back
    for _ in range(_MAX_PYTEST_DEPTH):
        if outer is None:
            return None
        item = get_pytest_item(outer)
        if item is not None:
            if code not in get_test_codes(item.obj):
                return None
            func = getattr(item.obj, "__func__", item.obj)
            return get_pytest_test_id(item), func
        outer = outer.f_back
    return None


def get_pytest_test_id(item):
    names = [item.module.__name__]
    if item.cls is not None:
        names.append(item.cls.__qualname__)
    names.append(item.name)
    return ".".join(names)
