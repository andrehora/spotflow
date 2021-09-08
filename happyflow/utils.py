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


def find_full_func_name(frame):
    code = frame.f_code
    module_name = find_module_name(code.co_filename)
    class_name = find_class_name(frame)
    function_name = code.co_name
    if class_name:
        return f'{module_name}.{class_name}.{function_name}'
    return f'{module_name}.{function_name}'