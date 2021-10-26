import os
import re
import inspect
import logging
import copy
# from pygments import highlight
# from pygments.lexers import get_lexer_by_name
# from pygments.formatters import get_formatter_by_name


def open_file(filename):
    try:
        with open(filename, 'r', encoding="utf-8") as f:
            return f.read()
    except:
        return None


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


def find_module_name(filename):
    return filename.split('/')[-1].split('.')[0]


def find_class_name(frame):
    args = inspect.getargvalues(frame)
    if 'self' in args.locals:
        obj = args.locals['self']
        try:
            return obj.__class__.__name__
        except Exception:
            return None
    return None


def find_full_entity_name(frame):
    code = frame.f_code
    module_name = find_module_name(code.co_filename)
    class_name = find_class_name(frame)
    function_name = code.co_name
    if class_name:
        return f'{module_name}.{class_name}.{function_name}'
    return f'{module_name}.{function_name}'


def line_intersection(lines, other_lines):
    return sorted(list(set(lines).intersection(other_lines)))


def function_metadata(func):
    module_name = find_module_name(func.__code__.co_filename)
    name = func.__name__
    filename = func.__code__.co_filename

    source = inspect.getsource(func)

    start_line = func.__code__.co_firstlineno
    end_line = get_end_line(start_line, source)
    return module_name, name, filename, start_line, end_line


def method_metadata(method):
    func = method.__func__
    class_name = (method.__self__.__class__.__name__)
    module_name, name, filename, start_line, end_line = function_metadata(func)

    return module_name, class_name, name, filename, start_line, end_line


def get_end_line(start_line, source):
    loc = source.count('\n')
    return start_line + loc - 1


def line_has_explicit_return(frame):
    traceback = inspect.getframeinfo(frame)
    if len(traceback.code_context) >= 1:
        code_line = traceback.code_context[0].strip()
        # __return__ = eval(code_line.split()[1], frame.f_globals, frame.f_locals)
        # print(__return__)
        return code_line.startswith('return')
    return False


def diff(list1, list2):
    second = set(list2)
    return [item for item in list1 if item not in second]


def clear_element(element):

    if is_hashable(element):
        return element

    if is_list_or_set(element):
        t = []
        for each in element:
            t.append(element_or_type(each))
        return tuple(t)

    return element_or_type(element)


def element_or_type(element):
    if is_hashable(element):
        return element
    return element.__class__.__name__


def is_hashable(element):
    try:
        hash(element)
        return True
    except TypeError:
        return False


def is_list_or_set(element):
    return type(element) == list or type(element) == set


def read_file(filename):
    with open(filename) as f:
        return f.read()


def read_file_lines(filename):
    with open(filename) as f:
        return f.readlines()


# def html_for_code(code):
#     lexer = get_lexer_by_name("python", stripall=True)
#     formatter = get_formatter_by_name("html", style="friendly")
#     return highlight(code, lexer, formatter)


# def html_lines_for_code(code):
#     html = html_for_code(code)
#     lines = []
#     for line in html.splitlines():
#         line = line.replace('<div class="highlight"><pre><span></span>', '')
#         line = line.replace('</pre></div>', '')
#         lines.append(line)
#     return lines


def write_html(fname, html):
    html = re.sub(r"(\A\s+)|(\s+$)", "", html, flags=re.MULTILINE) + "\n"
    with open(fname, "wb") as fout:
        fout.write(html.encode('ascii', 'xmlcharrefreplace'))


def copy_or_type(obj):
    try:
        return copy.deepcopy(obj)
    except Exception:
        return guess_name(obj)


def guess_name(obj):
    try:
        obj_string = str(obj)
        if obj_string.startswith('<') and obj_string.endswith('>'):
            if inspect.ismodule(obj) or inspect.isclass(obj) or inspect.ismethod(obj) or inspect.isfunction(obj):
                return f'{obj.__name__} class'
            return f'{obj.__class__.__name__} object'
        return obj_string
    except Exception:
        return obj_string


def try_copy(obj, name):
    try:
        return copy.deepcopy(obj)
    except Exception:
        logging.warning(f'Copy error: {name} {str(obj)}')
        raise


