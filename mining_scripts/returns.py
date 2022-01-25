from collections import Counter


def calls_that_return_value(monitored_system):

    counter = 0
    for call in monitored_system.all_calls():
        call_state = call.call_state
        if call_state.has_return():
            counter += 1

    print(counter)


def calls_that_return_true_or_false(monitored_system):

    return_values = []
    for call in monitored_system.all_calls():
        call_state = call.call_state
        if call_state.has_return():
            return_state = call_state.return_state
            if return_state.value == 'True' or return_state.value == 'False':
                return_values.append(return_state.value)

    most_common = Counter(return_values).most_common()
    print(most_common)