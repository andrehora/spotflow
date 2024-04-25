import json
import importlib
from spotflow.utils import write_csv
from collections import Counter
from spotflow.api import monitor_unittest_module

def spotflow_after(monitored_program, *args):
    pass


def write_json(data):
    with open('mapping_dataset.json', 'w', encoding='utf-8') as f:
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
        find_tests_and_methods(monitored_program, result)

    values_count = 0
    call_count = 0
    for test_name in result:
        call_count += len(result[test_name])
        result[test_name] = Counter(result[test_name]).most_common()
        values_count += len(result[test_name])
        print(test_name, result[test_name])

    print(len(result))
    print(values_count)
    print(call_count)
    write_json(result)


def find_tests_and_methods(monitored_program, result):

    for call in monitored_program.all_calls():
        for test_name in monitored_program.tests:
            if test_name in call.call_stack:
                result[test_name] = result.get(test_name, [])
                # result[test_name].add((call.monitored_method.full_name, call.is_directly_called_by_test()))
                result[test_name].append(call.monitored_method.full_name)

    return result

run_and_export_data()