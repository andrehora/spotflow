from happyflow.tracer import TraceRunner
from happyflow.target_loader import TargetEntityLoader
from happyflow.report import Report


def count_uppercase_words(text):
    counter = 0
    for word in text.split():
        if word.isupper():
            counter += 1
    return counter


def parseparam(s):
    s = ';' + str(s)
    plist = []
    while s[:1] == ';':
        s = s[1:]
        end = s.find(';')
        while end > 0 and (s.count('"', 0, end) - s.count('\\"', 0, end)) % 2:
            end = s.find(';', end + 1)
        if end < 0:
            end = len(s)
        f = s[:end]
        if '=' in f:
            i = f.index('=')
            f = f[:i].strip().lower() + '=' + f[i+1:].strip()
        plist.append(f.strip())
        s = s[end:]
    return plist


def inputs_count():
    count_uppercase_words('')
    count_uppercase_words('a')
    count_uppercase_words('A')
    count_uppercase_words('A B C')


def inputs_parseparam():
    parseparam('a')
    parseparam('a=1;b=2')
    parseparam('a="1;1"')


# target = TargetEntityLoader.load_func(count_uppercase_words)
# trace_result = TraceRunner.trace_from_func(inputs_count, target)
# flow_results = target.local_flows(trace_result)

# from test import test_gzip
# trace_result, target = TraceRunner.trace_from_test_module(test_gzip, ['gzip'])
# flow_results = target.local_flows(trace_result)

from test.test_email.test_email import TestMessageAPI
trace_result, target = TraceRunner.trace_from_test_class(TestMessageAPI, ['message'])
flow_results = target.local_flows(trace_result)


for flow_result in flow_results:
    print(flow_result.target_entity.full_name())
    reporter = Report(flow_result.target_entity, flow_result)
    reporter.html_report()
