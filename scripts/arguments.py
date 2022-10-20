from collections import Counter


def argument_values_for_specific_type(monitored_system, target_type):

    print('argument_values_for_specific_type')

    type_values = []
    for call in monitored_system.all_calls():
        call_state = call.call_state
        for arg in call_state.arg_states:
            if arg.type == target_type:
                type_values.append(arg.value)

    most_common_str_values = Counter(type_values).most_common()
    print(most_common_str_values)


def argument_values_and_types(monitored_system):

    print('argument_values_and_types')

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
