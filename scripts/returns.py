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
        cs = call.call_state
        if cs.has_return():
            return_state = cs.return_state
            if return_state.type == 'bool':
                return_values.append(return_state.value)

    most_common = Counter(return_values).most_common()
    print(most_common)


def calls_with_arg_and_return(monitored_system):

    print('calls_with_arg_and_return')

    counter = 0

    for call in monitored_system.all_calls():
        call_state = call.call_state
        if call_state.has_return() and call_state.has_argument():
            counter += 1

    print('all_methods', len(monitored_system.all_methods()))
    print('all_calls', len(monitored_system.all_calls()))
    print('calls_with_arg_and_return', counter)


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


def calls_with_primitive_types(monitored_system):

    print('calls_with_primitive_types')

    counter = 0
    counter_all_primitive = 0
    counter_primitive_returns = 0

    for call in monitored_system.all_calls():
        call_state = call.call_state
        if call_state.has_return() and call_state.has_argument():
            counter += 1

            if call_state.return_state.is_primitive():
                counter_primitive_returns += 1

                all_primitive_args = True
                for arg in call_state.arg_states:
                    if not arg.is_primitive():
                        all_primitive_args = False
                        break

                if all_primitive_args:
                    counter_all_primitive += 1
                    for arg in call_state.arg_states:
                        print(arg)
                    print(call_state.return_state)
                    print('======================')

    print('all_methods', len(monitored_system.all_methods()))
    print('all_calls', len(monitored_system.all_calls()))
    print('calls_with_arg_and_return', counter)
    print('counter_primitive_returns', counter_primitive_returns)
    print('counter_all_primitive', counter_all_primitive)


def calls_with_return_and_args(monitored_system):

    from spotflow.utils import write_txt
    import hashlib

    print('calls_with_return_and_args')

    counter = 0
    test_calls = 0
    internal_calls = 0

    for call in monitored_system.all_calls():
        call_state = call.call_state
        if call_state.has_return() and call_state.has_argument():
            counter += 1
            values = ""

            print(call.is_directly_called_from_test())
            if call.is_directly_called_from_test():
                test_calls += 1
            else:
                internal_calls += 1

            for arg in call_state.arg_states:
                values += arg.value + '\n'
            values += call_state.return_state.value + '\n'

            hash_id = hashlib.sha1(values.encode()).hexdigest()
            write_txt('hash38/' + str(hash_id) + '.txt', values)

            print(values)
            print(hash_id)
            print('======================')

    print('all_methods', len(monitored_system.all_methods()))
    print('all_calls', len(monitored_system.all_calls()))
    print('calls_with_return_and_args', counter)
    print('test calls', test_calls)
    print('internal calls', internal_calls)
