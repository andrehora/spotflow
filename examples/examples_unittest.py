from happyflow.playground import trace_from_test_class, trace_from_test_module
from test.test_email.test_email import TestMessageAPI
from test.test_email import test_email


trace_from_test_class(TestMessageAPI, ['message._parseparam'])
# trace_from_test_module(test_email, ['message._parseparam'])
