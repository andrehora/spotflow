import argparse
from happyflow.api import HappyFlow
from happyflow.libs.execfile import PyRunner

OK, ERR = 0, 1

parser = argparse.ArgumentParser(description='Command line for HappyFlow')
parser.add_argument('-d', '--dir', type=str, help='Write the output files to dir')
parser.add_argument('-t', '--target', type=str, action='append', help='One or more target entities')
parser.add_argument('-i', '--ignore', type=str, action='append', help='One or more target entities')
parser.add_argument('run',  type=str, nargs=argparse.REMAINDER, help='Command line to run, for example: pytest tests')
args = parser.parse_args()


class HappyFlowScript:

    def command_line(self):

        run_args = args.run
        directory = args.dir
        target_entities = args.target
        ignore_files = args.ignore

        if not run_args:
            print('Nothing to run...')
            return OK

        print(f"Running: {' '.join(run_args)}")
        return self.run(run_args, directory, target_entities, ignore_files)

    def run(self, run_args, directory=None, target_entities=None, ignore_files=None):

        flow = HappyFlow()
        flow.target_entities(target_entities)
        flow.ignore_files(ignore_files)

        runner = PyRunner(run_args, as_module=True)
        runner.prepare()

        flow.start()
        code_ran = True
        try:
            # Run the command line
            runner.run()
        except Exception as e:
            print(e)
            code_ran = False
            return ERR
        finally:
            flow.stop()
            if code_ran:
                flow.html_report(directory)
        return OK


def main():
    try:
        status = HappyFlowScript().command_line()
    except Exception as e:
        print(e)
        status = ERR
    return status