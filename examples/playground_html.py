from happyflow.tracer import TraceRunner
from happyflow.html_report import HTMLReport


trace_result, target = TraceRunner.trace_suite('test.test_email.test_email.TestMessageAPI', ['message._parseparam'])
flow_results = target.local_flows(trace_result)

for flow_result in flow_results:
    reporter = HTMLReport(flow_result.target_entity, flow_result)
    reporter.show_code(0)

