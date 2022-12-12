from spotflow.api import monitor_unittest_module
from spotflow.utils import ensure_dir
from exp.bptesting.exporter import export_calls_with_return_and_args
from platform import python_version
import importlib


def get_output_dir(output_dir, project, version):
    return output_dir + "/" + version + "/" + project + "-" + version


def export(project, output_dir):

    test_suite = f'test.test_{project}'
    test = importlib.import_module(test_suite)

    version = python_version()

    save_dir = get_output_dir(output_dir, version)
    ensure_dir(save_dir)
    print(save_dir)

    monitored_program = monitor_unittest_module(test, [project], var_states=False)
    export_calls_with_return_and_args(monitored_program, save_dir)


output_dir = 'output'
# projects = ['ast', 'gzip', 'json', 'calendar', 'collections', 'csv', 'ftplib', 'tarfile', 'locale', 'difflib']
projects = ['ast', 'gzip', 'json', 'locale']
# projects = ['calendar', 'collections', 'ftplib', 'tarfile', 'difflib']
# projects = ['gzip', 'locale']

for project in projects:
    print(project)
    export(project, output_dir)
