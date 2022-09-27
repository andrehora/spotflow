import os
import re
import inspect
import shutil
import trace
import types
import csv
from collections import Counter
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
    with open(filename, 'r', encoding="utf-8") as f:
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


def get_metadata(func_or_method):
    func = func_or_method
    class_name = None
    if isinstance(func_or_method, types.MethodType):
        func = func_or_method.__func__
        class_name = func_or_method.__self__.__class__.__name__

    module_name, name, filename, start_line, end_line, full_name, code = function_metadata(func)
    return module_name, class_name, name, filename, start_line, end_line, full_name, code


def function_metadata(func):

    func_code = func.__code__

    module_name = find_module_name(func_code.co_filename)
    name = func.__name__
    filename = func_code.co_filename
    full_name = find_full_name(func)

    code = inspect.getsource(func)
    start_line = func_code.co_firstlineno
    end_line = get_end_line(start_line, code)
    return module_name, name, filename, start_line, end_line, full_name, code


def find_full_name(func_or_method):
    try:
        module = func_or_method.__module__
        qualname = func_or_method.__qualname__

        return f'{module}.{qualname}'
    except Exception as e:
        return None


def get_end_line(start_line, source):
    loc = source.count('\n')
    return start_line + loc - 1


def check_is_generator_function(func_or_method):
    if inspect.isgeneratorfunction(func_or_method) or inspect.isgenerator(func_or_method):
        return None
    return func_or_method


def obj_value(obj):
    try:
        if is_definition(obj):
            return f'{obj.__qualname__} def'
        elif is_basic(obj) or is_safe_iterator(obj) or is_safe_set(obj) or is_safe_map(obj):
            return repr(obj)
        else:
            return obj.__class__.__qualname__
    except Exception as e:
        return type(obj).__qualname__


def obj_type(obj):
    return type(obj).__qualname__


def is_definition(obj):
    return obj.__class__.__name__ in ['type', 'module', 'function', 'method',
                                      'code', 'traceback', 'frame', 'generator', 'coroutine']


def is_basic(obj):
    return obj.__class__.__name__ in ['NoneType', 'bool', 'int', 'float', 'complex', 'str', 'range']


def is_safe_iterator(obj):
    if obj.__class__.__name__ in ['list', 'tuple']:
        if not obj:
            return True
        if obj and is_basic(obj[0]):
            return True
    return False


def is_safe_set(obj):
    if obj.__class__.__name__ in ['set', 'frozenset']:
        if not obj:
            return True
        for each in obj:
            # Only check the first element
            if is_basic(each):
                return True
            return False
    return False


def is_safe_map(obj):
    if obj.__class__.__name__ == 'dict':
        if not obj:
            return True
        for key in obj:
            # Only check the first element
            if is_basic(obj[key]):
                return True
            return False
    return False


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


def write_html(filename, content):
    html = re.sub(r"(\A\s+)|(\s+$)", "", content, flags=re.MULTILINE) + "\n"
    with open(filename, "wb") as fout:
        fout.write(html.encode('ascii', 'xmlcharrefreplace'))


def write_csv(filename, content):
    with open(filename, 'w') as fout:
        wr = csv.writer(fout, quoting=csv.QUOTE_ALL)
        wr.writerows(content)


def write_newline(filename, content):
    with open(filename, 'w') as fout:
        wr = csv.writer(fout)
        wr.writerows(content)


def write_txt(filename, content):
    with open(filename, 'w') as fout:
        fout.write(content)


def escape(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def line_intersection(lines, other_lines):
    return sorted(list(set(lines).intersection(other_lines)))


def find_executable_linenos(filename):
    return trace._find_executable_linenos(filename)


def is_method_or_func(entity):
    return inspect.ismethod(entity) or inspect.isfunction(entity)


def get_module_names(method_names):
    module_names = []
    for method_name in method_names:
        if isinstance(method_name, str):
            module_name = method_name.split('.')[0]
            module_names.append(module_name)
    return module_names


def ratio(a, b, dec=1):
    if b == 0:
        return 'NA'
    r = a / b * 100
    return round(r, dec)


def count_values(values, value1=True, value2=False):
    counter = Counter(values).most_common()
    counter_sorted = sorted(counter, reverse=True)
    if len(counter_sorted) == 1:
        element = counter_sorted[0]
        frequency = element[1]
        if element[0] == value1:
            return frequency, 0
        if element[0] == value2:
            return 0, frequency
    if len(counter_sorted) == 2:
        return counter_sorted[0][1], counter_sorted[1][1]
