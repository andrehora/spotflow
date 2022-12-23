python3 -m spotflow -t rich -s lab/happypath/happypath.py -arg output pytest -k 'not card and not markdown and not progress' lab/happypath/rich/tests
python3 -m spotflow -t locale -s lab/happypath/happypath.py -arg locale test.test_locale

# running other projects
#python -m spotflow -t rich -d pytest rich/tests
#python -m spotflow -t dateutil pytest dateutil/test
#python -m spotflow -t rest_framework pytest tests
