from happyflow.tracer import TraceRunner
from happyflow.report_txt import TextReport

# trace_result, target = TraceRunner.trace_suite("tests", ['url.url_is_from_any_domain'])
trace_result, target = TraceRunner.trace_pytests("tests/test_color.py", ['color.Color.downgrade'])

print(target.target_entities)
flow_results = target.local_flows(trace_result)

for flow_result in flow_results:
    report = TextReport(flow_result.target_entity, flow_result)
    report.show_most_common_args_and_return_values(3, show_code=True)

