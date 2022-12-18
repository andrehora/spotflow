import csv


def write_csv(filename, content):
    with open(filename, 'w') as fout:
        wr = csv.writer(fout, quoting=csv.QUOTE_ALL)
        wr.writerows(content)


def export_metrics_to_csv(monitored_program, filename, metrics_func):

    sorted_methods = sorted(monitored_program.all_methods(), key=lambda mth: mth.full_name)
    content = []

    for method in sorted_methods:

        names_and_values = metrics_func(method)

        if not content:
            metric_names = get_metric_names(names_and_values)
            content.append(metric_names)

        metric_values = get_metric_values(names_and_values)
        content.append(metric_values)

    write_csv(filename, content)


def get_metric_names(names_and_values):
    return get_metric(names_and_values, 0)


def get_metric_values(names_and_values):
    return get_metric(names_and_values, 1)


def get_metric(names_and_values, index):
    result = []
    for metric in names_and_values:
        result.append(metric[index])
    return result
