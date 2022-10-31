# running python libs
python -m spotflow -t email unittest test.test_email.test_email.TestMessageAPI
python -m spotflow -t ast unittest test.test_ast
python -m spotflow -t gzip unittest test.test_gzip
python -m spotflow -t urllib unittest test.test_urlparse
python -m spotflow -t json unittest test.test_json
python -m spotflow -t calendar unittest test.test_calendar
python -m spotflow -t collections unittest test.test_collections
python -m spotflow -t csv unittest test.test_csv
python -m spotflow -t ftplib unittest test.test_ftplib
python -m spotflow -t html unittest test.test_htmlparser
python -m spotflow -t http unittest test.test_httplib
python -m spotflow -t os unittest test.test_os
python -m spotflow -t math unittest test.test_math
python -m spotflow -t tarfile unittest test.test_tarfile
python -m spotflow -t pathlib unittest test.test_pathlib
python -m spotflow -t locale unittest test.test_locale
python -m spotflow -t hashlib unittest test.test_hashlib
python -m spotflow -t logging unittest test.test_logging
python -m spotflow -t ftplib unittest test.test_ftplib
python -m spotflow -t difflib unittest test.test_difflib
python -m spotflow -t imaplib unittest test.test_imaplib
python -m spotflow -t smtplib unittest test.test_smtplib

# running other projects
python -m spotflow -t rich -d pytest rich/tests
python -m spotflow -t dateutil pytest dateutil/test
python -m spotflow -t rest_framework pytest tests
