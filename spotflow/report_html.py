import os
from spotflow.libs.templite import Templite
from spotflow.utils import full_filename, ensure_dir, copy_files, read_file, write_html


REPORT_DIR = 'spotflow_html_report'
LOCAL_DIR = 'htmlfiles'
INDEX_FILE = 'index.html'
PY_FILE = 'pyfile2.html'
INDEX_FILE = 'index.html'
STATIC_FILES = [
    "highlight.css",
    "style.css",
    "coverage_html.js"
]


class HTMLCodeReport:

    def __init__(self, monitored_method, report_dir=None):
        self.monitored_method = monitored_method

        self.report_dir = report_dir
        if not self.report_dir:
            self.report_dir = REPORT_DIR

        pyfile_path = full_filename(LOCAL_DIR, PY_FILE)
        ensure_dir(self.report_dir)
        copy_files(LOCAL_DIR, STATIC_FILES, self.report_dir)

        pyfile_html_source = read_file(pyfile_path)
        self.source_tmpl = Templite(pyfile_html_source)

    def report(self):

        # for flow in self.monitored_method.flows:
        #     for line in flow.info.lines:
        #         if line.is_run():
        #             line.html = f'<span class="full run">{line.html()}</span>'
        #         if line.is_not_run():
        #             line.html = f'<span class="full not_run">{line.html()}</span>'

        html = self.source_tmpl.render({
            'monitored_method': self.monitored_method
        })

        pyfile = os.path.join(self.report_dir, self.monitored_method.info.full_name + '.html')
        write_html(pyfile, html)


class HTMLIndexReport:

    def __init__(self, monitored_system, report_dir=None):
        self.monitored_system = monitored_system

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
            'monitored_system': self.monitored_system
        })

        index_file = os.path.join(self.report_dir, INDEX_FILE)
        write_html(index_file, html)
