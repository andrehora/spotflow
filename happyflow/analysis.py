from collections import Counter


class Analysis:

    def __init__(self, method_trace):
        self.method_trace = method_trace

    def number_of_distinct_flows(self):
        return len(set(self.method_trace.distinct_run_lines()))

    def number_of_calls(self):
        return len(self.method_trace.calls)

    def most_common_run_lines(self):
        lines = self.method_trace.distinct_run_lines()
        return self._most_common(lines)

    def most_common_args(self):
        args = self.method_trace.arg_states()
        args_count = {}

        for arg in args:
            args_count[arg] = self._most_common(args[arg])

        return args_count

    def most_common_args_pretty(self):
        return self.pretty_args(self.most_common_args())

    def most_common_return_values(self):
        values = self.method_trace.return_states()
        return self._most_common(values)

    def most_common_return_values_pretty(self):
        return self.pretty_return_values(self.most_common_return_values())

    def _most_common(self, elements, n=10):
        try:
            return Counter(elements).most_common(n)
        except TypeError:
            return []

    def pretty_args(self, args, max_len=150):
        result = []
        for arg_name in args:
            arg_value = {}
            arg_value['name'] = arg_name
            values = ''
            for value in args[arg_name]:
                value_str = value[0]
                count = value[1]
                values += f'{value_str} ({count}) '
            arg_value['value'] = self.clear_values(values, max_len)
            result.append(arg_value)
        return result

    def pretty_return_values(self, return_values, max_len=150):
        values = ''
        for value in return_values:
            values += f'{value[0]} ({value[1]}) '
        if values:
            return self.clear_values(values, max_len)
        return None

    def clear_values(self, values, max_len):
        # values = values.rstrip(', ')
        if len(values) >= max_len:
            values = f'{values[0:max_len]}...'
        return values




