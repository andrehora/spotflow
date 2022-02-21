from happyflow.api import monitor_unittest_module, monitor_unittest_testcase
from mining_scripts import polarity


def monitor_test(test, target_methods=None, target_files=None, ignore_files=None):
    print('Test suite:', test.__name__)
    monitored_system = monitor_unittest_module(test, target_methods, target_files, ignore_files, var_states=False)
    # monitored_system = monitor_unittest_testcase(test, target_methods, target_files, ignore_files, var_states=False)

    # polarity.method_calls_that_return_true_or_false(monitored_system)
    # polarity.test_calls_that_return_true_or_false(monitored_system)

    # polarity.test_calls_branch_values(monitored_system)
    polarity.test_calls_branch_track_values(monitored_system)


def main():

    from test import test_gzip as test
    monitor_test(test, ['gzip'])

    from test import test_collections as test
    monitor_test(test, ['collections'])

    from test import test_httplib as test
    monitor_test(test, ['http'])

    from test import test_zipfile as test
    monitor_test(test, ['zipfile'])

    from test import test_tarfile as test
    monitor_test(test, ['tarfile'])

    from test import test_pathlib as test
    monitor_test(test, ['pathlib'])

    from test import test_email as test
    monitor_test(test, ['email'])

    from test import test_logging as test
    monitor_test(test, ['logging'])

    from test import test_difflib as test
    monitor_test(test, ['difflib'])

    from test import test_imaplib as test
    monitor_test(test, ['imaplib'])


# main()

from test import test_gzip as test
monitor_test(test, target_methods=['gzip'])