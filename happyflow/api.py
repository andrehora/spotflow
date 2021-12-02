from happyflow.report import Report
from happyflow.collector import Collector


class HappyFlow:

    def __init__(self):
        self.collector = Collector()

    def target_entities(self, target_entities):
        self.collector.target_entity_names = target_entities

    def ignore_files(self, ignore):
        self.collector.ignore = ignore

    def start(self):
        self.collector.start()

    def stop(self):
        self.collector.stop()

    def result(self):
        return self.collector.flow_result

    def html_report(self, directory=None):
        try:
            Report(self.collector.flow_result).html_report(directory)
        except Exception as e:
            print(e)

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


def run_and_flow_func(func, target_entities):
    flow = HappyFlow()
    flow.target_entities(target_entities)
    flow.start()

    func()

    flow.stop()
    return flow.result()


