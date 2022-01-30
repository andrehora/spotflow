from collections import Counter


def method_calls_that_return_true_or_false(monitored_system):

    print('method_calls_that_return_true_or_false')

    methods = []
    method_values = {}
    return_values = []
    for call in monitored_system.all_calls():
        call_state = call.call_state
        if call_state.has_return():
            return_state = call_state.return_state
            if return_state.value == 'True' or return_state.value == 'False':

                full_name = call.monitored_method.info.full_name
                methods.append(full_name)

                method_values[full_name] = method_values.get(full_name, [])
                method_values[full_name].append(return_state.value)

                return_values.append(return_state.value)

    most_common_method = Counter(methods).most_common()
    most_common_return_values = Counter(return_values).most_common()

    print('Methods:', len(most_common_method))
    print(most_common_return_values)
    print(most_common_method)
    for method in method_values:
        counter = Counter(method_values[method]).most_common()
        tf = sorted(counter, reverse=True)
        if len(tf) == 1:
            element = tf[0]
            if element[0] == 'True':
                print(method, element[1], 0)
            if element[0] == 'False':
                print(method, 0, element[1])
        if len(tf) == 2:
            print(method, tf[0][1], tf[1][1])


def test_calls_that_return_true_or_false(monitored_system):

    print('test_calls_that_return_true_or_false')

    tests = []
    method_values = {}
    return_values = []
    for call in monitored_system.all_calls():
        call_state = call.call_state
        if call_state.has_return():
            return_state = call_state.return_state
            if return_state.value == 'True' or return_state.value == 'False':

                method_name = call.call_stack[0]
                tests.append(method_name)

                method_values[method_name] = method_values.get(method_name, [])
                method_values[method_name].append(return_state.value)

                return_values.append(return_state.value)

    most_common_tests = Counter(tests).most_common()
    most_common_return_values = Counter(return_values).most_common()

    print('Tests:', len(most_common_tests))
    print(most_common_return_values)
    print(most_common_tests)
    for method in method_values:
        counter = Counter(method_values[method]).most_common()
        tf = sorted(counter, reverse=True)
        if len(tf) == 1:
            element = tf[0]
            if element[0] == 'True':
                print(method, element[1], 0)
            if element[0] == 'False':
                print(method, 0, element[1])
        if len(tf) == 2:
            print(method, tf[0][1], tf[1][1])
