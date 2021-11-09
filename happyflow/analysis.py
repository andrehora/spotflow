from collections import Counter
from happyflow.utils import guess_name


class Analysis:

    def __init__(self, target_entity, flow_result):
        self.target_entity = target_entity
        self.flow_result = flow_result

    def number_of_distinct_sources(self):
        return len(set(self.flow_result.source_entity_names))

    def number_of_distinct_flows(self):
        return len(set(self.flow_result.distinct_lines()))

    def number_of_calls(self):
        return len(self.flow_result.flows)

    def most_common_flow(self, n=None):
        lines = self.flow_result.distinct_lines()
        if n == -1:
            return self._least_common(lines)
        return self._most_common(lines, n)

    def most_common_args(self, n=None):
        args = self.flow_result.arg_states()
        args_count = {}
        if n == -1:
            for arg in args:
                args_count[arg] = self._least_common(args[arg])
            return args_count

        for arg in args:
            args_count[arg] = self._most_common(args[arg], n)

        return args_count

    def most_common_args_pretty(self, n=None):
        return self.pretty_args(self.most_common_args(n))

    def most_common_return_values(self, n=None):
        values = self.flow_result.return_states()
        if n == -1:
            return self._least_common(values)
        return self._most_common(values, n)

    def most_common_return_values_pretty(self, n=None):
        return self.pretty_return_values(self.most_common_return_values(n))

    def _most_common(self, elements, n=None):
        # try:
        return Counter(elements).most_common(n)
        # except TypeError:
        #     return []

    def _least_common(self, elements):
        try:
            counter = Counter(elements).most_common()
            if len(counter) == 0:
                return []
            return [Counter(elements).most_common()[-1]]
        except:
            return []

    def pretty_args(self, args, max_len=150):
        result = []
        for arg_name in args:
            arg_value = {}
            arg_value['name'] = arg_name
            values = ''
            for value in args[arg_name]:
                value_str = guess_name(value[0])
                count = value[1]
                values += f'{value_str} ({count}), '
            arg_value['value'] = self.clear_values(values, max_len)
            result.append(arg_value)
        return result

    def pretty_return_values(self, return_values, max_len=150):
        values = ''
        for value in return_values:
            values += f'{value[0]} ({value[1]}), '
        if values:
            return self.clear_values(values, max_len)
        return None

    def clear_values(self, values, max_len):
        values = values.rstrip(', ')
        if len(values) >= max_len:
            values = f'{values[0:max_len]}...'
        return values




