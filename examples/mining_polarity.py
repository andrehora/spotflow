from spotflow.api import monitor_unittest_module
from scripts import polarity
from spotflow.utils import write_csv


def monitor_test(test, target_methods):
    print('Test suite:', test.__name__)
    monitored_system = monitor_unittest_module(test, target_methods, var_states=False)
    test_methods = polarity.for_test_methods(monitored_system)

    project_name = target_methods[0]
    filename = '../report/' + project_name + '.csv'
    write_csv(filename, test_methods)


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

from test import test_imaplib as test

monitor_test(test, ['imaplib'])
