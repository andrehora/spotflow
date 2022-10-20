from collections import Counter


def thrown_exceptions(monitored_system):

    print('thrown_exceptions')

    exceptions = []
    for call in monitored_system.all_calls():
        call_state = call.call_state
        if call_state.has_exception():
            exceptions.append(call_state.exception_state.value)

    most_common = Counter(exceptions).most_common()
    print(most_common)
