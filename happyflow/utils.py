import os
import re
import inspect
import shutil
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import get_formatter_by_name


def find_python_files(dir='.'):
    if dir.endswith('.py'):
        return [dir]
    python_files = []
    for r, d, f in os.walk(dir):
        for file in f:
            if file.endswith('.py'):
                abs_dir = os.path.join(os.getcwd(), r, file)
                # if 'test' not in abs_dir:
                python_files.append(os.path.abspath(abs_dir))
    return python_files


def open_file(filename):
    try:
        with open(filename, 'r', encoding="utf-8") as f:
            return f.read()
    except:
        return None


def read_file(filename):
    with open(filename) as f:
        return f.read()


def read_file_lines(filename):
    with open(filename) as f:
        return f.readlines()


def copy_files(local_dir, files, destination):
    for static in files:
        shutil.copyfile(full_filename(local_dir, static), os.path.join(destination, static))


def ensure_dir(directory):
    if directory:
        os.makedirs(directory, exist_ok=True)


def full_filename(local_dir, filename):
    dir_path = os.path.dirname(__file__)
    return os.path.join(dir_path, local_dir, filename)


def find_module_name(filename):
    return filename.split('/')[-1].split('.')[0]


def method_metadata(method):
    func = method.__func__
    class_name = (method.__self__.__class__.__name__)
    module_name, name, filename, start_line, end_line, full_name = function_metadata(func)
    return module_name, class_name, name, filename, start_line, end_line, full_name


def function_metadata(func):
    module_name = find_module_name(func.__code__.co_filename)
    name = func.__name__
    filename = func.__code__.co_filename
    full_name = find_full_name(func)

    source = inspect.getsource(func)

    start_line = func.__code__.co_firstlineno
    end_line = get_end_line(start_line, source)
    return module_name, name, filename, start_line, end_line, full_name


def get_end_line(start_line, source):
    loc = source.count('\n')
    return start_line + loc - 1


def check_is_generator_function(func_or_method):
    if inspect.isgeneratorfunction(func_or_method):
        return None
    return func_or_method


def find_full_name(func_or_method):
    return f'{func_or_method.__module__}.{func_or_method.__qualname__}'


def line_has_explicit_return(frame):
    traceback = inspect.getframeinfo(frame)
    if traceback.code_context and len(traceback.code_context) >= 1:
        code_line = traceback.code_context[0].strip()
        # __return__ = eval(code_line.split()[1], frame.f_globals, frame.f_locals)
        # print(__return__)
        return code_line.startswith('return')
    return False


def get_obj_value(obj):
    obj_string = ''
    try:
        obj_string = repr(obj)
        if obj_string.startswith('<') and obj_string.endswith('>'):
            if is_definition(obj):
                return f'{obj.__name__} def'
            return f'{obj.__class__.__name__} obj'
        return obj_string
    except Exception as e:
        return obj_string


def is_definition(obj):
    return inspect.ismodule(obj) or inspect.isclass(obj) or inspect.ismethod(obj) or inspect.isfunction(obj)
    # inspect.isgeneratorfunction(obj) or inspect.isgenerator(obj)


def get_code_lines(entity):
    lines = read_file_lines(entity.filename)
    code_lines = []
    lineno = 0
    for line in lines:
        lineno += 1
        if entity.has_lineno(lineno):
            code_lines.append(line)
    return code_lines


def get_html_lines(code):
    html = html_for_code(code)
    lines = []
    for line in html.splitlines():
        line = line.replace('<div class="highlight"><pre><span></span>', '')
        line = line.replace('</pre></div>', '')
        lines.append(line)
    return lines


def html_for_code(code):
    lexer = get_lexer_by_name("python", stripall=True)
    formatter = get_formatter_by_name("html", style="friendly")
    return highlight(code, lexer, formatter)


def write_html(fname, html):
    html = re.sub(r"(\A\s+)|(\s+$)", "", html, flags=re.MULTILINE) + "\n"
    with open(fname, "wb") as fout:
        fout.write(html.encode('ascii', 'xmlcharrefreplace'))


def line_intersection(lines, other_lines):
    return sorted(list(set(lines).intersection(other_lines)))


def ratio(a, b, dec=1):
    r = a / b * 100
    return f'{round(r, dec)}%'