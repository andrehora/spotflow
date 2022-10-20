import argparse
import configparser
import importlib.util
from happyflow.api import SpotFlow
# from happyflow.libs.execfile import PyRunner
from coverage.cmdline import PyRunner

OK, ERR = 0, 1

parser = argparse.ArgumentParser(description='Command line for HappyFlow')

parser.add_argument('-a', '--action', type=str,
                    help='Action to be performed after monitoring the program. '
                         'It can be "mine", "html", or "csv". '
                         'Default is "mine".')

parser.add_argument('-t', '--target-method', type=str, action='append',
                    help='Target method full name (in the format module.Class.method) or prefix. '
                         'For example, "parser.StringParser.count" or simply "parse". '
                         'To monitor multiple methods, use multiple arguments, like -tm name1 -tm name2 -tm ...')

parser.add_argument('-f', '--target-file', type=str, action='append',
                    help='Target file. It can be a substring of the file full path. '
                         'For example, "path/to/my_program.py" or simply "my_program". '
                         'To monitor multiple files, use multiple arguments, like -tf file1 -tf file2 -tf ...')

parser.add_argument('-i', '--ignore-file', type=str, action='append',
                    help='File to ignore. It can be a substring of the file full path. '
                         'To ignore multiple files, use multiple arguments, like -if file1 -if file2 -if ...')

parser.add_argument('-d', '--dir', type=str, help='Write the output files to dir.')

parser.add_argument('run',  type=str, nargs=argparse.REMAINDER,
                    help='Command line to run, for example: "my_program.py", "pytest tests", "unittest discover", etc.')

args = parser.parse_args()


class HappyFlowScript:

    def __init__(self):
        self.action = args.action
        self.target_methods = args.target_method
        self.target_files = args.target_file
        self.ignore_files = args.ignore_file
        self.directory = args.dir
        self.run_args = args.run

    def command_line(self):
        if not self.run_args:
            print('Nothing to run...')
            return OK

        print(f"Running: {' '.join(self.run_args)}")
        return self.run()

    def run(self):

        hp = SpotFlow()
        hp.target_methods(self.target_methods)
        hp.target_files(self.target_files)
        hp.ignore_files(self.ignore_files)
        states = self.handle_config()
        if states:
            hp.collect_states(*states)

        py_runner = PyRunner(self.run_args, as_module=True)
        py_runner.prepare()

        hp.start()
        code_ran = True
        try:
            py_runner.run()
        except Exception as e:
            print(e)
            code_ran = False
        finally:
            hp.stop()
            if code_ran:
                self.handle_action(hp)
                return OK
            return ERR

    def handle_config(self):
        config = configparser.ConfigParser()
        has_config = config.read('./spotflow.cfg')
        if has_config:
            if 'state' in config:
                state = config['state']
                arg_states = state.getboolean('arg_states')
                return_states = state.getboolean('return_state')
                yield_states = state.getboolean('yield_states')
                exception_states = state.getboolean('exception_states')
                var_states = state.getboolean('var_states')
                states = arg_states, return_states, yield_states, exception_states, var_states
                return states
        return None

    def handle_action(self, spotter):

        if not self.action:
            self.handle_mine(spotter.result())

        if self.action and self.action.lower() == 'mine':
            self.handle_mine(spotter.result())

        if self.action and self.action.lower() == 'html':
            spotter.html_report(self.directory)

        if self.action and self.action.lower() == 'csv':
            spotter.csv_report(self.directory)

    def handle_mine(self, result):
        spec = importlib.util.spec_from_file_location("spotflow_report", "./scripts/spotflow_report.py")
        spotflow_report = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(spotflow_report)
        spotflow_report.process(result)


def main():
    try:
        status = HappyFlowScript().command_line()
    except Exception as e:
        print(e)
        status = ERR
    return status