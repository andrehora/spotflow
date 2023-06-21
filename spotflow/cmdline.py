import argparse
import configparser
import importlib.util
from spotflow.report import html_report
from spotflow.api import SpotFlow
from coverage.cmdline import PyRunner

OK, ERR = 0, 1


def parse_args(args=None):
    parser = argparse.ArgumentParser(description="Command line for SpotFlow")

    parser.add_argument(
        "-o", "--objects", action="store_true", help="Print summary of objects."
    )

    parser.add_argument(
        "-c", "--calls", action="store_true", help="Print summary of calls"
    )

    parser.add_argument(
        "-p", "--pprint", action="store_true", help="Pretty print code."
    )

    parser.add_argument(
        "-html", "--html", action="store_true", help="HTML report."
    )

    parser.add_argument(
        "-s",
        "--script",
        type=str,
        nargs="?",
        const="spotflow_script.py",
        help="Python script to be run after monitoring the program."
        'Default is "spotflow_script.py".',
    )

    parser.add_argument(
        "-arg",
        "--script-argument",
        type=str,
        action="append",
        help="Arguments that are passed to the script. Accept multiple arguments.",
    )

    parser.add_argument(
        "-t",
        "--target-method",
        type=str,
        action="append",
        help="Target method full name (in the format module.Class.method) or prefix. "
        'For example, "parser.StringParser.count" or simply "parse". '
        "To monitor multiple methods, use multiple arguments, like -t name1 -t name2 -t ...",
    )

    parser.add_argument(
        "-tt",
        "--target-method-name",
        type=str,
        action="append",
        help="Target method name. "
        "To monitor multiple methods, use multiple arguments, like -tt name1 -tt name2 -tt ...",
    )

    parser.add_argument(
        "-f",
        "--target-file",
        type=str,
        action="append",
        help="Target file. It can be a substring of the file full path. "
        'For example, "path/to/my_program.py" or simply "my_program". '
        "To monitor multiple files, use multiple arguments, like -f file1 -f file2 -f ...",
    )

    parser.add_argument(
        "-i",
        "--ignore-file",
        type=str,
        action="append",
        help="File to ignore. It can be a substring of the file full path. "
        "To ignore multiple files, use multiple arguments, like -i file1 -i file2 -i ...",
    )

    parser.add_argument(
        "run",
        type=str,
        nargs=argparse.REMAINDER,
        help="Command line to run, for example: "
        '"my_program.py", "pytest tests", "unittest discover", etc.'
        "This should be the last argument of command line.",
    )

    return parser.parse_args(args)


class SpotFlowCommandLine:
    def __init__(self, args=None):
        parsed_args = parse_args(args)

        self.objects = parsed_args.objects
        self.calls = parsed_args.calls
        self.pprint = parsed_args.pprint
        self.html = parsed_args.html

        self.script = parsed_args.script
        self.script_args = parsed_args.script_argument

        self.target_methods = parsed_args.target_method
        self.target_method_names = parsed_args.target_method_name

        self.target_files = parsed_args.target_file
        self.ignore_files = parsed_args.ignore_file

        self.run_args = parsed_args.run

    def run(self):
        if not self.run_args:
            print("Nothing to run...")
            return OK

        print(f"Running and monitoring: {' '.join(self.run_args)}")
        return self.py_run()

    def py_run(self):
        flow = SpotFlow()
        flow.target_methods(self.target_methods)
        flow.target_method_names(self.target_method_names)
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
            code_ran = False
        finally:
            flow.stop()
            if code_ran:
                self.run_action_or_script(flow)
                return OK
            return ERR

    def parse_config(self):
        config = configparser.ConfigParser()
        has_config = config.read("./spotflow.cfg")
        if has_config:
            if "state" not in config:
                return None

            state = config["state"]
            arg_states = state.getboolean("arg_states")
            return_states = state.getboolean("return_state")
            yield_states = state.getboolean("yield_states")
            exception_states = state.getboolean("exception_states")
            var_states = state.getboolean("var_states")

            states = (arg_states, return_states, yield_states, exception_states, var_states)

            return states

    def run_action_or_script(self, flow):
        if self.script:
            self.run_script(flow.result())
        else:
            self.run_action(flow.result())

    def run_action(self, result):
        if self.objects:
            result.show_summary()

        if self.calls:
            result.show_calls()

        if self.pprint:
            result.show_pprint()

        if self.html:
            html_report(result)

    def run_script(self, result):
        pyscript = self.script
        if not pyscript.endswith(".py"):
            pyscript = pyscript + ".py"

        if not self.script_args:
            self.script_args = []

        spec = importlib.util.spec_from_file_location(".", pyscript)
        pyscript_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(pyscript_module)
        pyscript_module.spotflow_after(result, *self.script_args)


def main():
    try:
        status = SpotFlowCommandLine().run()
    except Exception as e:
        print(e)
        status = ERR
    return status
