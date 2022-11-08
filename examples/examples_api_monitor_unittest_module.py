from spotflow.api import monitor_unittest_module


from test import test_gzip
monitored_program = monitor_unittest_module(test_gzip, ['gzip'])
monitored_program.show_objects()
