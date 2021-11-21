import unittest
from happyflow.api import HappyFlow


class TestE2E(unittest.TestCase):

    def test_generate_txt_report_count_uppercase_words(self):

        flow = HappyFlow()
        flow.target_entities(['tests.stub_funcs.count_uppercase_words'])
        flow.start()

        from tests.stub_funcs import inputs_count
        inputs_count()

        flow.stop()
        is_exported = flow.txt_report()
        self.assertTrue(is_exported)

    def test_generate_txt_report_parseparam(self):
        flow = HappyFlow()
        flow.target_entities(['tests.stub_funcs.parseparam'])
        flow.start()

        from tests.stub_funcs import inputs_parseparam
        inputs_parseparam()

        flow.stop()
        is_exported = flow.txt_report()
        self.assertTrue(is_exported)

    def test_generate_txt_report_splitparam(self):
        flow = HappyFlow()
        flow.target_entities(['tests.stub_funcs.splitparam'])
        flow.start()

        from tests.stub_funcs import inputs_splitparam
        inputs_splitparam()

        flow.stop()
        is_exported = flow.txt_report()
        self.assertTrue(is_exported)


if __name__ == '__main__':
    unittest.main()