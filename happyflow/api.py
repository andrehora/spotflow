from happyflow.report import Report
from happyflow.collector import Collector
from happyflow.unittest_utils import loadTestsFromModule, suite_runner


class HappyFlow:

    def __init__(self):
        self.collector = Collector()

    def target_methods(self, method_names):
        self.collector.method_names = method_names

    def ignore_files(self, ignore_files):
        self.collector.ignore_files = ignore_files

    def start(self):
        self.collector.start()

    def stop(self):
        self.collector.stop()

    def result(self):
        return self.collector.monitored_system

    def html_report(self, directory=None):
        # try:
        Report(self.collector.monitored_system).html_report(directory)
        # except Exception as e:
        #     print(e)

    def csv_report(self, directory=None):
        # try:
        Report(self.collector.monitored_system).csv_report(directory)
        # except Exception as e:
        #     print(e)

    def txt_report(self):
        try:
            Report(self.collector.monitored_system).txt_report()
            return True
        except Exception as e:
            print(e)
            return False


def monitor(func, target_methods=None):
    hp = HappyFlow()
    hp.target_methods(target_methods)
    hp.start()

    func()

    hp.stop()
    return hp.result()


def live(func, target_methods):
    hp = HappyFlow()
    hp.target_methods(target_methods)
    hp.start()

    func()

    hp.stop()
    hp.txt_report()


def monitor_unittest_module(module, target):
    suite = loadTestsFromModule(module)
    suite = suite_runner(suite)
    return monitor(suite, [target])


