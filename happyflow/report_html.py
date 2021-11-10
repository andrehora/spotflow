from happyflow.utils import *
from happyflow.templite import Templite

LOCAL_DIR = 'htmlfiles'
INDEX_FILE = 'index.html'
PY_FILE = 'pyfile2.html'
INDEX_FILE = 'index.html'
STATIC_FILES = [
    "highlight.css",
    "style.css",
    "coverage_html.js"
]
REPORT_DIR = 'report'


class HTMLCodeReport:

    def __init__(self, entity_info):
        self.entity_info = entity_info

        pyfile_path = full_filename(LOCAL_DIR, PY_FILE)
        ensure_dir(REPORT_DIR)
        copy_files(LOCAL_DIR, STATIC_FILES, REPORT_DIR)

        pyfile_html_source = read_file(pyfile_path)
        self.source_tmpl = Templite(pyfile_html_source)

    def report(self):

        for flow_data in self.entity_info:
            for line_data in flow_data:
                if line_data.is_run():
                    line_data.html = f'<span class="full run">{line_data.html}</span>'
                if line_data.is_not_run():
                    line_data.html = f'<span class="full not_run">{line_data.html}</span>'

        html = self.source_tmpl.render({
            'entity_info': self.entity_info
        })

        pyfile = os.path.join(REPORT_DIR, self.entity_info.target_entity.full_name + '.html')
        write_html(pyfile, html)


class HTMLIndexReport:

    def __init__(self, summary):
        self.summary = summary

        index_path = full_filename(LOCAL_DIR, INDEX_FILE)
        ensure_dir(REPORT_DIR)
        # copy_files(LOCAL_DIR, STATIC_FILES, REPORT_DIR)

        index_html_source = read_file(index_path)
        self.source_tmpl = Templite(index_html_source)

    def report(self):

        html = self.source_tmpl.render({
            'summary': self.summary
        })

        index_file = os.path.join(REPORT_DIR, INDEX_FILE)
        write_html(index_file, html)
