import json
import importlib
from spotflow.utils import write_csv
from collections import Counter
from spotflow.api import monitor_unittest_module


def spotflow_after(monitored_program, *args):

    # compute_argument_states(monitored_program)
    compute_var_states(monitored_program)


def write_json(data):
    with open('var_values_dataset.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=3)


def run_and_export_data():

    target_libs = ['gzip', 'calendar', 'locale', 'json', 'ast', 
                   'csv', 'ftplib', 'collections', 'os', 'tarfile', 
                   'pathlib', 'smtplib', 'argparse', 'configparser', 'email']
    
    
    # target_libs = ['gzip', 'calendar', 'csv', 'ast', 'os', 'json']
    # target_libs = ['gzip', 'calendar']
    # target_libs = ['calendar']

    result = {}
    for target_lib in target_libs:
        test_suite_name = 'test.test_' + target_lib
        test_module = importlib.import_module(test_suite_name)
        monitored_program = monitor_unittest_module(test_module, [target_lib])
        compute_argument_states(monitored_program, result)
        compute_var_states(monitored_program, result)

    values_count = 0
    for var_name in result:
        result[var_name] = Counter(result[var_name]).most_common()
        values_count += len(result[var_name])
        print(var_name, result[var_name])
    
    print(len(result))
    print(values_count)
    write_json(result)


def compute_argument_states(monitored_program, result):

    for call in monitored_program.all_calls():
        for arg in call.call_state.arg_states:
            if arg.name != "self":
                result[arg.name] = result.get(arg.name, [])
                result[arg.name].append(arg.value)

    # for var_name in result:
    #     result[var_name] = Counter(result[var_name]).most_common(5)
    #     print(var_name, result[var_name])

    print(len(result))
    return result


def compute_var_states(monitored_program, result):

    for call in monitored_program.all_calls():
        for var_name in call.call_state.var_states:
            state_history = call.call_state.var_states[var_name]
            for value in state_history.distinct_values():
                result[var_name] = result.get(var_name, [])
                result[var_name].append(value)

    # for var_name in result:
    #     result[var_name] = Counter(result[var_name]).most_common(5)
    #     print(var_name, result[var_name])

    print(len(result))
    return result


run_and_export_data()