from happyflow.report import Report
from happyflow.collector import Collector


class HappyFlow:

    def __init__(self):
        self.collector = Collector()

    def target_methods(self, target_method_names):
        self.collector.target_method_names = target_method_names

    def ignore_files(self, ignore):
        self.collector.ignore = ignore

    def start(self):
        self.collector.start()

    def stop(self):
        self.collector.stop()

    def result(self):
        return self.collector.flow_result

    def html_report(self, directory=None):
        # try:
        Report(self.collector.flow_result).html_report(directory)
        # except Exception as e:
        #     print(e)

    def csv_report(self, directory=None):
        # try:
        Report(self.collector.flow_result).csv_report(directory)
        # except Exception as e:
        #     print(e)

    def txt_report(self):
        try:
            Report(self.collector.flow_result).txt_report()
            return True
        except Exception as e:
            print(e)
            return False


def run_and_flow_func(func, target_methods):
    flow = HappyFlow()
    flow.target_methods(target_methods)
    flow.start()

    func()

    flow.stop()
    return flow.result()


def live(func, target_methods):
    flow = HappyFlow()
    flow.target_methods(target_methods)
    flow.start()

    func()

    flow.stop()
    flow.txt_report()


