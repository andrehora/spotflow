from happyflow.analysis import Analysis
from happyflow.utils import *
from happyflow.templite import Templite


class HTMLReport:

    def __init__(self, entity_info, analysis):
        self.entity_info = entity_info
        self.analysis = analysis

        self.pyfile_html_source = read_file("./html/pyfile2.html")
        self.source_tmpl = Templite(self.pyfile_html_source)

    def report(self):

        for flow_state_info in self.entity_info:

            flow_state_info.call_ratio = ratio(flow_state_info.call_count, self.entity_info.total_calls)

            for line_info in flow_state_info:

                if line_info.is_run():
                    line_info.html = f'<span class="full run">{line_info.html}</span>'
                if line_info.is_not_run():
                    line_info.html = f'<span class="full not_run">{line_info.html}</span>'

        html = self.source_tmpl.render({
            'entity_info': self.entity_info
        })
        write_html('./html/example.html', html)
