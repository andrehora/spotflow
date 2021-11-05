import unittest
from happyflow.playground import trace_from_test_class, trace_from_test_module
from test.test_email.test_email import TestMessageAPI
# from test import test_email


trace_from_test_class(TestMessageAPI, ['message'])
# trace_from_test_module(test_email, ['message'])

# runner = unittest.TextTestRunner()
# suite = unittest.TestLoader().loadTestsFromModule(test_email)
# runner.run(suite)
