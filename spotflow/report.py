from spotflow.report_html import HTMLCodeReport, HTMLIndexReport
from spotflow.report_csv import CSVCodeReport, CSVIndexReport


def html_report(monitored_program, report_dir):
    print(f'Report size: {len(monitored_program)}')
    count = 0
    for monitored_method in monitored_program:
        HTMLCodeReport(monitored_method, report_dir).report()
        count += 1
        print(f'{count}. {monitored_method.info.full_name}')
    HTMLIndexReport(monitored_program, report_dir).report()


def csv_report(monitored_program, report_dir):
    for monitored_method in monitored_program:
        CSVCodeReport(monitored_method, report_dir).report()
    CSVIndexReport(monitored_program, report_dir).report()
    