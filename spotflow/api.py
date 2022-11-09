from spotflow.report import Report
from spotflow.collector import Collector
from spotflow.utils_unittest import loadTestsFromModule, loadTestsFromTestCase, suite_runner


class SpotFlow:

    def __init__(self):
        self.collector = Collector()

    def target_methods(self, method_names):
        self.collector.method_names = method_names

    def target_files(self, file_names):
        self.collector.file_names = file_names

    def ignore_files(self, ignore_files):
        self.collector.ignore_files = ignore_files

    def collect_states(self, arg_states=True, return_states=True, yield_states=True,
                       exception_states=True, var_states=True):

        self.collector.collect_arg_states = arg_states
        self.collector.collect_return_states = return_states
        self.collector.collect_yield_states = yield_states
        self.collector.collect_exception_states = exception_states
        self.collector.collect_var_states = var_states

    def start(self):
        self.collector.start()

    def stop(self):
        self.collector.stop()

    def result(self):
        return self.collector.monitored_program

    def html_report(self, directory=None):
        try:
            Report(self.result()).html_report(directory)
        except Exception as e:
            print(e)

    def csv_report(self, directory=None):
        try:
            Report(self.result()).csv_report(directory)
        except Exception as e:
            print(e)

    def pprint_report(self):
        try:
            Report(self.collector.monitored_program).pprint_report()
            return True
        except Exception as e:
            print(e)
            return False


def pprint(func, target_methods):
    flow = SpotFlow()
    flow.target_methods(target_methods)

    flow.start()
    func()
    flow.stop()

    return flow.pprint_report()


def monitor(func, target_methods=None, target_files=None, ignore_files=None,
            arg_states=True, return_states=True, yield_states=True, exception_states=True, var_states=True):
    flow = SpotFlow()
    flow.target_methods(target_methods)
    flow.target_files(target_files)
    flow.ignore_files(ignore_files)
    flow.collect_states(arg_states, return_states, yield_states, exception_states, var_states)

    flow.start()
    func()
    flow.stop()

    return flow.result()


def monitor_unittest_module(module, target_methods=None, target_files=None, ignore_files=None,
            arg_states=True, return_states=True, yield_states=True, exception_states=True, var_states=True):

    suite = loadTestsFromModule(module)
    suite = suite_runner(suite)

    return monitor(suite, target_methods, target_files, ignore_files,
                   arg_states, return_states, yield_states, exception_states, var_states)


def monitor_unittest_testcase(test_case, target_methods=None, target_files=None, ignore_files=None,
            arg_states=True, return_states=True, yield_states=True, exception_states=True, var_states=True):

    suite = loadTestsFromTestCase(test_case)
    suite = suite_runner(suite)

    return monitor(suite, target_methods, target_files, ignore_files,
                   arg_states, return_states, yield_states, exception_states, var_states)
