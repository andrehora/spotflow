"""unittest tests used by test_finder (not collected as tests: see the file name)."""

import functools
import unittest
from tests.unit.stub_sut import SimpleCall


def decorated(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def generated():
    def helper(self):
        pass
    return helper


class Base(unittest.TestCase):

    def test_inherited(self):
        SimpleCall().simple_if()


class Sample(Base):

    def test_snake_case(self):
        SimpleCall().simple_if()

    def testCamelCase(self):
        SimpleCall().simple_if()

    @decorated
    def test_decorated(self):
        SimpleCall().simple_if()

    test_generated = generated()

    def test_with_nested_function(self):
        def test_nested():
            SimpleCall().simple_if()
        test_nested()

    def test_with_lambda(self):
        # A frame SpotFlow cannot name
        (lambda: SimpleCall().simple_if())()

    def helper_method(self):
        SimpleCall().simple_if()

    def test_calls_helper(self):
        self.helper_method()

    def test_no_sut_call(self):
        pass
