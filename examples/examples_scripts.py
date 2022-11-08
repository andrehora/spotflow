from spotflow.api import monitor_unittest_module
from examples.scripts import arguments, basics, exceptions, returns, tests


from test import test_gzip
monitored_program = monitor_unittest_module(test_gzip, ['gzip'])

basics.monitored_methods_overview(monitored_program)

# tests.tests_that_execute_specific_method(monitored_program, 'gzip._PaddedFile.read')
# tests.methods_executed_by_specific_test(monitored_program, 'test.test_gzip.TestGzip.test_zero_padded_file')
# exceptions.thrown_exceptions(monitored_program)
# returns.calls_that_return_value(monitored_program)
# returns.calls_that_return_true_or_false(monitored_program)
# arguments.argument_values_and_types(monitored_program)
# arguments.argument_values_for_specific_type(monitored_program, 'str')

# returns.calls_with_arg_and_return(monitored_program)
# returns.return_and_arg_values_and_types(monitored_program)
# returns.calls_with_primitive_types(monitored_program)
# returns.calls_with_return_and_args(monitored_program)
