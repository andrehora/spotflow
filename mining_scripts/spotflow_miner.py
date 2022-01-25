from mining_scripts.polarity import calls_that_return_true_or_false


def runtime_miner(monitored_system):

    calls_that_return_true_or_false(monitored_system)

    # methods = monitored_system.all_methods()
    # print('================= Simple report =================')
    # for method in methods:
    #     print(method.full_name, len(method.calls))
