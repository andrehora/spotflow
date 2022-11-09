from lab.polarity import compute_polarity


def main():

    from test import test_gzip as test
    compute_polarity(test, ['gzip'])

    from test import test_collections as test
    compute_polarity(test, ['collections'])

    from test import test_httplib as test
    compute_polarity(test, ['http'])

    from test import test_zipfile as test
    compute_polarity(test, ['zipfile'])

    from test import test_tarfile as test
    compute_polarity(test, ['tarfile'])

    from test import test_pathlib as test
    compute_polarity(test, ['pathlib'])

    from test import test_email as test
    compute_polarity(test, ['email'])

    from test import test_logging as test
    compute_polarity(test, ['logging'])

    from test import test_difflib as test
    compute_polarity(test, ['difflib'])

    from test import test_imaplib as test
    compute_polarity(test, ['imaplib'])


# main()

# from test import test_gzip as test
# monitor_test(test, ['gzip'])
