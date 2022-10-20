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
    test_bool_values = {}
    test_call_values = {}
    return_values = []
    # cont = 0
    for call in monitored_system.all_calls():
        call_state = call.call_state
        if call_state.has_return():
            return_state = call_state.return_state
            if return_state.value == 'True' or return_state.value == 'False':

                test_name = call.call_stack[0]
                tests.append(test_name)

                test_bool_values[test_name] = test_bool_values.get(test_name, [])
                test_bool_values[test_name].append(return_state.value)

                key = test_name, return_state.value
                call_name = call.monitored_method.info.full_name
                test_call_values[key] = test_call_values.get(key, set())
                # cont += 1
                test_call_values[key].add(call_name)
                # print(test_call_values[key])

                return_values.append(return_state.value)

    most_common_tests = Counter(tests).most_common()
    most_common_return_values = Counter(return_values).most_common()

    print('Tests:', len(most_common_tests))
    print(most_common_return_values)
    print(most_common_tests)
    for test_name in test_bool_values:

        counter = Counter(test_bool_values[test_name]).most_common()
        tf_values = sorted(counter, reverse=True)

        if len(tf_values) == 1:

            element = tf_values[0]

            bool_value = element[0]
            frequency = element[1]

            calls = []
            key = test_name, bool_value
            if key in test_call_values:
                calls = test_call_values[key]

            if element[0] == 'True':
                print(test_name, frequency, 0, list(calls))
                # print(test_name, frequency, 0)
            if element[0] == 'False':
                print(test_name, 0, frequency, list(calls))
                # print(test_name, 0, frequency)

        if len(tf_values) == 2:

            trues = tf_values[0]
            falses = tf_values[1]

            true_value = trues[0]
            true_freq = trues[1]

            false_value = falses[0]
            false_freq = falses[1]

            true_calls = []
            true_key = test_name, true_value
            if true_key in test_call_values:
                true_calls = test_call_values[true_key]

            false_calls = []
            false_key = test_name, false_value
            if false_key in test_call_values:
                false_calls = test_call_values[false_key]

            print('===================')
            print(test_name, true_freq, false_freq)
            print('TRUE')
            for t in true_calls:
                print(t)
            print('FALSE')
            for f in false_calls:
                print(f)
            print()


def test_calls_branch_values(monitored_system):

    print('test_calls_brach_values')

    tests = []
    method_values = {}
    return_values = []
    for call in monitored_system.all_calls():

        branch_values = call.branch_values()
        if branch_values:

            method_name = call.call_stack[0]
            tests.append(method_name)

            method_values[method_name] = method_values.get(method_name, [])
            method_values[method_name].extend(branch_values)

            return_values.extend(branch_values)

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


def for_test_methods(monitored_system):

    print('test_calls_branch_track_values')

    test_suite_data = monitored_system.compute_polarity(min_branch_frequency=99)

    # for each in branch_track_values:
    #     tf_values = branch_track_values[each]
    #     print(each, tf_values)

    to_export = []
    for test_name in test_suite_data:
        t, f, total_tf, positivity, negativity, exception_freq = test_suite_data[test_name]
        to_export.append([test_name, t, f, total_tf, positivity, negativity, exception_freq])
        print(test_name, t, f, total_tf, positivity, negativity, exception_freq)

    return to_export
