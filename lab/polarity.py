from spotflow.api import monitor_unittest_module
from spotflow.utils import count_values, ratio, write_csv


def compute_polarity(test, target_methods):
    print('Test suite:', test.__name__)
    monitored_program = monitor_unittest_module(test, target_methods, var_states=False)
    test_methods = polarity_for_program(monitored_program)

    project_name = target_methods[0]
    filename = project_name + '.csv'
    write_csv(filename, test_methods)


def polarity_for_program(monitored_program):

    print('compute_polarity_for_test_methods')

    test_suite_data = compute_polarity(monitored_program, min_branch_frequency=99)

    # for each in branch_track_values:
    #     tf_values = branch_track_values[each]
    #     print(each, tf_values)

    to_export = []
    for test_name in test_suite_data:
        t, f, total_tf, positivity, negativity, exception_freq = test_suite_data[test_name]
        to_export.append([test_name, t, f, total_tf, positivity, negativity, exception_freq])
        print(test_name, t, f, total_tf, positivity, negativity, exception_freq)

    return to_export


def compute_polarity(monitored_program, min_branch_frequency=95):

    branch_data = branch_data_for_program(monitored_program)
    test_suite_branch_data = {}
    test_suite_exception_data = {}

    for call in monitored_program.all_calls():

        branch_value = check_branch(call, branch_data, min_branch_frequency)
        if branch_value:
            if call.is_started_in_test():
                test_name = call.call_stack[0]
                test_suite_branch_data[test_name] = test_suite_branch_data.get(test_name, [])
                test_suite_branch_data[test_name].extend(branch_value)

        if call.call_state.has_exception():
            if call.is_started_in_test():
                test_name = call.call_stack[0]
                test_suite_exception_data[test_name] = test_suite_exception_data.get(test_name, [])
                test_suite_exception_data[test_name].append(call.call_state.exception_state.value)

    test_suite_result = {}
    for test_name in test_suite_branch_data:
        tf_values = test_suite_branch_data[test_name]
        tf_counter = count_values(tf_values)
        t = tf_counter[0]
        f = tf_counter[1]
        total_tf = t + f
        positivity = ratio(t, t + f)
        negativity = ratio(f, t + f)
        test_suite_result[test_name] = t, f, total_tf, positivity, negativity, 0

    for test_name in test_suite_exception_data:
        exception_freq = len(test_suite_exception_data[test_name])
        if test_name in test_suite_result:
            t, f, total_tf, positivity, negativity, _ = test_suite_result[test_name]
            test_suite_result[test_name] = t, f, total_tf, positivity, negativity, exception_freq
        else:
            test_suite_result[test_name] = 0, 0, 0, 0, 0, exception_freq

    return test_suite_result


def branch_data_for_program(monitored_program):

    branch_data = {}
    for call in monitored_program.all_calls():
        branch_data_for_call(call, branch_data)

    for key in branch_data:

        tf_values = branch_data[key]
        tf_counter = count_values(tf_values)

        t_freq = tf_counter[0]
        f_freq = tf_counter[1]

        branch_frequency = ratio(max(t_freq, f_freq), t_freq + f_freq)
        branch_prevalence = (True if t_freq > f_freq else False)

        branch_data[key] = t_freq, f_freq, branch_frequency, branch_prevalence

    return branch_data


def branch_data_for_call(method_call, branch_data):

    executable_lines = method_call.monitored_method.info.executable_lines()

    for control_flow_lineno in sorted(method_call.monitored_method.info.control_flow_lines):
        key = method_call.monitored_method.info.filename, control_flow_lineno
        if control_flow_lineno in executable_lines:
            control_flow_value = check_control_flow(method_call, control_flow_lineno, executable_lines)
            if control_flow_value is not None:
                branch_data[key] = branch_data.get(key, [])
                branch_data[key].append(control_flow_value)


def check_branch(method_call, branch_data, min_branch_frequency):

    result = []
    executable_lines = method_call.monitored_method.info.executable_lines()

    for control_flow_lineno in sorted(method_call.monitored_method.info.control_flow_lines):
        if control_flow_lineno in executable_lines:
            control_flow_value = check_control_flow(method_call, control_flow_lineno, executable_lines)
            if control_flow_value is not None:
                key = method_call.monitored_method.info.filename, control_flow_lineno
                t, f, branch_frequency, branch_prevalence = branch_data[key]
                if branch_frequency >= min_branch_frequency:
                    if control_flow_value == branch_prevalence:
                        result.append(True)
                    else:
                        result.append(False)
    return result


def check_control_flow(method_call, control_flow_lineno, executable_lines):

    next_control_flow_line = find_next_executable_line(control_flow_lineno, executable_lines)
    if not next_control_flow_line:
        return None

    if control_flow_lineno in method_call.run_lines and next_control_flow_line in method_call.run_lines:
        return True
    return False


def find_next_executable_line(lineno, executable_lines):
    try:
        index = executable_lines.index(lineno)
        return executable_lines[index + 1]
    except Exception:
        return None