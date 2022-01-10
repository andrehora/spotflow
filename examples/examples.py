from collections import Counter
from happyflow.api import run_and_monitor
from happyflow.unittest_utils import loadTestsFromModule, suite_runner


def load_module_and_run(module):
    suite = loadTestsFromModule(module)
    suite = suite_runner(suite)
    return run_and_monitor(suite, ['gzip'])


def called_methods(monitored_system):

    print(len(monitored_system.all_methods()))
    print(len(monitored_system.all_calls()))
    print(monitored_system.all_methods())


def tests_that_execute_specific_method(monitored_system):

    method = monitored_system['gzip._PaddedFile.read']

    tests = set()
    for call in method.calls:
        for caller in call.call_stack:
            if caller.startswith('test'):
                tests.add(caller)

    print(len(tests))
    print(tests)


def methods_executed_by_specific_test(monitored_system):

    methods = set()
    for call in monitored_system.all_calls():
        for caller in call.call_stack:
            if caller == 'test.test_gzip.TestGzip.test_zero_padded_file':
                methods.add(call.monitored_method.method_name)

    print(len(methods))
    print(methods)


def thrown_exceptions(monitored_system):

    exceptions = []
    for call in monitored_system.all_calls():
        call_state = call.call_state
        if call_state.has_exception():
            exceptions.append(call_state.exception_state.value)

    most_common = Counter(exceptions).most_common()
    print(most_common)


def calls_that_return_value(monitored_system):

    counter = 0
    for call in monitored_system.all_calls():
        call_state = call.call_state
        if call_state.has_return():
            counter += 1

    print(counter)


def calls_that_return_specific_value(monitored_system):

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


def argument_values_for_specific_type(monitored_system):
    int_values = []
    str_values = []
    for call in monitored_system.all_calls():
        call_state = call.call_state
        for arg in call_state.arg_states:
            if arg.type == 'int':
                int_values.append(arg.value)
            if arg.type == 'str':
                str_values.append(arg.value)

    most_common_int_values = Counter(int_values).most_common()
    most_common_str_values = Counter(str_values).most_common()
    print(most_common_int_values)
    print(most_common_str_values)


def main():
    from test import test_gzip, test_os
    monitored_system = load_module_and_run(test_gzip)

    # called_methods(monitored_system)
    #
    # tests_that_execute_specific_method(monitored_system)
    # methods_executed_by_specific_test(monitored_system)
    #
    # thrown_exceptions(monitored_system)
    #
    # calls_that_return_value(monitored_system)
    # calls_that_return_specific_value(monitored_system)

    # argument_values_and_types(monitored_system)
    argument_values_for_specific_type(monitored_system)



main()