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


if __name__ == '__main__':
    unittest.main()