from collections import Counter


class Analysis:

    def __init__(self, target_entity, flow_result):
        self.target_entity = target_entity
        self.flow_result = flow_result

    def distinct_flows(self):
        return len(self.most_common_flow())

    def most_common_flow(self, n=None):
        run_lines = self._run_lines_as_tuple()
        if n == -1:
            return self._least_common(run_lines)
        return self._most_common(run_lines, n)

    def most_common_args(self, n=None):
        args = {}
        for flow in self.flow_result.flows:
            for arg in flow.state_result.args:
                if arg.name in args:
                    args[arg.name].append(arg.value)
                else:
                    args[arg.name] = [arg.value]

        args_count = {}
        if n == -1:
            for arg in args:
                args_count[arg] = self._least_common(args[arg])
            return args_count

        for arg in args:
            args_count[arg] = self._most_common(args[arg], n)
        return args_count

    def most_common_return_values(self, n=None):
        values = []
        for flow in self.flow_result.flows:
            if flow.state_result.has_return():
                value = flow.state_result.return_value.value
                values.append(tuple(value))

        if n == -1:
            return self._least_common(values)
        return self._most_common(values, n)

    def _most_common(self, elements, n=None):
        return Counter(elements).most_common(n)

    def _least_common(self, elements):
        return [Counter(elements).most_common()[-1]]

    def _run_lines_as_tuple(self):
        result = []
        for flow in self.flow_result.flows:
            result.append(tuple(flow.distinct_lines()))
        return result






