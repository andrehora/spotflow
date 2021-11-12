import unittest
from happyflow.api import trace_from_test_class, trace_from_test_module


# from test.test_email.test_email import TestMessageAPI
# trace_from_test_class(TestMessageAPI, ['email.generator.Generator.flatten'], report_format='html', report_dir='xxx')

# from test.test_email import test_email
# trace_from_test_module(test_email, ['email.generator.Generator.flatten'], report_format='html', report_dir='xxx2')

from test.test_email import test_email
trace_from_test_module(test_email, ['email'], report_format='html', report_dir='email')

# runner = unittest.TextTestRunner()
# suite = unittest.TestLoader().loadTestsFromModule(test_email)
# runner.run(suite)


# from test import test_ast
# trace_from_test_module(test_ast, ['ast'], report_format='html', report_dir='ast')
#
#
# from test import test_gzip
# trace_from_test_module(test_gzip, ['gzip'], report_format='html', report_dir='gzip')
#
#
# from test import test_urlparse
# trace_from_test_module(test_urlparse, ['urllib'], report_format='html', report_dir='urllib')

