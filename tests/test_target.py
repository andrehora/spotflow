import unittest
from happyflow.target import TargetMethod


class TestTarget(unittest.TestCase):

    def test_is_method(self):
        f = TargetMethod(module_name='m', class_name='c', name='foo', full_name='m.c.foo', filename='')
        self.assertEqual(f.module_name, 'm')
        self.assertEqual(f.class_name, 'c')
        self.assertEqual(f.name, 'foo')
        self.assertEqual(f.full_name, 'm.c.foo')
        self.assertEqual(f.filename, '')

        self.assertTrue(f.is_method())
        self.assertFalse(f.is_func())

    def test_is_function(self):
        f = TargetMethod(module_name='m', class_name=None, name='foo', full_name='m.foo', filename='')
        self.assertEqual(f.module_name, 'm')
        self.assertEqual(f.class_name, None)
        self.assertEqual(f.name, 'foo')
        self.assertEqual(f.full_name, 'm.foo')
        self.assertEqual(f.filename, '')

        self.assertFalse(f.is_method())
        self.assertTrue(f.is_func())


if __name__ == '__main__':
    unittest.main()