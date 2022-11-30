

def method_metrics(monitored_program, save_dir):

    sorted_methods = sorted(monitored_program.all_methods(), key=lambda mth: len(mth.calls), reverse=True)

    print('rank, method_name, calls, exceptions')
    count = 0
    for method in sorted_methods:
        count += 1
        print(f'{count}, {method.full_name}, {len(method.calls)}, {len(method.exception_states())}')

