from happyflow.tracer import TraceRunner
from happyflow.report import Report
from happyflow.target_model import TargetEntity


def trace_from_func(source_func, target_func, report_format):
    target = TargetEntity.build_from_func(target_func)
    trace_result = TraceRunner.trace_from_func(source_func, target)
    export_report(trace_result, report_format)


def trace_from_test_class(test_class, target_names, report_format):
    trace_result = TraceRunner.trace_from_test_class(test_class, target_names)
    export_report(trace_result, report_format)


def trace_from_test_module(module, target_names, report_format):
    trace_result = TraceRunner.trace_from_test_module(module, target_names)
    export_report(trace_result, report_format)


def trace_pytests():
    pass


def export_report(trace_result, report_format):
    if report_format == 'html':
        Report.export_html(trace_result)
    elif report_format == 'txt':
        Report.export_txt(trace_result)





