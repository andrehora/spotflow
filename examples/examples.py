from collections import Counter
from happyflow.api import run
from happyflow.unittest_utils import loadTestsFromModule, suite_runner


def called_methods():

    from test import test_gzip
    suite = loadTestsFromModule(test_gzip)
    suite = suite_runner(suite)
    result = run(suite, ['gzip'])

    print(len(result.all_methods()))
    print(len(result.all_calls()))
    print(result.all_methods())


def tests_that_execute_specific_method():

    from test import test_gzip
    suite = loadTestsFromModule(test_gzip)
    suite = suite_runner(suite)
    result = run(suite, ['gzip._PaddedFile.read'])

    tests = set()
    for call in result.all_calls():
        for caller in call.call_stack:
            if caller.startswith('test'):
                tests.add(caller)

    print(len(tests))
    print(tests)


def methods_executed_by_specific_test():

    from test import test_gzip
    suite = loadTestsFromModule(test_gzip)
    suite = suite_runner(suite)
    result = run(suite, ['gzip'])

    methods = set()
    for call in result.all_calls():
        for caller in call.call_stack:
            if caller == 'test.test_gzip.TestGzip.test_zero_padded_file':
                methods.add(call.monitored_method.method_name)

    print(len(methods))
    print(methods)


def thrown_exceptions():

    from test import test_gzip
    suite = loadTestsFromModule(test_gzip)
    suite = suite_runner(suite)
    result = run(suite, ['gzip'])

    exceptions = []
    for call in result.all_calls():
        call_state = call.call_state
        if call_state.has_exception():
            exceptions.append(call_state.exception_state.value)

    most_common = Counter(exceptions).most_common()
    print(most_common)


def methods_that_return_value():

    from test import test_gzip
    suite = loadTestsFromModule(test_gzip)
    suite = suite_runner(suite)
    result = run(suite, ['gzip'])

    has_return = []
    for call in result.all_calls():
        call_state = call.call_state
        if call_state.has_return():
            has_return.append(True)

    print(len(has_return))


def methods_that_return_specific_value():

    from test import test_gzip
    suite = loadTestsFromModule(test_gzip)
    suite = suite_runner(suite)
    result = run(suite, ['gzip'])

    return_values = []
    for call in result.all_calls():
        call_state = call.call_state
        if call_state.has_return():
            return_state = call_state.return_state
            if return_state.value == 'True' or return_state.value == 'False':
                return_values.append(return_state.value)

    most_common = Counter(return_values).most_common()
    print(most_common)


def main():
    # called_methods()

    # tests_that_execute_specific_method()
    # methods_executed_by_specific_test()

    # thrown_exceptions()

    methods_that_return_value()
    methods_that_return_specific_value()

main()