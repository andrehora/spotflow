"""pytest tests used by test_finder (not collected as tests: see the file name)."""

import functools

import pytest
from tests.unit.stub_sut import SimpleCall


def decorated(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def helper():
    SimpleCall().simple_if()


def test_function():
    SimpleCall().simple_if()


@decorated
def test_decorated():
    SimpleCall().simple_if()


@pytest.mark.parametrize('value', ['a/b', 'c.d'])
def test_parametrized(value):
    SimpleCall().simple_if()


def test_with_nested_function():
    def test_nested():
        SimpleCall().simple_if()
    test_nested()


def test_calls_helper():
    helper()


class TestClass:

    def test_method(self):
        SimpleCall().simple_if()
