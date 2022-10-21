class Report:

    def __init__(self, monitored_system):
        self.monitored_system = monitored_system

    def html_report(self, report_dir):
        from spotflow.report_html import HTMLCodeReport, HTMLIndexReport
        print(f'Report size: {len(self.monitored_system)}')
        count = 0
        for monitored_method in self.monitored_system:
            HTMLCodeReport(monitored_method, report_dir).report()
            count += 1
            print(f'{count}. {monitored_method.info.full_name}')
        HTMLIndexReport(self.monitored_system, report_dir).report()

    def csv_report(self, report_dir):
        from spotflow.report_csv import CSVCodeReport, CSVIndexReport
        for monitored_method in self.monitored_system:
            CSVCodeReport(monitored_method, report_dir).report()
        CSVIndexReport(self.monitored_system, report_dir).report()

    def txt_report(self):
        from spotflow.report_txt import TextReport
        for monitored_method in self.monitored_system:
            TextReport(monitored_method).report()