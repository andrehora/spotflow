from happyflow.api import monitor_unittest_module
from mining_scripts import basics, tests, exceptions, returns, arguments


def main():
    from test import test_gzip
    monitored_system = monitor_unittest_module(test_gzip, ['gzip'])

    basics.monitored_methods_overview(monitored_system)
    tests.tests_that_execute_specific_method(monitored_system, 'gzip._PaddedFile.read')
    tests.methods_executed_by_specific_test(monitored_system, 'test.test_gzip.TestGzip.test_zero_padded_file')
    exceptions.thrown_exceptions(monitored_system)
    returns.calls_that_return_value(monitored_system)
    returns.calls_that_return_true_or_false(monitored_system)
    arguments.argument_values_and_types(monitored_system)
    arguments.argument_values_for_specific_type(monitored_system, 'str')


main()