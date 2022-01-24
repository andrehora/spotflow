import unittest
from happyflow.api import HappyFlow


class TestTXTReport(unittest.TestCase):

    def test_generate_txt_report_count_uppercase_words(self):

        call = HappyFlow()
        call.target_methods(['tests.integration.stub_funcs.count_uppercase_words'])
        call.start()

        from tests.e2e.stub_funcs import inputs_count
        inputs_count()

        call.stop()
        is_exported = call.txt_report()
        self.assertTrue(is_exported)

    def test_generate_txt_report_parseparam(self):
        hp = HappyFlow()
        hp.target_methods(['tests.integration.stub_funcs.parseparam'])
        hp.start()

        from tests.e2e.stub_funcs import inputs_parseparam
        inputs_parseparam()

        hp.stop()
        is_exported = hp.txt_report()
        self.assertTrue(is_exported)

    def test_generate_txt_report_splitparam(self):
        hp = HappyFlow()
        hp.target_methods(['tests.integration.stub_funcs.splitparam'])
        hp.start()

        from tests.e2e.stub_funcs import inputs_splitparam
        inputs_splitparam()

        hp.stop()
        is_exported = hp.txt_report()
        self.assertTrue(is_exported)


if __name__ == '__main__':
    unittest.main()