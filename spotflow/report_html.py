import os
import re
from spotflow.libs.templite import Templite
from spotflow.utils import full_filename, full_dir, ensure_dir, copy_files, read_file
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import get_formatter_by_name


REPORT_DIR = 'report_html'
LOCAL_DIR = 'htmlfiles'
INDEX_FILE = 'index.html'
PY_FILE = 'pyfile2.html'
INDEX_FILE = 'index.html'
STATIC_FILES = [
    "highlight.css",
    "style.css",
    "coverage_html.js"
]


def write_html(filename, content):
    html = re.sub(r"(\A\s+)|(\s+$)", "", content, flags=re.MULTILINE) + "\n"
    with open(filename, "wb") as fout:
        fout.write(html.encode("ascii", "xmlcharrefreplace"))


def get_html_lines(code):
    html = html_for_code(code)
    lines = []
    for line in html.splitlines():
        line = line.replace('<div class="highlight"><pre><span></span>', "")
        line = line.replace("</pre></div>", "")
        lines.append(line)
    return lines


def html_for_code(code):
    lexer = get_lexer_by_name("python", stripall=True)
    formatter = get_formatter_by_name("html", style="friendly")
    return highlight(code, lexer, formatter)


class HTMLCodeReport:

    def __init__(self, monitored_method, report_dir=None):
        self.monitored_method = monitored_method

        self.report_dir = report_dir
        if not self.report_dir:
            self.report_dir = REPORT_DIR

        pyfile = full_filename(LOCAL_DIR, PY_FILE, __file__)
        self.report_dir = full_dir(self.report_dir, __file__)
        ensure_dir(self.report_dir)
        copy_files(LOCAL_DIR, STATIC_FILES, self.report_dir, __file__)

        pyfile_html_source = read_file(pyfile)
        self.source_tmpl = Templite(pyfile_html_source)

    def report(self):

        html = self.source_tmpl.render({'monitored_method': self.monitored_method})

        pyfile = os.path.join(self.report_dir, self.monitored_method.info.full_name + '.html')
        write_html(pyfile, html)


class HTMLIndexReport:

    def __init__(self, monitored_program, report_dir=None):
        self.monitored_program = monitored_program

        self.report_dir = report_dir
        if not self.report_dir:
            self.report_dir = REPORT_DIR

        index_path = full_filename(LOCAL_DIR, INDEX_FILE, __file__)
        self.report_dir = full_dir(self.report_dir, __file__)
        ensure_dir(self.report_dir)
        # copy_files(LOCAL_DIR, STATIC_FILES, REPORT_DIR)

        index_html_source = read_file(index_path)
        self.source_tmpl = Templite(index_html_source)

    def report(self):

        html = self.source_tmpl.render({
            'monitored_program': self.monitored_program
        })

        index_file = os.path.join(self.report_dir, INDEX_FILE)
        write_html(index_file, html)
