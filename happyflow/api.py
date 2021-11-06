from happyflow.target_loader import TargetEntityLoader
from happyflow.tracer import TraceRunner
from happyflow.report_txt import TextReport
from happyflow.report import Report


def trace_from_func(source_func, target_func, report_format):
    target = TargetEntityLoader.load_func(target_func)
    trace_result = TraceRunner.trace_from_func(source_func, target)
    flow_results = target.local_flows(trace_result)
    export_report(flow_results, report_format)


def trace_from_test_class(test_class, target_names, report_format):
    trace_result, target = TraceRunner.trace_from_test_class(test_class, target_names)
    flow_results = target.local_flows(trace_result)
    export_report(flow_results, report_format)


def trace_from_test_module(module, target_names, report_format):
    trace_result, target = TraceRunner.trace_from_test_module(module, target_names)
    flow_results = target.local_flows(trace_result)
    export_report(flow_results, report_format)


def trace_pytests():
    pass


def export_report(flow_results, report_format='html'):
    if report_format == 'html':
        Report.export_html(flow_results)
    elif report_format == 'txt':
        Report.export_txt(flow_results)





