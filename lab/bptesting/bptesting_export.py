from spotflow.api import monitor_unittest_module
from spotflow.utils import get_python_version
from lab.bptesting.bptesting import calls_with_return_and_args

from test import test_gzip as test

project = 'gzip'
python_version = get_python_version()
folder = project + python_version

monitored_program = monitor_unittest_module(test, [project])

calls_with_return_and_args(monitored_program, folder)