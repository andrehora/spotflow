class TextReport:

    def __init__(self, monitored_method):
        self.monitored_method = monitored_method

    def report(self):

        # self.show_state_summary(self.monitored_method.calls[0].call_state)
        # print('============================================')

        for flow in self.monitored_method.flows:
            current_line = 0
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

                code_str = f'{line_number_str} {is_run} {line.code().rstrip()}'
                code_str = code_str.ljust(40)

                if line.is_arg():
                    arg_summary = ''
                    separator = '🟢 '
                    arg_summary += f'{separator}{line.state}'
                    if arg_summary:
                        print(code_str, arg_summary)
                    else:
                        print(code_str)
                elif line.is_return():
                    separator = '🔴 '
                    return_str = f'{separator}{line.state}'
                    print(code_str, return_str)
                elif line.is_var():
                    separator = '🟡 '
                    states_str = f'{separator}{separator.join(line.state)}'
                    print(code_str, states_str)
                else:
                    print(code_str)
            print()

    def show_state_summary(self, state_result):
        print('============================================')
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



