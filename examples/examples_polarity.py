from collections import Counter
from happyflow.api import monitor_unittest_module


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


def calls_that_return_true_or_false(monitored_system):
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
        print(method, tf)


def monitor_test(test, target=None):
    print('Test suite:', test.__name__)
    monitored_system = monitor_unittest_module(test, target)
    calls_that_return_true_or_false(monitored_system)


def main():

    # from test import test_ast as test
    # monitor_test(test, ['ast'])

    from test import test_gzip as test
    monitor_test(test, ['gzip'])

    # from test import test_urlparse as test
    # monitor_test(test, ['urllib'])

    # from test import test_json as test
    # monitor_test(test, ['json'])

    # from test import test_calendar as test
    # monitor_test(test, ['calendar'])

    from test import test_collections as test
    monitor_test(test, ['collections'])

    # from test import test_csv as test
    # monitor_test(test, ['csv'])

    # from test import test_ftplib as test
    # monitor_test(test, ['ftplib'])
    #
    # from test import test_htmlparser as test
    # monitor_test(test, ['html'])

    from test import test_httplib as test
    monitor_test(test, ['http'])

    # from test import test_time as test
    # monitor_test(test, ['time'])
    #
    # from test import test_zlib as test
    # monitor_test(test, 'zlib')

    from test import test_zipfile as test
    monitor_test(test, ['zipfile'])

    # from test import test_types as test
    # monitor_test(test, ['types'])

    from test import test_tarfile as test
    monitor_test(test, ['tarfile'])

    from test import test_pathlib as test
    monitor_test(test, ['pathlib'])

    from test import test_email as test
    monitor_test(test, ['email'])

    # from test import test_os as test
    # monitor_test(test, ['os'])
    #
    # from test import test_math as test
    # monitor_test(test, ['math'])


# main()

from test import test_gzip as test
monitor_test(test, ['gzip', 'os'])
