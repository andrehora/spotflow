import argparse
from happyflow.api import HappyFlow
from happyflow.libs.execfile import PyRunner

OK, ERR = 0, 1

parser = argparse.ArgumentParser(description='Command line for HappyFlow')
parser.add_argument('--dir', type=str, help='Write the output files to dir')
parser.add_argument('target', type=str, nargs='+', help='One or more target entities')
parser.add_argument('--run',  type=str, nargs='+', help='Command line to be run')
args = parser.parse_args()


class HappyFlowScript:

    def command_line(self):

        directory = args.dir
        target_entitie_names = args.target
        run_args = args.run
        if directory:
            print(f"Dir: {directory}")
        print(f"Target: {' '.join(target_entitie_names)}")
        print(f"Run: {' '.join(run_args)}")

        # return self.run(target_entitie_names, run_args)

    def run(self, target_entitie_names, run_args):

        flow = HappyFlow()
        flow.target_entities(target_entitie_names)

        runner = PyRunner(run_args, as_module=True)
        runner.prepare()

        flow.start()
        code_ran = True
        try:
            # Run the command line
            runner.run()
        except Exception:
            code_ran = False
            return ERR
        finally:
            flow.stop()
            if code_ran:
                flow.html_report()
        return OK


def main():
    try:
        status = HappyFlowScript().command_line()
    except Exception as e:
        print(e)
        status = ERR
    return status