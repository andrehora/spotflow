from spotflow.utils import write_txt, ensure_dir
import hashlib


def calls_with_primitive_types(monitored_program):

    print('calls_with_primitive_types')

    counter = 0
    counter_all_primitive = 0
    counter_primitive_returns = 0

    for call in monitored_program.all_calls():
        call_state = call.call_state
        if call_state.has_return() and call_state.has_argument():
            counter += 1

            if call_state.return_state.is_primitive():
                counter_primitive_returns += 1

                all_primitive_args = True
                for arg in call_state.arg_states:
                    if not arg.is_primitive():
                        all_primitive_args = False
                        break

                if all_primitive_args:
                    counter_all_primitive += 1
                    for arg in call_state.arg_states:
                        print(arg)
                    print(call_state.return_state)
                    print('======================')

    print('all_methods', len(monitored_program.all_methods()))
    print('all_calls', len(monitored_program.all_calls()))
    print('calls_with_arg_and_return', counter)
    print('counter_primitive_returns', counter_primitive_returns)
    print('counter_all_primitive', counter_all_primitive)


def calls_with_return_and_args(monitored_program):

    print('calls_with_return_and_args')

    counter = 0
    test_calls = 0
    internal_calls = 0

    for call in monitored_program.all_calls():
        call_state = call.call_state
        if call_state.has_return() and call_state.has_argument():
            counter += 1
            values = ""

            print(call.is_directly_called_from_test())
            if call.is_directly_called_from_test():
                test_calls += 1
            else:
                internal_calls += 1

            for arg in call_state.arg_states:
                values += arg.value + '\n'
            values += call_state.return_state.value + '\n'

            hash_id = hashlib.sha1(values.encode()).hexdigest()
            ensure_dir('hash38')
            write_txt('hash38/' + str(hash_id) + '.txt', values)

            print(values)
            print(hash_id)
            print('======================')

    print('all_methods', len(monitored_program.all_methods()))
    print('all_calls', len(monitored_program.all_calls()))
    print('calls_with_return_and_args', counter)
    print('test calls', test_calls)
    print('internal calls', internal_calls)
