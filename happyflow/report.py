class Report:

    def __init__(self, monitored_system):
        self.monitored_system = monitored_system.filter(monitored_system.has_calls)
        self.monitored_system.compute_flows()

    def html_report(self, report_dir):
        from happyflow.report_html import HTMLCodeReport, HTMLIndexReport
        print(f'Report size: {len(self.monitored_system)}')
        count = 0
        for traced_method in self.monitored_system:
            HTMLCodeReport(traced_method, report_dir).report()
            count += 1
            print(f'{count}. {traced_method.info.full_name}')
        HTMLIndexReport(self.monitored_system, report_dir).report()

    def csv_report(self, report_dir):
        from happyflow.report_csv import CSVCodeReport, CSVIndexReport
        for traced_method in self.monitored_system:
            CSVCodeReport(traced_method, report_dir).report()
        CSVIndexReport(self.monitored_system, report_dir).report()

    def txt_report(self):
        from happyflow.report_txt import TextReport
        for traced_method in self.monitored_system:
            TextReport(traced_method).report()