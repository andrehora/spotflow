import unittest
import shutil
import os.path
from happyflow.api import trace_from_test_class, trace_from_test_module, trace_from_func


class TestE2E(unittest.TestCase):

    @unittest.skip
    def test_generate_html_report_from_test_class(self):

        from test.test_email.test_email import TestMessageAPI

        is_exported = trace_from_test_class(TestMessageAPI, ['email.message._parseparam'], report_format='html')
        self.assertTrue(is_exported)
        self.assertTrue(os.path.isdir('./report'))
        self.assertTrue(os.path.isfile('./report/email.message._parseparam.html'))
        self.assertTrue(os.path.isfile('./report/index.html'))
        self.assertTrue(os.path.isfile('./report/style.css'))
        self.assertTrue(os.path.isfile('./report/highlight.css'))
        self.assertTrue(os.path.isfile('./report/coverage_html.js'))
        shutil.rmtree('./report')

    @unittest.skip
    def test_generate_txt_report(self):

        from examples.examples_func import inputs_count, inputs_parseparam, inputs_splitparam, count_uppercase_words, parseparam, splitparam

        is_exported = trace_from_func(inputs_count, count_uppercase_words, report_format='txt')
        self.assertTrue(is_exported)

        is_exported = trace_from_func(inputs_parseparam, parseparam, report_format='txt')
        self.assertTrue(is_exported)

        is_exported = trace_from_func(inputs_splitparam, splitparam, report_format='txt')
        self.assertTrue(is_exported)


if __name__ == '__main__':
    unittest.main()