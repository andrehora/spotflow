# from happyflow.tracer import TraceRunner, PyTracer
from happyflow.report import Report
from happyflow.target import TargetEntity
from happyflow.collector import Collector


class HappyFlow:

    def __init__(self):
        self._collector = Collector()

    def target_entities(self, target_entities):
        self._collector.target_entity_names = target_entities

    def start(self):
        self._collector.start()

    def stop(self):
        self._collector.stop()

    def result(self):
        return self._collector.trace_result

    def html_report(self, directory='report'):
        try:
            Report(self._collector.trace_result).html_report(directory)
            return True
        except Exception as e:
            print(e)
            return False

    def txt_report(self):
        try:
            Report(self._collector.trace_result).txt_report()
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



# def trace_from_func(source_func, target_func, report_format):
#     target = TargetEntity.build_from_func(target_func)
#     trace_result = TraceRunner.trace_from_func(source_func, target)
#     return export_report(trace_result, report_format)
#
#
# def trace_from_test_class(test_class, target_names, report_format, report_dir=None):
#     trace_result = TraceRunner.trace_from_test_class(test_class, target_names)
#     return export_report(trace_result, report_format, report_dir)
#
#
# def trace_from_test_module(module, target_names, report_format, report_dir=None):
#     trace_result = TraceRunner.trace_from_test_module(module, target_names)
#     return export_report(trace_result, report_format, report_dir)
#
#
# def trace_pytests():
#     pass
#
#
# def export_report(trace_result, report_format, report_dir=None):
#     try:
#         if report_format == 'html':
#             Report(trace_result).html(report_dir)
#         elif report_format == 'txt':
#             Report.export_txt(trace_result)
#         return True
#     except Exception as e:
#         print(e)
#         return False





