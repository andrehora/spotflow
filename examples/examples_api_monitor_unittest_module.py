from spotflow.api import monitor_unittest_module


from test import test_locale as test
monitored_program = monitor_unittest_module(test, ['locale'])
# monitored_program.show_summary()
