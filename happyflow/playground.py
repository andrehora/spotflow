from happyflow.target_loader import TargetEntityLoader
from happyflow.tracer import TraceRunner
from happyflow.txt_report import TextReport


def live_func(source_func, target_func):

    target = TargetEntityLoader.load_func(target_func)
    trace_result = TraceRunner.trace_funcs(source_func, target)

    flow_results = target.local_flows(trace_result)

    for flow_result in flow_results:
        report = TextReport(flow_result.target_entity, flow_result)
        report.show_most_common_args_and_return_values(3, show_code=True)



