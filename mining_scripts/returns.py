from collections import Counter


def calls_that_return_value(monitored_system):

    print('calls_that_return_value')

    counter = 0
    for call in monitored_system.all_calls():
        call_state = call.call_state
        if call_state.has_return():
            counter += 1

    print(counter)


def calls_that_return_true_or_false(monitored_system):

    print('calls_that_return_true_or_false')

    return_values = []
    for call in monitored_system.all_calls():
        call_state = call.call_state
        if call_state.has_return():
            return_state = call_state.return_state
            if return_state.value == 'True' or return_state.value == 'False':
                return_values.append(return_state.value)

    most_common = Counter(return_values).most_common()
    print(most_common)


def calls_that_with_arg_and_return(monitored_system):

    print('calls_that_with_arg_and_return')

    counter = 0

    for call in monitored_system.all_calls():
        call_state = call.call_state
        if call_state.has_return() and call_state.has_argument():
            counter += 1

    print('all_methods', len(monitored_system.all_methods()))
    print('all_calls', len(monitored_system.all_calls()))
    print('calls_that_with_arg_and_return', counter)


def return_and_arg_values_and_types(monitored_system):

    print('return_and_arg_values_and_types')

    arg_values = []
    arg_types = []
    return_values = []
    return_types = []

    for call in monitored_system.all_calls():
        call_state = call.call_state
        if call_state.has_return() and call_state.has_argument():

            for arg in call_state.arg_states:
                arg_values.append(arg.value)
                arg_types.append(arg.type)

            return_values.append(call_state.return_state.value)
            return_types.append(call_state.return_state.type)

    most_common_arg_values = Counter(arg_values).most_common()
    most_common_arg_types = Counter(arg_types).most_common()
    most_common_return_values = Counter(return_values).most_common()
    most_common_return_types = Counter(return_types).most_common()

    print(most_common_arg_values)
    print(most_common_arg_types)
    print(most_common_return_values)
    print(most_common_return_types)
