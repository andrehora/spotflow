from collections import Counter


class Analysis:

    def __init__(self, target_entity, flow_result):
        self.target_entity = target_entity
        self.flow_result = flow_result

    def number_of_distinct_sources(self):
        return len(set(self.flow_result.source_entity_names))

    def number_of_distinct_flows(self):
        return len(set(self.flow_result.distinct_lines()))

    def number_of_flows(self):
        return len(self.flow_result.flows)

    def most_common_flow(self, n=None):
        lines = self.flow_result.distinct_lines()
        if n == -1:
            return self._least_common(lines)
        return self._most_common(lines, n)

    def most_common_args(self, n=None):
        args = self.flow_result.args()
        args_count = {}
        if n == -1:
            for arg in args:
                args_count[arg] = self._least_common(args[arg])
            return args_count

        for arg in args:
            args_count[arg] = self._most_common(args[arg], n)
        return args_count

    def most_common_return_values(self, n=None):
        values = self.flow_result.return_states()
        if n == -1:
            return self._least_common(values)
        return self._most_common(values, n)

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



