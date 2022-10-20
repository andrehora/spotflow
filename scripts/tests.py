def tests_that_execute_specific_method(monitored_system, method_name):

    print('tests_that_execute_specific_method')

    method = monitored_system[method_name]
    tests = set()
    for call in method.calls:
        for caller in call.call_stack:
            if caller.startswith('test'):
                tests.add(caller)

    print(len(tests))
    print(tests)


def methods_executed_by_specific_test(monitored_system, test_name):

    print('methods_executed_by_specific_test')

    methods = set()
    for call in monitored_system.all_calls():
        for caller in call.call_stack:
            if caller == test_name:
                methods.add(call.monitored_method.name)

    print(len(methods))
    print(methods)


def methods_executed_by_specific_test2(monitored_system, test_name):

    print(test_name)

    methods = []
    cont = 0
    for call in monitored_system.all_calls():
        if test_name in call.call_stack:
            # if call.call_state.return_boolean():

            method_call = call.monitored_method
            # value = call.call_state.return_state.value

            cont += 1
            print(cont, method_call.full_name)
            if call.call_state.arg_states:
                for arg in call.call_state.arg_states:
                    print(arg)
            # methods.append(call.monitored_method.full_name)

    # print(len(methods))
    # print(methods)
