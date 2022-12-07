from spotflow.api import monitor_unittest_module


from test import test_gzip as test
monitored_program = monitor_unittest_module(test, ['gzip'])
# monitored_program.show_summary()
