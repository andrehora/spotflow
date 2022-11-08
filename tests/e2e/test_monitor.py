import unittest
from spotflow.api import monitor


class TestMonitor(unittest.TestCase):

    def test_monitor_count_uppercase_words(self):

        from tests.e2e.stub_funcs import inputs_count, count_uppercase_words
        monitored_program = monitor(inputs_count, [count_uppercase_words])
        self.assertEqual(len(monitored_program.all_methods()), 1)

    def test_monitor_report_parseparam(self):

        from tests.e2e.stub_funcs import inputs_parseparam, parseparam
        monitored_program = monitor(inputs_parseparam, [parseparam])
        self.assertEqual(len(monitored_program.all_methods()), 1)

    def test_monitor_report_splitparam(self):

        from tests.e2e.stub_funcs import inputs_splitparam, splitparam
        monitored_program = monitor(inputs_splitparam, [splitparam])
        self.assertEqual(len(monitored_program.all_methods()), 1)


if __name__ == '__main__':
    unittest.main()
