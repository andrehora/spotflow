import argparse
import configparser
import importlib.util
from spotflow.api import SpotFlow
from coverage.cmdline import PyRunner

OK, ERR = 0, 1


def parse_args():

    parser = argparse.ArgumentParser(description='Command line for SpotFlow')

    parser.add_argument('-a', '--action', type=str,
                        help='Action to be performed after monitoring the program. '
                             'It can be "summary", "calls", "post", or "pprint". '
                             'Default is "summary".')

    parser.add_argument('-arg', '--post-argument', type=str, action='append',
                        help='Arguments that are passed to "post" function. Accept multiple arguments.')

    parser.add_argument('-t', '--target-method', type=str, action='append',
                        help='Target method full name (in the format module.Class.method) or prefix. '
                             'For example, "parser.StringParser.count" or simply "parse". '
                             'To monitor multiple methods, use multiple arguments, like -t name1 -t name2 -t ...')

    parser.add_argument('-f', '--target-file', type=str, action='append',
                        help='Target file. It can be a substring of the file full path. '
                             'For example, "path/to/my_program.py" or simply "my_program". '
                             'To monitor multiple files, use multiple arguments, like -f file1 -f file2 -f ...')

    parser.add_argument('-i', '--ignore-file', type=str, action='append',
                        help='File to ignore. It can be a substring of the file full path. '
                             'To ignore multiple files, use multiple arguments, like -i file1 -i file2 -i ...')

    parser.add_argument('-d', '--dir', type=str, help='Write the output files to dir.')

    parser.add_argument('run',  type=str, nargs=argparse.REMAINDER,
                        help='Command line to run, for example: "my_program.py", "pytest tests", "unittest discover", etc.')

    return parser.parse_args()


class SpotFlowScript:

    def __init__(self):
        args = parse_args()
        self.action = args.action
        self.post_args = args.post_argument
        if not self.post_args:
            self.post_args = []
        self.target_methods = args.target_method
        self.target_files = args.target_file
        self.ignore_files = args.ignore_file
        self.directory = args.dir
        self.run_args = args.run

    def command_line(self):
        if not self.run_args:
            print('Nothing to run...')
            return OK

        print(f"Running and monitoring: {' '.join(self.run_args)}")
        return self.run()

    def run(self):

        flow = SpotFlow()
        flow.target_methods(self.target_methods)
        flow.target_files(self.target_files)
        flow.ignore_files(self.ignore_files)
        states = self.parse_config()
        if states:
            flow.collect_states(*states)

        py_runner = PyRunner(self.run_args, as_module=True)
        py_runner.prepare()

        flow.start()
        code_ran = True
        try:
            py_runner.run()
        except Exception as e:
            # print(e)
            code_ran = False
        finally:
            flow.stop()
            if code_ran:
                self.handle_action(flow)
                return OK
            return ERR

    def parse_config(self):
        config = configparser.ConfigParser()
        has_config = config.read('./spotflow.cfg')
        if has_config:

            if 'state' not in config:
                return None

            state = config['state']
            arg_states = state.getboolean('arg_states')
            return_states = state.getboolean('return_state')
            yield_states = state.getboolean('yield_states')
            exception_states = state.getboolean('exception_states')
            var_states = state.getboolean('var_states')

            states = arg_states, return_states, yield_states, exception_states, var_states

            return states

    def handle_action(self, flow):

        if not self.action or (self.action and self.action.lower() == 'summary'):
            pass
            # flow.result().show_summary()

        if self.action and self.action.lower() == 'calls':
            flow.result().show_calls()

        if self.action and self.action.lower() == 'post':
            self.run_spotflow_post(flow.result())

        if self.action and self.action.lower() == 'pprint':
            flow.pprint_report()

        # if self.action and self.action.lower() == 'html':
        #     flow.html_report(self.directory)
        #
        # if self.action and self.action.lower() == 'csv':
        #     flow.csv_report(self.directory)

    def run_spotflow_post(self, result):
        spec = importlib.util.spec_from_file_location(".", "./spotflow.py")
        spotflow_post = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(spotflow_post)
        spotflow_post.spotflow_post(result, *self.post_args)


def main():
    try:
        status = SpotFlowScript().command_line()
    except Exception as e:
        print(e)
        status = ERR
    return status
