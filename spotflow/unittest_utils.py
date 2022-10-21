import unittest


loader = unittest.TestLoader()


def loadTestsFromTestCase(test_class):
    suite = loader.loadTestsFromTestCase(test_class)
    return suite


def loadTestsFromModule(module):
    suite = loader.loadTestsFromModule(module)
    return suite


def loadTestsFromName(pattern='test*.py'):
    suite = loader.loadTestsFromName(pattern)
    return suite


def suite_runner(suite):
    test_runner = unittest.TextTestRunner()

    def runner():
        test_runner.run(suite)

    return runner
