class Report:

    def __init__(self, monitored_program):
        self.monitored_program = monitored_program

    def html_report(self, report_dir):
        from lab.happypath.report_html import HTMLCodeReport, HTMLIndexReport
        print(f'Report size: {len(self.monitored_program)}')
        count = 0
        for monitored_method in self.monitored_program:
            HTMLCodeReport(monitored_method, report_dir).report()
            count += 1
            print(f'{count}. {monitored_method.info.full_name}')
        HTMLIndexReport(self.monitored_program, report_dir).report()

    def csv_report(self, report_dir):
        from lab.happypath.report_csv import CSVCodeReport, CSVIndexReport
        for monitored_method in self.monitored_program:
            CSVCodeReport(monitored_method, report_dir).report()
        CSVIndexReport(self.monitored_program, report_dir).report()

