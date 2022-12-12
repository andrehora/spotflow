from exp.bptesting.exporter import export_calls_with_return_and_args
from spotflow.utils import ensure_dir


output_dir = 'output'
project = 'rich'


def get_output_dir(output_dir, project, version):
    return output_dir + "/" + project + "-" + version


def spotflow_post(monitored_program, *args):

    version = args[0]

    save_dir = get_output_dir(output_dir, project, version)
    ensure_dir(save_dir)
    print(save_dir)

    export_calls_with_return_and_args(monitored_program, save_dir)
