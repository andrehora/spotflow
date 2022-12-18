import unittest
from spotflow.api import pprint


class TestPrettyPrint(unittest.TestCase):

    def test_pprint_count_uppercase_words(self):

        from tests.e2e.stub_funcs import inputs_count, count_uppercase_words
        ok = pprint(inputs_count, [count_uppercase_words])
        self.assertTrue(ok)

    def test_pprint_parseparam(self):

        from tests.e2e.stub_funcs import inputs_parseparam, parseparam
        ok = pprint(inputs_parseparam, [parseparam])
        self.assertTrue(ok)

    def test_pprint_splitparam(self):

        from tests.e2e.stub_funcs import inputs_splitparam, splitparam
        ok = pprint(inputs_splitparam, [splitparam])
        self.assertTrue(ok)


if __name__ == '__main__':
    unittest.main()
