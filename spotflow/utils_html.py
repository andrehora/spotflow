import re
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import get_formatter_by_name


def write_html(filename, content):
    html = re.sub(r"(\A\s+)|(\s+$)", "", content, flags=re.MULTILINE) + "\n"
    with open(filename, "wb") as fout:
        fout.write(html.encode("ascii", "xmlcharrefreplace"))


def get_html_lines(code):
    html = code_as_html(code)
    lines = []
    for line in html.splitlines():
        line = line.replace('<div class="highlight"><pre><span></span>', "")
        line = line.replace("</pre></div>", "")
        lines.append(line)
    return lines


def code_as_html(code):
    lexer = get_lexer_by_name("python", stripall=True)
    formatter = get_formatter_by_name("html", style="friendly")
    return highlight(code, lexer, formatter)