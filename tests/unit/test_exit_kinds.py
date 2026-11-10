import asyncio
import unittest
from tests.unit.stub_sut import ExitKinds
from spotflow.api import monitor_func


class TestExitKinds(unittest.TestCase):
    """Returns and yields are found from what the frame runs, not from the text of the line."""

    base = 'tests.unit.stub_sut.ExitKinds'

    def states(self, name, func):
        result = monitor_func(func, [self.base])
        return [call.call_state for call in result[f'{self.base}.{name}'].calls]

    def state(self, name, func):
        states = self.states(name, func)
        self.assertEqual(len(states), 1)
        return states[0]

    def yields(self, state):
        return [each.value for each in state.yield_states]

    # Returns

    def test_exception_in_return_line_is_not_a_return(self):
        def func():
            with self.assertRaises(ValueError):
                ExitKinds().return_raises('x')

        state = self.state('return_raises', func)
        self.assertIsNone(state.return_state)
        self.assertEqual(state.exception_state, 'ValueError')

    def test_return_line_without_exception(self):
        state = self.state('return_raises', lambda: ExitKinds().return_raises('1'))
        self.assertEqual(state.return_state, '1')
        self.assertIsNone(state.exception_state)

    def test_name_starts_with_return(self):
        state = self.state('name_starts_with_return', ExitKinds().name_starts_with_return)
        self.assertIsNone(state.return_state)

    def test_name_starts_with_yield(self):
        state = self.state('name_starts_with_yield', ExitKinds().name_starts_with_yield)
        self.assertIsNone(state.return_state)
        self.assertEqual(state.yield_states, [])

    def test_inline_return(self):
        def func():
            ExitKinds().inline_return(1)
            ExitKinds().inline_return(0)

        states = self.states('inline_return', func)
        self.assertEqual(states[0].return_state, '1')
        self.assertEqual(states[0].return_state.lineno, states[1].return_state.lineno - 1)
        self.assertEqual(states[1].return_state, '2')

    def test_inline_return_or_implicit(self):
        def func():
            ExitKinds().inline_return_or_implicit(1)
            ExitKinds().inline_return_or_implicit(0)

        states = self.states('inline_return_or_implicit', func)
        self.assertEqual(states[0].return_state, '1')
        self.assertIsNone(states[1].return_state)

    def test_inline_def(self):
        state = self.state('inline_def', ExitKinds().inline_def)
        self.assertEqual(state.return_state, '7')

    def test_return_in_with(self):
        state = self.state('return_in_with', ExitKinds().return_in_with)
        self.assertEqual(state.return_state, '5')

    def test_return_in_finally(self):
        state = self.state('return_in_finally', ExitKinds().return_in_finally)
        self.assertEqual(state.return_state, '6')

    def test_multi_line_return(self):
        state = self.state('multi_line_return', lambda: ExitKinds().multi_line_return(1))
        self.assertEqual(state.return_state, "{'a': 1}")

    def test_return_none_in_expression(self):
        state = self.state('return_none_in_expression', lambda: ExitKinds().return_none_in_expression(0))
        self.assertEqual(state.return_state, 'None')

    def test_lambdas(self):
        func = ExitKinds().call_lambdas
        result = monitor_func(func, [self.base])
        calls = result[f'{self.base}.call_lambdas.<locals>.<lambda>'].calls
        self.assertEqual([call.call_state.return_state.value for call in calls], ['3', 'None'])

    # Yields

    def test_assigned_yield(self):
        state = self.state('assigned_yield', lambda: list(ExitKinds().assigned_yield()))
        self.assertEqual(self.yields(state), ['1', '2'])
        self.assertIsNone(state.return_state)

    def test_yield_in_expression(self):
        state = self.state('yield_in_expression', lambda: list(ExitKinds().yield_in_expression()))
        self.assertEqual(self.yields(state), ['1'])

    def test_inline_yield(self):
        state = self.state('inline_yield', lambda: list(ExitKinds().inline_yield(1)))
        self.assertEqual(self.yields(state), ['1'])

    def test_end_of_generator_is_not_a_yield(self):
        state = self.state('closed', lambda: list(ExitKinds().closed()))
        self.assertEqual(self.yields(state), ['1', '2'])
        self.assertEqual(self.yields(state), [each.value for each in state.get_yield_states()])
        self.assertIsNone(state.return_state)

    def test_yield_then_return(self):
        state = self.state('yield_then_return', lambda: list(ExitKinds().yield_then_return()))
        self.assertEqual(self.yields(state), ['1'])
        self.assertEqual(state.return_state, '9')

    def test_yield_then_statement(self):
        state = self.state('yield_then_statement', lambda: list(ExitKinds().yield_then_statement()))
        self.assertEqual(self.yields(state), ['1'])
        self.assertIsNone(state.return_state)

    def test_yield_from(self):
        state = self.state('yield_from', lambda: list(ExitKinds().yield_from()))
        self.assertEqual(self.yields(state), ['1', '2', '1'])
        self.assertIsNone(state.return_state)

    def test_closed_generator(self):
        state = self.state('closed', ExitKinds().run_closed)
        self.assertEqual(self.yields(state), ['1'])
        self.assertIsNone(state.return_state)

    def test_exception_thrown_into_generator(self):
        state = self.state('thrown', ExitKinds().run_thrown)
        self.assertEqual(self.yields(state), ['1'])
        self.assertIsNone(state.return_state)

    def test_yield_then_raise(self):
        def func():
            with self.assertRaises(KeyError):
                list(ExitKinds().yield_then_raise())

        state = self.state('yield_then_raise', func)
        self.assertEqual(self.yields(state), ['1'])
        self.assertIsNone(state.return_state)

    # Generator expressions: their lines are of the method they are in, but
    # the values they yield are not yielded by the method

    def test_generator_expression_in_return(self):
        state = self.state('genexpr_in_return', lambda: ExitKinds().genexpr_in_return([1, 2]))
        self.assertEqual(state.yield_states, [])
        self.assertEqual(state.return_state, "'1 2'")

    def test_generator_expression_in_assign(self):
        state = self.state('genexpr_in_assign', lambda: ExitKinds().genexpr_in_assign([1, 2]))
        self.assertEqual(state.yield_states, [])
        self.assertEqual(state.return_state, '3')

    def test_generator_expression_in_yield(self):
        state = self.state('genexpr_in_yield', lambda: list(ExitKinds().genexpr_in_yield([1, 2])))
        self.assertEqual(self.yields(state), ['3'])
        self.assertIsNone(state.return_state)

    def test_generator_expression_lines(self):
        result = monitor_func(lambda: ExitKinds().genexpr_in_assign([1, 2]), [self.base])
        method = result[f'{self.base}.genexpr_in_assign']
        self.assertEqual(method.info.yield_lines, set())
        self.assertFalse(method.info.has_yield())
        self.assertEqual(len(method.info.return_lines), 1)
        # The line of the generator expression runs once for each value
        self.assertGreater(len(method.calls[0].run_lines), 2)

    # Coroutines

    def test_await_is_not_a_yield(self):
        func = lambda: asyncio.run(ExitKinds().coroutine())
        for name in ['coroutine', 'coroutine_inner']:
            state = self.state(name, func)
            self.assertEqual(state.yield_states, [], name)
            self.assertEqual(state.return_state, '4', name)

    def test_async_generator(self):
        func = lambda: asyncio.run(ExitKinds().use_async_generator())
        state = self.state('async_generator', func)
        self.assertEqual(len(state.yield_states), 2)
        self.assertIsNone(state.return_state)

        state = self.state('use_async_generator', func)
        self.assertEqual(state.yield_states, [])
        self.assertEqual(state.return_state, '[1, 2]')


if __name__ == '__main__':
    unittest.main()
