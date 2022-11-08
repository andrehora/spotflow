from spotflow.api import monitor_unittest_testcase


from test.test_gzip import TestGzip
monitored_program = monitor_unittest_testcase(TestGzip, ['gzip'])
monitored_program.show_objects()
