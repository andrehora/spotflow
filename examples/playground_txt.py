from happyflow.target_loader import TargetEntityLoader
from happyflow.tracer import TraceRunner
from happyflow.txt_report import TextReport


# target = TargetEntityLoader.find('message._formatparam', 'email', 'message')
# trace_result = TraceRunner.trace_tests('test.test_email.test_email.TestMessageAPI', target)

target = TargetEntityLoader.find('encoder.JSONEncoder.iterencode', 'json', 'encoder')
trace_result = TraceRunner.trace_tests('test.test_json', target)

# target = TargetEntityLoader.find('csv.Sniffer.sniff', '.', 'csv')
# trace_result = TraceRunner.trace_tests('test.test_csv', target)

# target = TargetEntityLoader.find('gzip.GzipFile.close', '.', 'gzip')
# trace_result = TraceRunner.trace_tests('test.test_gzip', target)

# target = TargetEntityLoader.find('random.Random.vonmisesvariate', '.', 'random')
# trace_result = TraceRunner.trace_tests('test.test_random', target)

# target = TargetEntityLoader.find('request.request_host', 'urllib', 'request')
# trace_result = TraceRunner.trace_tests('test.test_urllib', None)

# flow_results = target.local_flows(trace_result)
# report = TextReport(target, flow_results[0])
# report.show_code_state(state_summary=True)


