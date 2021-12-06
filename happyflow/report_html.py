from happyflow.utils import *
from happyflow.libs.templite import Templite

LOCAL_DIR = 'htmlfiles'
INDEX_FILE = 'index.html'
PY_FILE = 'pyfile2.html'
INDEX_FILE = 'index.html'
STATIC_FILES = [
    "highlight.css",
    "style.css",
    "coverage_html.js"
]
REPORT_DIR = 'report_html'


class HTMLCodeReport:

    def __init__(self, method_trace, report_dir=None):
        self.method_trace = method_trace

        self.report_dir = report_dir
        if not self.report_dir:
            self.report_dir = REPORT_DIR

        pyfile_path = full_filename(LOCAL_DIR, PY_FILE)
        ensure_dir(self.report_dir)
        copy_files(LOCAL_DIR, STATIC_FILES, self.report_dir)

        pyfile_html_source = read_file(pyfile_path)
        self.source_tmpl = Templite(pyfile_html_source)

    def report(self):

        for flow in self.method_trace.flows:
            for line in flow.info.lines:
                if line.is_run():
                    line.html = f'<span class="full run">{line.html}</span>'
                if line.is_not_run():
                    line.html = f'<span class="full not_run">{line.html}</span>'

        html = self.source_tmpl.render({
            'method_trace': self.method_trace
        })

        pyfile = os.path.join(self.report_dir, self.method_trace.target_method.full_name + '.html')
        write_html(pyfile, html)


class HTMLIndexReport:

    def __init__(self, flow_result, report_dir=None):
        self.flow_result = flow_result

        self.report_dir = report_dir
        if not self.report_dir:
            self.report_dir = REPORT_DIR

        index_path = full_filename(LOCAL_DIR, INDEX_FILE)
        ensure_dir(self.report_dir)
        # copy_files(LOCAL_DIR, STATIC_FILES, REPORT_DIR)

        index_html_source = read_file(index_path)
        self.source_tmpl = Templite(index_html_source)

    def report(self):

        html = self.source_tmpl.render({
            'flow_result': self.flow_result
        })

        index_file = os.path.join(self.report_dir, INDEX_FILE)
        write_html(index_file, html)
