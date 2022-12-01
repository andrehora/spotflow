from spotflow.api import monitor_unittest_module
from spotflow.utils import ensure_dir
from lab.datasets import exporter, python_metrics
from platform import python_version
import importlib


def get_output_dir(output_dir, version):
    return output_dir + "/" + version + "/"


def export(project, output_dir):

    test_suite = f'test.test_{project}'
    test = importlib.import_module(test_suite)

    version = python_version()

    save_dir = get_output_dir(output_dir, version)
    ensure_dir(save_dir)
    filename = project + "-" + version + ".csv"
    full_filename = save_dir + filename
    print(full_filename)

    monitored_program = monitor_unittest_module(test, [project], var_states=False)
    exporter.export_metrics_to_csv(monitored_program, full_filename, python_metrics.metrics)


output_dir = 'output'
projects = ['gzip', 'locale']

for project in projects:
    print(project)
    export(project, output_dir)
