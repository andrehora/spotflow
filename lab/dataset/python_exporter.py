from spotflow.api import monitor_unittest_module
from lab.dataset.exporter import method_metrics
from platform import python_version
import importlib


def get_output_dir(output_dir, project, version):
    return output_dir + "/" + version + "/" + project + "-" + version


def export_dataset(project, output_dir):

    test_suite = f'test.test_{project}'
    test = importlib.import_module(test_suite)

    version = python_version()

    save_dir = get_output_dir(output_dir, project, version)
    print(save_dir)

    monitored_program = monitor_unittest_module(test, [project], var_states=False)
    method_metrics(monitored_program, save_dir)


output_dir = 'output'
projects = ['gzip', 'locale']

for project in projects:
    print(project)
    export_dataset(project, output_dir)
