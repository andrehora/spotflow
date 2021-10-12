import unittest
import pytest


class PytestLoader:

    def find_tests(self):
        pass

    @staticmethod
    def run_test(test):
        def run():
            pytest.main(["-x", test])
        return run

    @staticmethod
    def get_suite_name(test):
        return 'TestSuite'


class UnittestLoader:

    def __init__(self):
        self.tests = []

    def find_tests(self, pattern='test*.py'):

        loader = unittest.TestLoader()
        suite = loader.loadTestsFromName(pattern)

        return self._find_test_methods(suite)

    def find_suite(self, pattern='test*.py'):

        loader = unittest.TestLoader()
        suite = loader.loadTestsFromName(pattern)

        return suite

    def _find_test_methods(self, suite):

        def find(suite, test_methods):
            if issubclass(suite.__class__, unittest.TestCase):
                test_methods.append(suite)
                return
            for test in suite._tests:
                find(test, test_methods)

        test_methods = []
        find(suite, test_methods)
        return test_methods

    @staticmethod
    def run_test(test):
        runner = unittest.TextTestRunner()

        def run():
            runner.run(test)

        return run

    @staticmethod
    def get_test_name(test):
        return test._testMethodName

    @staticmethod
    def get_suite_name(test):
        return 'TestSuite'