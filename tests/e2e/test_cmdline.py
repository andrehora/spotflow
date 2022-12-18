import unittest
from spotflow.cmdline import SpotFlowCommandLine


class TestCmdLine(unittest.TestCase):

    def test_one_t_unittest(self):

        args = '-t gzip -c unittest test.test_gzip'.split()
        result = SpotFlowCommandLine(args).run()
        self.assertEqual(result, 0)

    def test_multiple_t_unittest(self):

        args = '-t gzip -t _compression -c unittest test.test_gzip'.split()
        result = SpotFlowCommandLine(args).run()
        self.assertEqual(result, 0)

    def test_one_tt_unittest(self):
        args = '-tt read -c unittest test.test_gzip'.split()
        result = SpotFlowCommandLine(args).run()
        self.assertEqual(result, 0)

    def test_multiple_tt_unittest(self):
        args = '-tt read -tt write -c unittest test.test_gzip'.split()
        result = SpotFlowCommandLine(args).run()
        self.assertEqual(result, 0)

    def test_one_tt_program(self):
        args = '-tt sum -c spotflow.sample'.split()
        result = SpotFlowCommandLine(args).run()
        self.assertEqual(result, 0)

        args = '-tt absolute -c spotflow.sample'.split()
        result = SpotFlowCommandLine(args).run()
        self.assertEqual(result, 0)

    def test_multiple_tt(self):
        args = '-tt sum -tt absolute -c spotflow.sample'.split()
        result = SpotFlowCommandLine(args).run()
        self.assertEqual(result, 0)

    def test_no_t(self):
        args = '-c spotflow.sample'.split()
        result = SpotFlowCommandLine(args).run()
        self.assertEqual(result, 0)


if __name__ == '__main__':
    unittest.main()
