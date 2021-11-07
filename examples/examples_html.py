from happyflow.api import trace_from_test_class
from happyflow.api import trace_from_test_module

# from test.test_email.test_email import TestMessageAPI
# trace_from_test_class(TestMessageAPI, ['message'], report_format='html')

# from test import test_ast
# trace_from_test_module(test_ast, ['ast'], report_format='html')


# from test import test_gzip
# trace_from_test_module(test_gzip, ['gzip'])

from test.test_urlparse import UrlParseTestCase
trace_from_test_class(UrlParseTestCase, ['parse._splitparams'], report_format='html')



