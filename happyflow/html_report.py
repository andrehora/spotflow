from happyflow.analysis import Analysis
from happyflow.utils import *
from happyflow.templite import Templite


class HTMLReport:

    def __init__(self, target_entity, flow_result):
        self.target_entity = target_entity
        self.flow_result = flow_result
        self.analysis = Analysis(self.target_entity, self.flow_result)

        self.pyfile_html_source = read_file("./happyflow/html/pyfile2.html")
        self.source_tmpl = Templite(self.pyfile_html_source)

    def report(self, flow_number=0):

        flow = self.flow_result.flows[flow_number]
        state_result = flow.state_result
        flow_lines = flow.run_lines

        content = read_file(self.target_entity.filename)
        html_lines = html_lines_for_code(content)
        current_line = 0
        lines = []
        for line in html_lines:
            current_line += 1
            if self.target_entity.has_line(current_line):

                if current_line in flow_lines:
                    line = f'<span class="happy">{line}</span>'
                if current_line not in flow_lines:
                    line = f'<span class="alter">{line}</span>'
                lines.append(line)

        html = self.source_tmpl.render({'lines': lines})
        write_html('./happyflow/html/example.html', html)
