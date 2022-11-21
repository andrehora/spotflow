from spotflow.api import monitor_unittest_module
from lab.bptesting.exporter import calls_with_return_and_args
from platform import python_version


from test import test_gzip as test
output_folder = python_version()
project = 'gzip'
python_version = python_version()
save_folder = output_folder + "/" + project + "-" + python_version

monitored_program = monitor_unittest_module(test, [project])
calls_with_return_and_args(monitored_program, save_folder)
