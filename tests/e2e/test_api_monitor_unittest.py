import unittest
from spotflow.api import monitor_unittest_module, monitor_unittest_testcase


class TestMonitorUnittest(unittest.TestCase):

    def test_monitor_unittest_module_gzip(self):

        from test import test_gzip
        monitored_program = monitor_unittest_module(test_gzip, ['gzip'])
        self.assertGreater(len(monitored_program.all_methods()), 25)

    def test_monitor_unittest_testcase_email(self):
        from test.test_email.test_email import TestMessageAPI
        monitored_program = monitor_unittest_testcase(TestMessageAPI, ['email'])
        self.assertGreater(len(monitored_program.all_methods()), 100)


if __name__ == '__main__':
    unittest.main()
