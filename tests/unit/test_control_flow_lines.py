import asyncio
import unittest
from tests.unit.stub_sut import ControlFlow, async_values
from spotflow.api import monitor_func


class TestControlFlowLines(unittest.TestCase):
    """The lines of a method with if, elif, while and for statements."""

    base = 'tests.unit.stub_sut.ControlFlow'

    def lines(self, name, func):
        # Line numbers in the method: its definition is line 1
        result = monitor_func(func, [self.base])
        info = result[f'{self.base}.{name}'].info
        self.assertEqual(info.control_flow_lines & info.other_lines, set())
        control_flow_lines = sorted(lineno - info.start_line + 1 for lineno in info.control_flow_lines)
        other_lines = sorted(lineno - info.start_line + 1 for lineno in info.other_lines)
        return control_flow_lines, other_lines

    def test_names_start_with_keywords(self):
        control_flow_lines, other_lines = self.lines('names_start_with_keywords',
                                                     ControlFlow().names_start_with_keywords)
        self.assertEqual(control_flow_lines, [])
        self.assertEqual(other_lines, [2, 3, 4, 5, 6])

    def test_if_while_for(self):
        control_flow_lines, other_lines = self.lines('statements', lambda: ControlFlow().statements(1))
        self.assertEqual(control_flow_lines, [2, 8, 10])
        self.assertEqual(other_lines, [3, 9, 11, 12])

    def test_elif(self):
        control_flow_lines, other_lines = self.lines('statements', lambda: ControlFlow().statements(2))
        self.assertEqual(control_flow_lines, [2, 4, 8, 10])

    def test_inline_if(self):
        control_flow_lines, other_lines = self.lines('inline_if', lambda: ControlFlow().inline_if(1))
        self.assertEqual(control_flow_lines, [2])
        self.assertEqual(other_lines, [3])

    def test_multi_line_if(self):
        control_flow_lines, other_lines = self.lines('multi_line_if', lambda: ControlFlow().multi_line_if(1, 1))
        self.assertEqual(control_flow_lines, [2, 3])
        self.assertEqual(other_lines, [4, 5])

    def test_expressions_are_not_control_flow(self):
        control_flow_lines, other_lines = self.lines('expressions', lambda: ControlFlow().expressions(1))
        self.assertEqual(control_flow_lines, [])
        self.assertEqual(other_lines, [2, 3, 4, 5])

    def test_nested(self):
        control_flow_lines, other_lines = self.lines('nested', lambda: ControlFlow().nested([1]))
        self.assertEqual(control_flow_lines, [2, 3, 4])
        self.assertEqual(other_lines, [5, 6])

    def test_async_for(self):
        func = lambda: asyncio.run(ControlFlow().async_for(async_values()))
        control_flow_lines, other_lines = self.lines('async_for', func)
        self.assertEqual(control_flow_lines, [2])
        self.assertEqual(other_lines, [3])

    def test_only_lines_that_run(self):
        control_flow_lines, other_lines = self.lines('not_run', lambda: ControlFlow().not_run(0))
        self.assertEqual(control_flow_lines, [2])
        self.assertEqual(other_lines, [5])


if __name__ == '__main__':
    unittest.main()
