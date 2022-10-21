import unittest
from spotflow.comparator import find_distinct_in_file, find_distinct_in_set


class TestComparator(unittest.TestCase):

    @unittest.skip
    def test_find_distinct_in_file(self):

        result = find_distinct_in_file('./unit/old_all_distinct.txt', './unit/new_all_distinct.txt')
        self.assertEqual(result, {'1', '2', '3', '4', '5', '6'})

    def test_find_distinct_all_equal(self):

        old = {1, 2, 3}
        new = {1, 2, 3}

        result = find_distinct_in_set(old, new)
        self.assertEqual(result, set())

    def test_find_distinct_all_distinct(self):

        old = {1, 2, 3}
        new = {4, 5, 6}

        result = find_distinct_in_set(old, new)
        self.assertEqual(result, {1, 2, 3, 4, 5, 6})

    def test_find_distinct_some_equal(self):

        old = {1, 2, 3}
        new = {3, 4, 5}

        result = find_distinct_in_set(old, new)
        self.assertEqual(result, {1, 2, 4, 5})

    def test_find_distinct_empty(self):

        old = set()
        new = set()

        result = find_distinct_in_set(old, new)
        self.assertEqual(result, set())
