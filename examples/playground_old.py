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


def count_uppercase_words(text):
    counter = 0
    for word in text.split():
        if word.isupper():
            counter += 1
    return counter


def hello(hour):
    if hour >= 12:
        if hour >= 18:
            return 'boa noite'
        return 'boa tarde'
    return 'bom dia'


def add_values(first, last):
    total = 0
    for each in range(first, last+1):
        total += each
    return total + 100


def change_list_state():
    a = []
    a.append(1)
    a.append(2)
    a.append(3)
    a.append(4)
    return a


def add(a, n):
    a.append(n)


def _splitparam(param):
    a, sep, b = str(param).partition(';')
    if not sep:
        return a.strip(), None
    return a.strip(), b.strip()


def jaccard_similariy(setA, setB, alternativeUnion=False):
    if isinstance(setA, set) and isinstance(setB, set):

        intersection = len(setA.intersection(setB))

        if alternativeUnion:
            union = len(setA) + len(setB)
        else:
            union = len(setA.union(setB))

        return intersection / union

    if isinstance(setA, (list, tuple)) and isinstance(setB, (list, tuple)):

        intersection = [element for element in setA if element in setB]

        if alternativeUnion:
            union = len(setA) + len(setB)
        else:
            union = setA + [element for element in setB if element not in setA]

        return len(intersection) / len(union)


def sum(a, b):
    return a + b


def source():
    # sum(10, 15)
    # _parseparam('a=2;b=3')
    # count_uppercase_words('A B C')
    # hello(20)
    # add_values(5, 10)
    change_list_state()
    # _splitparam("a;b")
    # setA = {"a", "b", "c", "d", "e"}
    # setB = {"c", "d", "e", "f", "h", "i"}
    # jaccard_similariy(setA, setB)


target = TargetEntityLoader.load_func(change_list_state)
trace_result = TraceRunner.trace_funcs(source, target)
flow_result = target.local_flows(trace_result)

report = TextReport(target, flow_result)
report.show_code_state(state_summary=True)
# report.show_most_common_flow()
# print(len(flow_result.flows))

# for flow in flow_result.flows:
#     a = flow.state_result.vars['a']
#     for state in a.states:
#         print(state.line)