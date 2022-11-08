import unittest
from spotflow.api import SpotFlow, pprint


class TestPrettyPrintReport(unittest.TestCase):

    def test_generate_pprint_report_count_uppercase_words(self):

        flow = SpotFlow()
        flow.target_methods(['tests.e2e.stub_funcs.count_uppercase_words'])
        flow.start()

        from tests.e2e.stub_funcs import inputs_count
        inputs_count()

        flow.stop()
        is_exported = flow.pprint_report()
        self.assertTrue(is_exported)

    def test_generate_pprint_report_parseparam(self):
        flow = SpotFlow()
        flow.target_methods(['tests.e2e.stub_funcs.parseparam'])
        flow.start()

        from tests.e2e.stub_funcs import inputs_parseparam
        inputs_parseparam()

        flow.stop()
        is_exported = flow.pprint_report()
        self.assertTrue(is_exported)

    def test_generate_pprint_report_splitparam(self):
        flow = SpotFlow()
        flow.target_methods(['tests.e2e.stub_funcs.splitparam'])
        flow.start()

        from tests.e2e.stub_funcs import inputs_splitparam
        inputs_splitparam()

        flow.stop()
        is_exported = flow.pprint_report()
        self.assertTrue(is_exported)

    def test_generate_pprint_report_count_uppercase_words_shortcut(self):

        from tests.e2e.stub_funcs import inputs_count, count_uppercase_words
        is_exported = pprint(inputs_count, [count_uppercase_words])
        self.assertTrue(is_exported)

    def test_generate_pprint_report_parseparam_shortcut(self):

        from tests.e2e.stub_funcs import inputs_parseparam, parseparam
        is_exported = pprint(inputs_parseparam, [parseparam])
        self.assertTrue(is_exported)

    def test_generate_pprint_report_splitparam_shortcut(self):

        from tests.e2e.stub_funcs import inputs_splitparam, splitparam
        is_exported = pprint(inputs_splitparam, [splitparam])
        self.assertTrue(is_exported)


if __name__ == '__main__':
    unittest.main()
