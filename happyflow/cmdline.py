import argparse
import importlib.util
from happyflow.api import HappyFlow
from happyflow.libs.execfile import PyRunner

OK, ERR = 0, 1

parser = argparse.ArgumentParser(description='Command line for HappyFlow')
parser.add_argument('-tm', '--target-method', type=str, action='append', help='One or more target methods')
parser.add_argument('-tf', '--target-file', type=str, action='append', help='One or more target files')
parser.add_argument('-if', '--ignore-file', type=str, action='append', help='One or more files to ignore')
parser.add_argument('-d', '--dir', type=str, help='Write the output files to dir')
parser.add_argument('-s', '--run-script', type=str, help='Python script to be run')
parser.add_argument('run',  type=str, nargs=argparse.REMAINDER, help='Command line to run, for example: pytest tests')
args = parser.parse_args()


class HappyFlowScript:

    def __init__(self):
        self.run_args = args.run
        self.directory = args.dir
        self.target_methods = args.target_method
        self.target_files = args.target_file
        self.ignore_files = args.ignore_file
        self.run_script = args.run_script

    def command_line(self):

        # run_args = args.run
        # directory = args.dir
        # target_methods = args.target_method
        # target_files = args.target_file
        # ignore_files = args.ignore_file
        # run_script = args.run_script

        if not self.run_args:
            print('Nothing to run...')
            return OK
        print(f"Running: {' '.join(self.run_args)}")

        return self.run()

    def run(self):

        hp = HappyFlow()
        hp.target_methods(self.target_methods)
        hp.target_files(self.target_files)
        hp.ignore_files(self.ignore_files)

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
                self.handle_result(hp.result())
                # hp.html_report(directory)
                # hp.csv_report(directory)
                return OK
            return ERR

    def handle_result(self, result):
        spec = importlib.util.spec_from_file_location("spotflow_miner", "./mining_scripts/spotflow_miner.py")
        spotflow_mining = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(spotflow_mining)
        spotflow_mining.runtime_miner(result)


def main():
    try:
        status = HappyFlowScript().command_line()
    except Exception as e:
        print(e)
        status = ERR
    return status