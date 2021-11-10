from happyflow.utils import *
from happyflow.templite import Templite


class HTMLReport:

    LOCAL_DIR = 'htmlfiles'
    INDEX_FILE = 'index.html'
    PY_FILE = 'pyfile2.html'
    STATIC_FILES = [
        "highlight.css"
    ]
    REPORT_DIR = 'report'

    def __init__(self, entity_info, analysis):
        self.entity_info = entity_info
        self.analysis = analysis

        pyfile_path = full_filename(self.LOCAL_DIR, self.PY_FILE)
        ensure_dir(self.REPORT_DIR)
        copy_files(self.LOCAL_DIR, self.STATIC_FILES, self.REPORT_DIR)

        self.pyfile_html_source = read_file(pyfile_path)
        self.source_tmpl = Templite(self.pyfile_html_source)

    def report(self):

        for flow_data in self.entity_info:

            flow_data.call_ratio = ratio(flow_data.call_count, self.entity_info.total_calls)

            for line_data in flow_data:

                if line_data.is_run():
                    line_data.html = f'<span class="full run">{line_data.html}</span>'
                if line_data.is_not_run():
                    line_data.html = f'<span class="full not_run">{line_data.html}</span>'

        html = self.source_tmpl.render({
            'entity_info': self.entity_info
        })

        pyfile = os.path.join(self.REPORT_DIR, self.entity_info.target_entity.full_name + '.html')
        write_html(pyfile, html)

