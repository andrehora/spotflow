import unittest
import shutil
import os.path
from happyflow.api import HappyFlow


class TestE2E(unittest.TestCase):

    # @unittest.skip
    def test_generate_html_report_from_test_class(self):
        flow = HappyFlow()
        flow.target_entities(['email.message._parseparam'])
        flow.start()

        from test.test_email.test_email import TestMessageAPI

        runner = unittest.TextTestRunner()
        suite = unittest.TestLoader().loadTestsFromTestCase(TestMessageAPI)
        runner.run(suite)

        flow.stop()

        result = flow.result()
        is_exported = flow.html_report()

        self.assertEqual(len(result), 1)
        self.assertEqual(len(result['email.message._parseparam'].flows), 94)

        self.assertTrue(is_exported)
        self.assertTrue(os.path.isdir('./report'))
        self.assertTrue(os.path.isfile('./report/email.message._parseparam.html'))
        self.assertTrue(os.path.isfile('./report/index.html'))
        self.assertTrue(os.path.isfile('./report/style.css'))
        self.assertTrue(os.path.isfile('./report/highlight.css'))
        self.assertTrue(os.path.isfile('./report/coverage_html.js'))
        shutil.rmtree('./report')

    def test_generate_html_report_count_uppercase_words(self):

        flow = HappyFlow()
        flow.target_entities(['tests.stub_funcs.count_uppercase_words'])
        flow.start()

        from tests.stub_funcs import inputs_count
        inputs_count()

        flow.stop()
        is_exported = flow.html_report()

        self.assertTrue(is_exported)
        self.assertTrue(os.path.isdir('./report'))
        self.assertTrue(os.path.isfile('./report/tests.stub_funcs.count_uppercase_words.html'))
        self.assertTrue(os.path.isfile('./report/index.html'))
        self.assertTrue(os.path.isfile('./report/style.css'))
        self.assertTrue(os.path.isfile('./report/highlight.css'))
        self.assertTrue(os.path.isfile('./report/coverage_html.js'))
        shutil.rmtree('./report')

    def test_generate_html_report_parseparam(self):
        flow = HappyFlow()
        flow.target_entities(['tests.stub_funcs.parseparam'])
        flow.start()

        from tests.stub_funcs import inputs_parseparam
        inputs_parseparam()

        flow.stop()
        is_exported = flow.html_report()

        self.assertTrue(is_exported)
        self.assertTrue(os.path.isdir('./report'))
        self.assertTrue(os.path.isfile('./report/tests.stub_funcs.parseparam.html'))
        self.assertTrue(os.path.isfile('./report/index.html'))
        self.assertTrue(os.path.isfile('./report/style.css'))
        self.assertTrue(os.path.isfile('./report/highlight.css'))
        self.assertTrue(os.path.isfile('./report/coverage_html.js'))
        shutil.rmtree('./report')

    def test_generate_html_report_splitparam(self):
        flow = HappyFlow()
        flow.target_entities(['tests.stub_funcs.splitparam'])
        flow.start()

        from tests.stub_funcs import inputs_splitparam
        inputs_splitparam()

        flow.stop()
        is_exported = flow.html_report()

        self.assertTrue(is_exported)
        self.assertTrue(os.path.isdir('./report'))
        self.assertTrue(os.path.isfile('./report/tests.stub_funcs.splitparam.html'))
        self.assertTrue(os.path.isfile('./report/index.html'))
        self.assertTrue(os.path.isfile('./report/style.css'))
        self.assertTrue(os.path.isfile('./report/highlight.css'))
        self.assertTrue(os.path.isfile('./report/coverage_html.js'))
        shutil.rmtree('./report')


if __name__ == '__main__':
    unittest.main()