import os
import inspect


def open_file(filename):
    try:
        # print(filename)
        with open(filename, 'r', encoding="utf-8") as f:
            return f.read()
    except:
        return None


def find_python_files(dir='.'):
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
        return str(obj.__class__.__name__)
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
        return code_line.startswith('return')
    return False


def diff(list1, list2):
    second = set(list2)
    return [item for item in list1 if item not in second]
