from happyflow.target_loader import TargetEntityLoader
from happyflow.tracer import TraceRunner
from happyflow.report_txt import TextReport


def trace_from_func(source_func, target_func):
    target = TargetEntityLoader.load_func(target_func)
    trace_result = TraceRunner.trace_from_func(source_func, target)
    _trace_and_show(trace_result, target)


def trace_from_test_class(test_class, target_names):
    trace_result, target = TraceRunner.trace_from_test_class(test_class, target_names)
    _trace_and_show(trace_result, target)


def trace_from_test_module(module, target_names):
    trace_result, target = TraceRunner.trace_from_test_module(module, target_names)
    _trace_and_show(trace_result, target)


def _trace_and_show(trace_result, target):
    flow_results = target.local_flows(trace_result)
    _show_results(flow_results)


def _show_results(flow_results):
    for flow_result in flow_results:
        report = TextReport(flow_result.target_entity, flow_result)
        report.show_most_common_args_and_return_values(3, show_code=True)



