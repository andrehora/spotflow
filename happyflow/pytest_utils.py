import pytest


def run_test(test):
    def run():
        pytest.main(["-x", test])
    return run
