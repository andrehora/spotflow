class Report:

    def __init__(self, flow_result):
        self.flow_result = flow_result.filter(flow_result.has_calls)
        self.flow_result.compute_flows()

    def html_report(self, report_dir):
        from happyflow.report_html import HTMLCodeReport, HTMLIndexReport
        print(f'Report size: {len(self.flow_result)}')
        count = 0
        for method_trace in self.flow_result:
            HTMLCodeReport(method_trace, report_dir).report()
            count += 1
            print(f'{count}. {method_trace.target_method.full_name}')
        HTMLIndexReport(self.flow_result, report_dir).report()

    def csv_report(self, report_dir):
        from happyflow.report_csv import CSVCodeReport, CSVIndexReport
        for method_trace in self.flow_result:
            CSVCodeReport(method_trace, report_dir).report()
        CSVIndexReport(self.flow_result, report_dir).report()

    def txt_report(self):
        from happyflow.report_txt import TextReport
        for method_trace in self.flow_result:
            TextReport(method_trace).report()