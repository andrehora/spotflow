class Report:

    def __init__(self, traced_system):
        self.traced_system = traced_system.filter(traced_system.has_calls)
        self.traced_system.compute_flows()

    def html_report(self, report_dir):
        from happyflow.report_html import HTMLCodeReport, HTMLIndexReport
        print(f'Report size: {len(self.traced_system)}')
        count = 0
        for traced_method in self.traced_system:
            HTMLCodeReport(traced_method, report_dir).report()
            count += 1
            print(f'{count}. {traced_method.info.full_name}')
        HTMLIndexReport(self.traced_system, report_dir).report()

    def csv_report(self, report_dir):
        from happyflow.report_csv import CSVCodeReport, CSVIndexReport
        for traced_method in self.traced_system:
            CSVCodeReport(traced_method, report_dir).report()
        CSVIndexReport(self.traced_system, report_dir).report()

    def txt_report(self):
        from happyflow.report_txt import TextReport
        for traced_method in self.traced_system:
            TextReport(traced_method).report()