class TextReport:

    def __init__(self, method_trace):
        self.method_trace = method_trace

    def report(self):

        # print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        # self.show_state_summary(state_history)
        # print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')

        current_line = 0
        for flow in self.method_trace.flows:
            for line in flow.info.lines:
                current_line += 1
                if line.is_run():
                    is_run = '✅'
                if line.is_not_run():
                    is_run = '❌'
                if line.is_not_exec():
                    is_run = '⬜'

                line_number_str = str(current_line).ljust(2)
                is_run = is_run.ljust(3)

                code_str = f'{line_number_str} {is_run} {line.code.rstrip()}'
                code_str = code_str.ljust(50)
                print(code_str)
            print()

                # states = state_history.states_for_line(current_line)
                #
                # if self.target_method.line_is_entity_definition(current_line):
                #     arg_summary = ''
                #     separator = '🟢 '
                #     for arg in state_history.arg_states:
                #         if arg.name != 'self':
                #             arg_summary += f'{separator}{arg} '
                #     if arg_summary:
                #         print(code_str, arg_summary)
                #     else:
                #         print(code_str)
                # elif state_history.is_return_value(current_line):
                #     separator = '🔴 '
                #     return_state = state_history.return_state
                #     return_str = f'{separator}{return_state}'
                #     print(code_str, return_str)
                # elif states:
                #     separator = '🟡 '
                #     states_str = f'{separator}{separator.join(states)}'
                #     print(code_str, states_str)
                # else:
                #     print(code_str)

    def show_state_summary(self, state_result):
        print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        for arg in state_result.arg_states:
            if arg.name != 'self':
                arg_summary = f'🟢 IN {arg.name}: {str(arg.value)}'
                print(arg_summary)

        if state_result.has_return():
            return_summary = f'🔴 OUT {state_result.return_state}'
            print(return_summary)

        for var in state_result.var_states:
            if var != 'self':
                state_history = state_result.var_states[var]
                values = state_history.distinct_sequential_values()
                values_str = ' -> '.join(map(str, values))
                var_summary = f'🟡 {var}: {values_str}'
                print(var_summary)



