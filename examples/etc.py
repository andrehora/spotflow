from happyflow.tracer import TraceRunner
from happyflow.target_loader import TargetEntityLoader
from happyflow.txt_report import TextReport


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


def zipp():
    l1 = [1, 2, 3]
    l2 = [4, 5, 6]
    for x, y in zip(l1, l2):
        x += 1
        y += 1


def count_uppercase_words(text):
    counter = 0
    for word in text.split():
        if word.isupper():
            counter += 1
    return counter


def inputs_parseparam():
    # parseparam('a')
    # parseparam('a=1;b=2;b=2;b=2')
    # parseparam('a=1;b=2;b=2;b=2')
    # parseparam('a=1;b=2;b=2;b=2')
    # parseparam('a="1;1"')
    count_uppercase_words('AAA')
    # count_uppercase_words('A B')
    # count_uppercase_words('A B C')
    # zipp()


target = TargetEntityLoader.load_func(count_uppercase_words)
trace_result = TraceRunner.trace_from_func(inputs_parseparam, target)
flow_results = target.local_flows(trace_result)

for flow_result in flow_results:

    reporter = TextReport(flow_result.target_entity, flow_result)
    reporter.show_code_state()

    entity_info = reporter.code_flows_and_states(0)
    for line_info in entity_info:
        print(line_info)

