
def mine(monitored_program):

    methods = monitored_program.all_methods()
    sorted_methods = sorted(methods, key=lambda mth: len(mth.calls), reverse=True)
    print('rank, method_name, number_of_calls')
    count = 0
    for method in sorted_methods:
        count += 1
        print(f'{count}, {method.full_name}, {len(method.calls)}')
