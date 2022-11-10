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

python -m spotflow -a calls -t abc unittest test.test_abc
python -m spotflow -a calls -t argparse unittest test.test_argparse
python -m spotflow -a calls -t base64 unittest test.test_base64
python -m spotflow -a calls -t bdb unittest test.test_bdb
python -m spotflow -a calls -t binascii unittest test.test_binascii # check
python -m spotflow -a calls -t cmd unittest test.test_cmd
python -m spotflow -a calls -t codecs unittest test.test_codecs # slow
python -m spotflow -a calls -t colorsys unittest test.test_colorsys
python -m spotflow -a calls -t compileall unittest test.test_compileall
python -m spotflow -a calls -t configparser unittest test.test_configparser # slow
python -m spotflow -a calls -t copy unittest test.test_copy
python -m spotflow -a calls -t copyreg unittest test.test_copyreg
python -m spotflow -a calls -t dbm unittest test.test_dbm
python -m spotflow -a calls -t dis unittest test.test_dis # slow
python -m spotflow -a calls -t doctest unittest test.test_doctest
python -m spotflow -a calls -t filecmp unittest test.test_filecmp
python -m spotflow -a calls -t fileinput unittest test.test_fileinput
python -m spotflow -a calls -t html unittest test.test_html
python -m spotflow -a calls -t http unittest test.test_http_cookies
python -m spotflow -a calls -t http unittest test.test_httpservers
python -m spotflow -a calls -t inspect unittest test.test_inspect.TestGetattrStatic # fail
python -m spotflow -a calls -t io unittest test.test_io

# running other projects
#python -m spotflow -t rich -d pytest rich/tests
#python -m spotflow -t dateutil pytest dateutil/test
#python -m spotflow -t rest_framework pytest tests
