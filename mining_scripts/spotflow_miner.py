from mining_scripts import basics, exceptions, returns, arguments


def runtime_miner(monitored_system):

    basics.monitored_methods_overview(monitored_system)
    exceptions.thrown_exceptions(monitored_system)
    returns.calls_that_return_value(monitored_system)
    arguments.argument_values_and_types(monitored_system)

    # methods = monitored_system.all_methods()
    # print('================= Simple report =================')
    # for method in methods:
    #     print(method.full_name, len(method.calls))
