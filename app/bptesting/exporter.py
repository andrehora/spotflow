from spotflow.utils import write_txt
import hashlib


def export_calls_with_return_and_args(monitored_program, save_dir):

    counter = 0
    test_calls = 0
    internal_calls = 0

    for call in monitored_program.all_calls():
        call_state = call.call_state
        if call_state.has_return() and call_state.has_argument():
            counter += 1
            values = ""

            if call.is_directly_called_from_test():
                test_calls += 1
            else:
                internal_calls += 1

            for arg in call_state.arg_states:
                values += arg.value + '\n'
            values += call_state.return_state.value + '\n'

            hash_id = hashlib.sha1(values.encode()).hexdigest()
            full_filename = save_dir + '/' + str(hash_id) + '.txt'
            write_txt(full_filename, values)

    print('all_methods', len(monitored_program.all_methods()))
    print('all_calls', len(monitored_program.all_calls()))
    print('calls_with_return_and_args', counter)
    print('test calls', test_calls)
    print('internal calls', internal_calls)
