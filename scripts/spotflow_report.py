from scripts import basics, exceptions, returns, arguments, polarity


def process(monitored_system):

    polarity.test_calls_that_return_true_or_false(monitored_system)

    # basics.monitored_methods_overview(monitored_system)
    # exceptions.thrown_exceptions(monitored_system)
    # returns.calls_that_return_value(monitored_system)
    # arguments.argument_values_and_types(monitored_system)

    # methods = monitored_system.all_methods()
    # sorted_methods = sorted(methods, key=lambda mth: len(mth.calls), reverse=True)
    #
    # print(f'========= Most called methods (total: {len(methods)}) =========')
    # print('rank, method_name, number_of_calls')
    # count = 0
    # for method in sorted_methods:
    #     count += 1
    #     print(f'{count}, {method.full_name}, {len(method.calls)}')
