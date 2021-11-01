from happyflow.analysis import Analysis
from happyflow.utils import *
from happyflow.templite import Templite


class HTMLReport:

    def __init__(self, entity_data, analysis):
        self.entity_data = entity_data
        self.analysis = analysis

        self.pyfile_html_source = read_file("./html/pyfile2.html")
        self.source_tmpl = Templite(self.pyfile_html_source)

    def report(self):

        for flow_data in self.entity_data:

            flow_data.call_ratio = ratio(flow_data.call_count, self.entity_data.total_calls)

            for line_data in flow_data:

                if line_data.is_run():
                    line_data.html = f'<span class="full run">{line_data.html}</span>'
                if line_data.is_not_run():
                    line_data.html = f'<span class="full not_run">{line_data.html}</span>'

        html = self.source_tmpl.render({
            'entity_data': self.entity_data
        })
        write_html(f'./html/{self.entity_data.full_name}.html', html)

    def pluralize(self, value):
        if value >= 2:
            return 's'
        return ''

