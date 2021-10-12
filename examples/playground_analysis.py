from happyflow.target_loader import TargetEntityLoader
from happyflow.tracer import TraceRunner
from happyflow.txt_report import TextReport


def count_uppercase_words(text):
    counter = 0
    for word in text.split():
        if word.isupper():
            counter += 1
    return counter


def _parseparam(s):
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


def _splitparam(param):
    a, sep, b = str(param).partition(';')
    if not sep:
        return a.strip(), None
    return a.strip(), b.strip()


# def source():
    # foo()
    # count_uppercase_words('a b')
    # count_uppercase_words('A B')
    # count_uppercase_words('A B')
    # count_uppercase_words('A B C')
    # count_uppercase_words('A B C')
    # count_uppercase_words('A B C')
    # count_uppercase_words('A B C')
    # _parseparam('a="1;b=1"')
    # _splitparam("a;b")


# target = TargetEntityLoader.load_func(bar)
# trace_result = TraceRunner.trace_funcs(source, target)

# target = TargetEntityLoader.find('message._parseparam', 'email', 'message')
# trace_result, target = TraceRunner.trace_suite('test.test_email.test_email.TestMessageAPI', ['message._parseparam'])

# target = TargetEntityLoader.find('csv.Sniffer.has_header', '.', 'csv')
# trace_result = TraceRunner.trace_suite('test.test_csv', None)

# target = TargetEntityLoader.find('gzip.GzipFile', '.', 'gzip')
# trace_result = TraceRunner.trace_suite('test.test_gzip', None)

# target = TargetEntityLoader.find('tarfile.nti', '.', 'tarfile')
# trace_result, target = TraceRunner.trace_suite('test.test_os', ['os.get_exec_path'])

trace_result, target = TraceRunner.trace_suite('tests', ['url.url_is_from_any_domain'])


flow_results = target.local_flows(trace_result)

for flow_result in flow_results:
    report = TextReport(flow_result.target_entity, flow_result)
    report.show_most_common_args_and_return_values(3, show_code=True)
