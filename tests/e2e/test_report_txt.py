import unittest
from happyflow.api import SpotFlow


class TestTXTReport(unittest.TestCase):

    def test_generate_txt_report_count_uppercase_words(self):

        call = SpotFlow()
        call.target_methods(['tests.e2e.stub_funcs.count_uppercase_words'])
        call.start()

        from tests.e2e.stub_funcs import inputs_count
        inputs_count()

        call.stop()
        is_exported = call.txt_report()
        self.assertTrue(is_exported)

    def test_generate_txt_report_parseparam(self):
        hp = SpotFlow()
        hp.target_methods(['tests.e2e.stub_funcs.parseparam'])
        hp.start()

        from tests.e2e.stub_funcs import inputs_parseparam
        inputs_parseparam()

        hp.stop()
        is_exported = hp.txt_report()
        self.assertTrue(is_exported)

    def test_generate_txt_report_splitparam(self):
        hp = SpotFlow()
        hp.target_methods(['tests.e2e.stub_funcs.splitparam'])
        hp.start()

        from tests.e2e.stub_funcs import inputs_splitparam
        inputs_splitparam()

        hp.stop()
        is_exported = hp.txt_report()
        self.assertTrue(is_exported)


if __name__ == '__main__':
    unittest.main()