from collections import Counter
from happyflow.api import monitor_unittest_module


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


def argument_values_and_types(monitored_system):
    arg_values = []
    arg_types = []
    for call in monitored_system.all_calls():
        call_state = call.call_state
        for arg in call_state.arg_states:
            arg_values.append(arg.value)
            arg_types.append(arg.type)

    most_common_values = Counter(arg_values).most_common()
    most_common_types = Counter(arg_types).most_common()
    print(most_common_values)
    print(most_common_types)


def main():
    from test import test_gzip

    monitored_system = monitor_unittest_module(test_gzip, 'gzip')
    calls_that_return_true_or_false(monitored_system)


main()