import unittest


class UnittestFramework:

    def find_funcs(self, pattern):

        loader = unittest.TestLoader()
        # suite = loader.discover('.', pattern)
        suite = loader.loadTestsFromName(pattern)

        return self._find_test_methods(suite)

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

    def run_func(self, func):
        runner = unittest.TextTestRunner()

        def run():
            runner.run(func)

        return run

    def get_func_name(self, test):
        return test._testMethodName


class PyTestFramework:

    def find_funcs(self):
        pass

    def run_func(self):
        pass

    def get_func_name(self):
        pass


class TestLoader:

    def __init__(self, testing_framework=UnittestFramework()):
        self.tests = []
        self.testing_framework = testing_framework

    def find_tests(self, pattern='test*.py'):
        self.tests = self.testing_framework.find_funcs(pattern)
        return self.tests
