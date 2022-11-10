from spotflow.api import monitor_unittest_module
from lab.bptesting import calls_with_primitive_types, calls_with_return_and_args

from test import test_gzip as test
monitored_program = monitor_unittest_module(test, ['gzip'])

# calls_with_primitive_types(monitored_program)
calls_with_return_and_args(monitored_program)
