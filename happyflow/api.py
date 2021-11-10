from happyflow.tracer import TraceRunner
from happyflow.report import Report
from happyflow.target_model import TargetEntity


def trace_from_func(source_func, target_func, report_format):
    target = TargetEntity.build_from_func(target_func)
    trace_result = TraceRunner.trace_from_func(source_func, target)
    return export_report(trace_result, report_format)


def trace_from_test_class(test_class, target_names, report_format, report_dir=None):
    trace_result = TraceRunner.trace_from_test_class(test_class, target_names)
    return export_report(trace_result, report_format, report_dir)


def trace_from_test_module(module, target_names, report_format, report_dir=None):
    trace_result = TraceRunner.trace_from_test_module(module, target_names)
    return export_report(trace_result, report_format, report_dir)


def trace_pytests():
    pass


def export_report(trace_result, report_format, report_dir=None):
    try:
        if report_format == 'html':
            Report(trace_result).export_html(report_dir)
        elif report_format == 'txt':
            Report.export_txt(trace_result)
        return True
    except Exception as e:
        print(e)
        return False





