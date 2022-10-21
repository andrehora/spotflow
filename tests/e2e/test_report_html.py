import unittest
import shutil
import os.path
from spotflow.api import SpotFlow


class TestHTMLReport(unittest.TestCase):

    def assert_exists(self, filename):
        self.assertTrue(os.path.exists(filename))

    # @unittest.skip
    def test_generate_html_report_from_test_class(self):
        flow = SpotFlow()
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

        call1 = result['email.message._parseparam'].flows[0]
        self.assertEqual(len(call1.info.lines), 18)
        self.assertEqual(call1.info.run_count, 15)
        self.assertEqual(call1.info.not_run_count, 1)
        self.assertEqual(call1.info.not_exec_count, 2)
        self.assertEqual(call1.info.call_count, 83)
        self.assertEqual(call1.info.call_ratio, 88.3)
        self.assertEqual(call1.info.lines[0].code(), 'def _parseparam(s):')
        self.assertEqual(call1.info.lines[0].html(), '<span class="k">def</span> <span class="nf">_parseparam</span><span class="p">(</span><span class="n">s</span><span class="p">):</span>')
        self.assertTrue(call1.info.lines[0].is_not_exec())
        self.assertTrue(call1.info.lines[1].is_not_exec())
        self.assertTrue(call1.info.lines[2].is_run())
        self.assertTrue(call1.info.lines[8].is_not_run())

        call2 = result['email.message._parseparam'].flows[1]
        self.assertEqual(len(call2.info.lines), 18)
        self.assertEqual(call2.info.run_count, 13)
        self.assertEqual(call2.info.not_run_count, 3)
        self.assertEqual(call2.info.not_exec_count, 2)
        self.assertEqual(call2.info.call_count, 9)
        self.assertEqual(call2.info.call_ratio, 9.6)
        self.assertEqual(call2.info.lines[0].code(), 'def _parseparam(s):')
        self.assertEqual(call2.info.lines[0].html(), '<span class="k">def</span> <span class="nf">_parseparam</span><span class="p">(</span><span class="n">s</span><span class="p">):</span>')
        self.assertTrue(call2.info.lines[0].is_not_exec())
        self.assertTrue(call2.info.lines[1].is_not_exec())
        self.assertTrue(call2.info.lines[2].is_run())
        self.assertTrue(call2.info.lines[8].is_not_run())
        self.assertTrue(call2.info.lines[13].is_not_run())
        self.assertTrue(call2.info.lines[14].is_not_run())

        call3 = result['email.message._parseparam'].flows[2]
        self.assertEqual(len(call3.info.lines), 18)
        self.assertEqual(call3.info.run_count, 16)
        self.assertEqual(call3.info.not_run_count, 0)
        self.assertEqual(call3.info.not_exec_count, 2)
        self.assertEqual(call3.info.call_count, 2)
        self.assertEqual(call3.info.call_ratio, 2.1)
        self.assertEqual(call3.info.lines[0].code(), 'def _parseparam(s):')
        self.assertEqual(call3.info.lines[0].html(), '<span class="k">def</span> <span class="nf">_parseparam</span><span class="p">(</span><span class="n">s</span><span class="p">):</span>')
        self.assertTrue(call3.info.lines[0].is_not_exec())
        self.assertTrue(call3.info.lines[1].is_not_exec())
        self.assertTrue(call3.info.lines[2].is_run())

        self.assert_exists('./spotflow_html_report')
        self.assert_exists('./spotflow_html_report/email.message._parseparam.html')
        self.assert_exists('./spotflow_html_report/email.message._formatparam.html')
        self.assert_exists('./spotflow_html_report/email.message._splitparam.html')
        self.assert_exists('./spotflow_html_report/email.message._unquotevalue.html')
        self.assert_exists('./spotflow_html_report/index.html')
        self.assert_exists('./spotflow_html_report/style.css')
        self.assert_exists('./spotflow_html_report/highlight.css')
        self.assert_exists('./spotflow_html_report/coverage_html.js')
        shutil.rmtree('./spotflow_html_report')

    def test_generate_html_report_count_uppercase_words(self):

        flow = SpotFlow()
        flow.target_methods(['tests.e2e.stub_funcs.count_uppercase_words'])
        flow.start()

        # Run code
        from tests.e2e.stub_funcs import inputs_count
        inputs_count()

        flow.stop()
        flow.html_report()

        self.assert_exists('./spotflow_html_report')
        self.assert_exists('./spotflow_html_report/tests.e2e.stub_funcs.count_uppercase_words.html')
        self.assert_exists('./spotflow_html_report/index.html')
        self.assert_exists('./spotflow_html_report/style.css')
        self.assert_exists('./spotflow_html_report/highlight.css')
        self.assert_exists('./spotflow_html_report/coverage_html.js')
        shutil.rmtree('./spotflow_html_report')

    def test_generate_html_report_parseparam(self):
        flow = SpotFlow()
        flow.target_methods(['tests.e2e.stub_funcs.parseparam'])
        flow.start()

        # Run code
        from tests.e2e.stub_funcs import inputs_parseparam
        inputs_parseparam()

        flow.stop()
        flow.html_report()

        self.assert_exists('./spotflow_html_report')
        self.assert_exists('./spotflow_html_report/tests.e2e.stub_funcs.parseparam.html')
        self.assert_exists('./spotflow_html_report/index.html')
        self.assert_exists('./spotflow_html_report/style.css')
        self.assert_exists('./spotflow_html_report/highlight.css')
        self.assert_exists('./spotflow_html_report/coverage_html.js')
        shutil.rmtree('./spotflow_html_report')

    def test_generate_html_report_splitparam(self):
        flow = SpotFlow()
        flow.target_methods(['tests.e2e.stub_funcs.splitparam'])
        flow.start()

        # Run code
        from tests.e2e.stub_funcs import inputs_splitparam
        inputs_splitparam()

        flow.stop()
        flow.html_report()

        self.assert_exists('./spotflow_html_report')
        self.assert_exists('./spotflow_html_report/tests.e2e.stub_funcs.splitparam.html')
        self.assert_exists('./spotflow_html_report/index.html')
        self.assert_exists('./spotflow_html_report/style.css')
        self.assert_exists('./spotflow_html_report/highlight.css')
        self.assert_exists('./spotflow_html_report/coverage_html.js')
        shutil.rmtree('./spotflow_html_report')


if __name__ == '__main__':
    unittest.main()