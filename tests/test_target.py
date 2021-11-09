import unittest
from happyflow.target_model import TargetFunction, TargetMethod


class TestTestLoader(unittest.TestCase):
    pass


class TestTestRunner(unittest.TestCase):
    pass


class TestSUTLoader(unittest.TestCase):
    pass


class TestSUT(unittest.TestCase):

    def test_method(self):
        f = TargetMethod(module_name='m', class_name='c', name='foo', full_name='m.c.foo')
        self.assertEqual(f.module_name, 'm')
        self.assertEqual(f.class_name, 'c')
        self.assertEqual(f.name, 'foo')
        self.assertEqual(f.full_name, 'm.c.foo')

    def test_function(self):
        f = TargetFunction(module_name='m', name='foo', full_name='m.foo')
        self.assertEqual(f.module_name, 'm')
        self.assertEqual(f.name, 'foo')
        self.assertEqual(f.full_name, 'm.foo')


if __name__ == '__main__':
    unittest.main()