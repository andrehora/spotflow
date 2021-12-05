import unittest
import shutil
import os.path
from happyflow.api import HappyFlow


class TestCSVReport(unittest.TestCase):

    # @unittest.skip
    def test_generate_csv_report_from_test_class(self):
        flow = HappyFlow()
        flow.target_methods(['email.message._parseparam'])
        flow.start()

        from test.test_email.test_email import TestMessageAPI

        runner = unittest.TextTestRunner()
        suite = unittest.TestLoader().loadTestsFromTestCase(TestMessageAPI)
        runner.run(suite)

        flow.stop()

        result = flow.result()
        flow.csv_report()

        self.assertEqual(len(result), 1)
        self.assertEqual(len(result['email.message._parseparam'].calls), 94)

        self.assertTrue(os.path.isdir('./report_csv'))
        self.assertTrue(os.path.isfile('./report_csv/email.message._parseparam.csv'))
        self.assertTrue(os.path.isfile('./report_csv/index.csv'))
        shutil.rmtree('./report_csv')

    def test_generate_csv_report_count_uppercase_words(self):

        flow = HappyFlow()
        flow.target_methods(['tests.stub_funcs.count_uppercase_words'])
        flow.start()

        from tests.stub_funcs import inputs_count
        inputs_count()

        flow.stop()
        flow.csv_report()

        self.assertTrue(os.path.isdir('./report_csv'))
        self.assertTrue(os.path.isfile('./report_csv/tests.stub_funcs.count_uppercase_words.csv'))
        self.assertTrue(os.path.isfile('./report_csv/index.csv'))
        shutil.rmtree('./report_csv')

    def test_generate_csv_report_parseparam(self):
        flow = HappyFlow()
        flow.target_methods(['tests.stub_funcs.parseparam'])
        flow.start()

        from tests.stub_funcs import inputs_parseparam
        inputs_parseparam()

        flow.stop()
        flow.csv_report()

        self.assertTrue(os.path.isdir('./report_csv'))
        self.assertTrue(os.path.isfile('./report_csv/tests.stub_funcs.parseparam.csv'))
        self.assertTrue(os.path.isfile('./report_csv/index.csv'))
        shutil.rmtree('./report_csv')

    def test_generate_csv_report_splitparam(self):
        flow = HappyFlow()
        flow.target_methods(['tests.stub_funcs.splitparam'])
        flow.start()

        from tests.stub_funcs import inputs_splitparam
        inputs_splitparam()

        flow.stop()
        flow.csv_report()

        self.assertTrue(os.path.isdir('./report_csv'))
        self.assertTrue(os.path.isfile('./report_csv/tests.stub_funcs.splitparam.csv'))
        self.assertTrue(os.path.isfile('./report_csv/index.csv'))
        shutil.rmtree('./report_csv')


if __name__ == '__main__':
    unittest.main()
