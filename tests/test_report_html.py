import unittest
import shutil
import os.path
from happyflow.api import HappyFlow


class TestHTMLReport(unittest.TestCase):

    # @unittest.skip
    def test_generate_html_report_from_test_class(self):
        flow = HappyFlow()
        flow.target_methods(['email.message._parseparam',
                             'email.message._formatparam',
                             'email.message._splitparam',
                             'email.message._unquotevalue'])
        flow.start()

        from test.test_email.test_email import TestMessageAPI

        # Run code
        runner = unittest.TextTestRunner()
        suite = unittest.TestLoader().loadTestsFromTestCase(TestMessageAPI)
        runner.run(suite)

        flow.stop()
        result = flow.result()
        flow.html_report()

        self.assertEqual(len(result), 4)

        self.assertEqual(len(result['email.message._parseparam'].calls), 94)
        self.assertEqual(len(result['email.message._formatparam'].calls), 35)
        self.assertEqual(len(result['email.message._splitparam'].calls), 444)
        self.assertEqual(len(result['email.message._unquotevalue'].calls), 98)

        self.assertEqual(len(result['email.message._parseparam'].flows), 3)
        self.assertEqual(len(result['email.message._formatparam'].flows), 4)
        self.assertEqual(len(result['email.message._splitparam'].flows), 2)
        self.assertEqual(len(result['email.message._unquotevalue'].flows), 1)

        self.assertTrue(os.path.isdir('./report_html'))
        self.assertTrue(os.path.isfile('./report_html/email.message._parseparam.html'))
        self.assertTrue(os.path.isfile('./report_html/email.message._formatparam.html'))
        self.assertTrue(os.path.isfile('./report_html/email.message._splitparam.html'))
        self.assertTrue(os.path.isfile('./report_html/email.message._unquotevalue.html'))
        self.assertTrue(os.path.isfile('./report_html/index.html'))
        self.assertTrue(os.path.isfile('./report_html/style.css'))
        self.assertTrue(os.path.isfile('./report_html/highlight.css'))
        self.assertTrue(os.path.isfile('./report_html/coverage_html.js'))
        shutil.rmtree('./report_html')

    def test_generate_html_report_count_uppercase_words(self):

        flow = HappyFlow()
        flow.target_methods(['tests.stub_funcs.count_uppercase_words'])
        flow.start()

        # Run code
        from tests.stub_funcs import inputs_count
        inputs_count()

        flow.stop()
        flow.html_report()

        self.assertTrue(os.path.isdir('./report_html'))
        self.assertTrue(os.path.isfile('./report_html/tests.stub_funcs.count_uppercase_words.html'))
        self.assertTrue(os.path.isfile('./report_html/index.html'))
        self.assertTrue(os.path.isfile('./report_html/style.css'))
        self.assertTrue(os.path.isfile('./report_html/highlight.css'))
        self.assertTrue(os.path.isfile('./report_html/coverage_html.js'))
        shutil.rmtree('./report_html')

    def test_generate_html_report_parseparam(self):
        flow = HappyFlow()
        flow.target_methods(['tests.stub_funcs.parseparam'])
        flow.start()

        # Run code
        from tests.stub_funcs import inputs_parseparam
        inputs_parseparam()

        flow.stop()
        flow.html_report()

        self.assertTrue(os.path.isdir('./report_html'))
        self.assertTrue(os.path.isfile('./report_html/tests.stub_funcs.parseparam.html'))
        self.assertTrue(os.path.isfile('./report_html/index.html'))
        self.assertTrue(os.path.isfile('./report_html/style.css'))
        self.assertTrue(os.path.isfile('./report_html/highlight.css'))
        self.assertTrue(os.path.isfile('./report_html/coverage_html.js'))
        shutil.rmtree('./report_html')

    def test_generate_html_report_splitparam(self):
        flow = HappyFlow()
        flow.target_methods(['tests.stub_funcs.splitparam'])
        flow.start()

        # Run code
        from tests.stub_funcs import inputs_splitparam
        inputs_splitparam()

        flow.stop()
        flow.html_report()

        self.assertTrue(os.path.isdir('./report_html'))
        self.assertTrue(os.path.isfile('./report_html/tests.stub_funcs.splitparam.html'))
        self.assertTrue(os.path.isfile('./report_html/index.html'))
        self.assertTrue(os.path.isfile('./report_html/style.css'))
        self.assertTrue(os.path.isfile('./report_html/highlight.css'))
        self.assertTrue(os.path.isfile('./report_html/coverage_html.js'))
        shutil.rmtree('./report_html')


if __name__ == '__main__':
    unittest.main()