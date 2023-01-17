export PYTHONPATH='/Users/andrehora/Documents/git/spotflow'

# Python libs
python3 -m spotflow -t gzip -s happypath.py -arg output/gzip test.test_gzip
python3 -m spotflow -t email -s happypath.py -arg output/email test.test_email
python3 -m spotflow -t calendar -s happypath.py -arg output/calendar test.test_calendar
python3 -m spotflow -t ftplib -s happypath.py -arg output/ftplib test.test_ftplib
python3 -m spotflow -t collections -s happypath.py -arg output/collections test.test_collections
python3 -m spotflow -t os -s happypath.py -arg output/os test.test_os
python3 -m spotflow -t tarfile -s happypath.py -arg output/tarfile test.test_tarfile
python3 -m spotflow -t pathlib -s happypath.py -arg output/pathlib test.test_pathlib
python3 -m spotflow -t logging -s happypath.py -arg output/logging test.test_logging
python3 -m spotflow -t difflib -s happypath.py -arg output/difflib test.test_difflib
python3 -m spotflow -t imaplib -s happypath.py -arg output/imaplib test.test_imaplib
python3 -m spotflow -t smtplib -s happypath.py -arg output/smtplib test.test_smtplib
python3 -m spotflow -t csv -s happypath.py -arg output/csv test.test_csv
python3 -m spotflow -t argparse -s happypath.py -arg output/argparse test.test_argparse
python3 -m spotflow -t configparser -s happypath.py -arg output/configparser test.test_configparser




# Other projects
#python3 -m spotflow -t rich -s happypath.py -arg output pytest -k 'not card and not markdown and not progress' lab/happypath/rich/tests
#thefuck
#six
#requests
#flask
#Cookiecutter
#Rich
#DateUtil