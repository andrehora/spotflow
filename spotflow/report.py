from spotflow.info import PathInfo


def pprint_report(monitored_program):
    
    from spotflow.report_pprint import PrettyPrintReport

    for monitored_method in monitored_program:
        for call in monitored_method.calls:
            path_info = PathInfo(monitored_method, call)
            PrettyPrintReport(monitored_method, path_info).report()


def html_report(monitored_program, report_dir=None):
    
    from spotflow.report_html import HTMLCodeReport, HTMLIndexReport

    print(f'Report size: {len(monitored_program)}')
    count = 0
    for monitored_method in monitored_program:
        count += 1
        print(f'{count}. {monitored_method.info.full_name}')
        HTMLCodeReport(monitored_method, report_dir).report()
    HTMLIndexReport(monitored_program, report_dir).report()


def csv_report(monitored_program, report_dir=None):
    
    from spotflow.report_csv import CSVCodeReport, CSVIndexReport

    for monitored_method in monitored_program:
        CSVCodeReport(monitored_method, report_dir).report()
    CSVIndexReport(monitored_program, report_dir).report()
    