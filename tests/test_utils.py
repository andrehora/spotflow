import unittest
from happyflow.utils import *


class TestUtils(unittest.TestCase):

    def test_find_python_file(self):
        files = find_python_files('')
        for filename in files:
            self.assertTrue('/' in filename)
            self.assertTrue(filename.endswith('.py'))

    def test_intersection(self):
        start_line = 10
        end_line = 20
        lines = range(start_line, end_line + 1)

        other_lines = [1, 10, 15, 20, 100]
        inter = line_intersection(lines, other_lines)

        self.assertEqual(inter, [10, 15, 20])

    def test_find_module_name(self):
        self.assertEqual(find_module_name('module.py'), 'module')
        self.assertEqual(find_module_name('a/b/module.py'), 'module')

    def test_guess_value(self):
        self.assertEqual(get_obj_value(100), '100')
        self.assertEqual(get_obj_value('foo'), "'foo'")
        self.assertEqual(get_obj_value([1, 2, 3, 4]), "[1, 2, 3, 4]")
        self.assertEqual(get_obj_value({1, 2, 3, 4}), "{1, 2, 3, 4}")
        self.assertEqual(get_obj_value(object()), "object obj")
        self.assertEqual(get_obj_value(self.test_guess_value), "test_guess_value def")
        self.assertEqual(get_obj_value(TestUtils), "TestUtils def")

        from tests.stub_sut import Calculator
        self.assertEqual(get_obj_value(Calculator), 'Calculator def')
        self.assertEqual(get_obj_value(Calculator()), 'Calculator obj')
        self.assertEqual(get_obj_value(Calculator(100)), 'Calculator obj')
        self.assertEqual(get_obj_value(Calculator(100).add), 'add def')
        self.assertEqual(get_obj_value(Calculator(100).__str__), '__str__ def')
        self.assertEqual(get_obj_value(Calculator(100).add(1)), 'None')
        self.assertEqual(get_obj_value(Calculator(100).total), '100')



if __name__ == '__main__':
    unittest.main()