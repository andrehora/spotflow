from spotflow.api import monitor_unittest_module
from lab.bptesting.exporter import calls_with_return_and_args
from platform import python_version
import importlib


def get_output_dir(output_dir, project, version):
    return output_dir + "/" + version + "/" + project + "-" + version


def export_bptesting(project):

    test_suite = f'test.test_{project}'
    test = importlib.import_module(test_suite)

    output_dir = 'output'
    version = python_version()

    save_dir = get_output_dir(output_dir, project, version)
    # save_dir = output_dir + "/" + version + "/" + project + "-" + version
    print(save_dir)

    monitored_program = monitor_unittest_module(test, [project])
    calls_with_return_and_args(monitored_program, save_dir)


# projects = ['ast', 'gzip', 'json', 'calendar', 'collections', 'csv', 'ftplib', 'tarfile', 'locale', 'difflib']
projects = ['ast', 'gzip', 'json', 'csv', 'locale']

for project in projects:
    print(project)
    export_bptesting(project)
