import unittest
import shutil
import os.path
from happyflow.api import HappyFlow


class TestCSVReport(unittest.TestCase):

    # @unittest.skip
    def test_generate_csv_report_from_test_class(self):
        hp = HappyFlow()
        hp.target_methods(['email.message._parseparam'])
        hp.start()

        from test.test_email.test_email import TestMessageAPI

        runner = unittest.TextTestRunner()
        suite = unittest.TestLoader().loadTestsFromTestCase(TestMessageAPI)
        runner.run(suite)

        hp.stop()

        result = hp.result()
        hp.csv_report()

        self.assertEqual(len(result), 1)
        self.assertEqual(len(result['email.message._parseparam'].calls), 94)

        self.assertTrue(os.path.isdir('./report_csv'))
        self.assertTrue(os.path.isfile('./report_csv/email.message._parseparam.csv'))
        self.assertTrue(os.path.isfile('./report_csv/index.csv'))
        shutil.rmtree('./report_csv')

    def test_generate_csv_report_count_uppercase_words(self):

        hp = HappyFlow()
        hp.target_methods(['tests.e2e.stub_funcs.count_uppercase_words'])
        hp.start()

        from tests.e2e.stub_funcs import inputs_count
        inputs_count()

        hp.stop()
        hp.csv_report()

        self.assertTrue(os.path.isdir('./report_csv'))
        self.assertTrue(os.path.isfile('./report_csv/tests.e2e.stub_funcs.count_uppercase_words.csv'))
        self.assertTrue(os.path.isfile('./report_csv/index.csv'))
        shutil.rmtree('./report_csv')

    def test_generate_csv_report_parseparam(self):
        hp = HappyFlow()
        hp.target_methods(['tests.e2e.stub_funcs.parseparam'])
        hp.start()

        from tests.e2e.stub_funcs import inputs_parseparam
        inputs_parseparam()

        hp.stop()
        hp.csv_report()

        self.assertTrue(os.path.isdir('./report_csv'))
        self.assertTrue(os.path.isfile('./report_csv/tests.e2e.stub_funcs.parseparam.csv'))
        self.assertTrue(os.path.isfile('./report_csv/index.csv'))
        shutil.rmtree('./report_csv')

    def test_generate_csv_report_splitparam(self):
        hp = HappyFlow()
        hp.target_methods(['tests.e2e.stub_funcs.splitparam'])
        hp.start()

        from tests.e2e.stub_funcs import inputs_splitparam
        inputs_splitparam()

        hp.stop()
        hp.csv_report()

        self.assertTrue(os.path.isdir('./report_csv'))
        self.assertTrue(os.path.isfile('./report_csv/tests.e2e.stub_funcs.splitparam.csv'))
        self.assertTrue(os.path.isfile('./report_csv/index.csv'))
        shutil.rmtree('./report_csv')


if __name__ == '__main__':
    unittest.main()
