from spotflow.api import monitor_unittest_module


from test import test_json as test
monitored_program = monitor_unittest_module(test, ['json'])
# monitored_program.show_summary()
