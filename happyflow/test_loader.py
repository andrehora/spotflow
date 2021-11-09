import unittest
import pytest


class PytestLoader:

    @staticmethod
    def run_test(test):
        def run():
            pytest.main(["-x", test])
        return run


class UnittestLoader:

    def __init__(self):
        self.tests = []
        self.loader = unittest.TestLoader()

    def loadTestsFromTestCase(self, test_class):
        suite = self.loader.loadTestsFromTestCase(test_class)
        return suite

    def loadTestsFromModule(self, module):
        suite = self.loader.loadTestsFromModule(module)
        return suite

    def loadTestsFromName(self, pattern='test*.py'):
        suite = self.loader.loadTestsFromName(pattern)
        return suite

    @staticmethod
    def run_test(test):
        runner = unittest.TextTestRunner()

        def run():
            runner.run(test)

        return run
