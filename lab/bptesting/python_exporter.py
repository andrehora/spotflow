from spotflow.api import monitor_unittest_module
from lab.bptesting.exporter import calls_with_return_and_args
from platform import python_version
import importlib


def export_bptesting(project_name):

    test_suite = f'test.test_{project_name}'
    test = importlib.import_module(test_suite)

    output_folder = 'output'
    project = 'gzip'
    version = python_version()

    save_folder = output_folder + "/" + version + "/" + project + "-" + version
    print(save_folder)

    monitored_program = monitor_unittest_module(test, [project])
    calls_with_return_and_args(monitored_program, save_folder)


projects = ['gzip']

for project in projects:
    export_bptesting(project)
