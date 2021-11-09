from happyflow.api import trace_from_test_class, trace_from_test_module


from test.test_email.test_email import TestMessageAPI
trace_from_test_class(TestMessageAPI, ['email.message._parseparam'], report_format='html')


# from test.test_email import test_email
# trace_from_test_module(test_email, ['email.message._parseparam'], report_format=None)




