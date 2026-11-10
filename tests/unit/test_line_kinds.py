import unittest
from tests.unit.stub_sut import ExitKinds
from spotflow.api import monitor_func


class TestLineKinds(unittest.TestCase):
    """The lines of a method that return, yield and raise exceptions."""

    base = 'tests.unit.stub_sut.ExitKinds'

    def method(self, name, func):
        result = monitor_func(func, [self.base])
        return result[f'{self.base}.{name}']

    def lines(self, method, linenos):
        # Line numbers in the method: its definition is line 1
        return sorted(lineno - method.info.start_line + 1 for lineno in linenos)

    def test_return_lines(self):
        def func():
            ExitKinds().inline_return(1)
            ExitKinds().inline_return(0)

        method = self.method('inline_return', func)
        self.assertEqual(self.lines(method, method.info.return_lines), [2, 3])
        self.assertTrue(method.info.has_return())
        self.assertFalse(method.info.has_yield())
        self.assertFalse(method.info.has_exception())

    def test_only_return_lines_that_run(self):
        method = self.method('inline_return', lambda: ExitKinds().inline_return(0))
        self.assertEqual(self.lines(method, method.info.return_lines), [3])

    def test_no_return_lines(self):
        method = self.method('name_starts_with_return', ExitKinds().name_starts_with_return)
        self.assertEqual(method.info.return_lines, set())
        self.assertFalse(method.info.has_return())

    def test_yield_lines(self):
        method = self.method('assigned_yield', lambda: list(ExitKinds().assigned_yield()))
        self.assertEqual(self.lines(method, method.info.yield_lines), [2, 3])
        self.assertTrue(method.info.has_yield())
        self.assertFalse(method.info.has_return())

    def test_yield_and_return_lines(self):
        method = self.method('yield_then_return', lambda: list(ExitKinds().yield_then_return()))
        self.assertEqual(self.lines(method, method.info.yield_lines), [2])
        self.assertEqual(self.lines(method, method.info.return_lines), [3])

    def test_exception_lines(self):
        def func():
            with self.assertRaises(ValueError):
                ExitKinds().return_raises('x')

        method = self.method('return_raises', func)
        self.assertEqual(self.lines(method, method.info.exception_lines), [2])
        self.assertTrue(method.info.has_exception())
        self.assertEqual(method.info.return_lines, set())

    def test_no_exception_lines(self):
        method = self.method('return_raises', lambda: ExitKinds().return_raises('1'))
        self.assertEqual(method.info.exception_lines, set())
        self.assertFalse(method.info.has_exception())
        self.assertEqual(self.lines(method, method.info.return_lines), [2])

    def test_line_of_several_kinds(self):
        def func():
            ExitKinds().return_raises('1')
            with self.assertRaises(ValueError):
                ExitKinds().return_raises('x')

        method = self.method('return_raises', func)
        self.assertEqual(self.lines(method, method.info.return_lines), [2])
        self.assertEqual(self.lines(method, method.info.exception_lines), [2])

    def test_yield_line_with_exception(self):
        method = self.method('thrown', ExitKinds().run_thrown)
        self.assertEqual(self.lines(method, method.info.yield_lines), [2])
        self.assertEqual(self.lines(method, method.info.exception_lines), [2])

    # Return states in the lines of a call

    def return_lines_of_call(self, call):
        return {line.lineno: line.state for line in call.path_info().lines if line.is_return()}

    def test_return_state_in_the_line_that_returns(self):
        def func():
            ExitKinds().inline_return(1)
            ExitKinds().inline_return(0)

        method = self.method('inline_return', func)
        self.assertEqual(self.return_lines_of_call(method.calls[0]), {2: '1'})
        self.assertEqual(self.return_lines_of_call(method.calls[1]), {3: '2'})

    def test_no_return_state_in_call_that_does_not_return(self):
        def func():
            ExitKinds().inline_return_or_implicit(1)
            ExitKinds().inline_return_or_implicit(0)

        method = self.method('inline_return_or_implicit', func)
        self.assertEqual(self.return_lines_of_call(method.calls[0]), {2: '1'})
        self.assertEqual(self.return_lines_of_call(method.calls[1]), {})

    def test_no_return_state_in_call_with_exception(self):
        def func():
            ExitKinds().return_raises('1')
            with self.assertRaises(ValueError):
                ExitKinds().return_raises('x')

        method = self.method('return_raises', func)
        self.assertEqual(self.return_lines_of_call(method.calls[0]), {2: '1'})
        self.assertEqual(self.return_lines_of_call(method.calls[1]), {})

    def test_no_return_state_when_not_collected(self):
        result = monitor_func(lambda: ExitKinds().inline_return(1), [self.base], return_states=False)
        method = result[f'{self.base}.inline_return']
        self.assertEqual(self.lines(method, method.info.return_lines), [2])
        self.assertEqual(self.return_lines_of_call(method.calls[0]), {})


if __name__ == '__main__':
    unittest.main()
