from collections import Counter


def argument_values_for_specific_type(monitored_system, type):
    int_values = []
    str_values = []
    for call in monitored_system.all_calls():
        call_state = call.call_state
        for arg in call_state.arg_states:
            if arg.type == type:
                str_values.append(arg.value)

    most_common_int_values = Counter(int_values).most_common()
    most_common_str_values = Counter(str_values).most_common()
    print(most_common_int_values)
    print(most_common_str_values)


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