from os import listdir
from os.path import isfile, join
from spotflow.utils import read_file_lines2


def list_files(folder):
    return {f for f in listdir(folder) if isfile(join(folder, f))}


def get_arg(hash_lines):
    return tuple(hash_lines[0:-1])


def get_return(hash_lines):
    return hash_lines[-1]


class ArgReturnValue:

    def __init__(self, arg_value, return_value, is_new):
        self.arg_value = arg_value
        self.return_value = return_value
        self._is_new = is_new

    def is_new(self):
        return self._is_new

    def is_old(self):
        return not self.is_new()

    def __repr__(self):
        if self.is_new():
            return f'New return: {self.return_value}'
        return f'Old return: {self.return_value}'


class ChangeRepository:

    def __init__(self, project, old_dir, new_dir):
        self.project = project
        self.old_dir = old_dir
        self.new_dir = new_dir
        self.arg_return_values = {}
        self.build()

    def build(self):

        old_files = list_files(self.old_dir)
        new_files = list_files(self.new_dir)

        new_files_only = new_files - old_files
        old_files_only = old_files - new_files
        print('new_files_only', len(new_files_only))
        print('old_files_only', len(old_files_only))

        for each in new_files_only:
            hash_lines = read_file_lines2(self.new_dir + '/' + each)
            arg_value = get_arg(hash_lines)
            return_value = get_return(hash_lines)
            v = ArgReturnValue(arg_value, return_value, is_new=True)
            self.add_new(v)

        for each in old_files_only:
            hash_lines = read_file_lines2(self.old_dir + '/' + each)
            arg_value = get_arg(hash_lines)
            return_value = get_return(hash_lines)
            v = ArgReturnValue(arg_value, return_value, is_new=False)
            self.add_old(v)

    def find_changes(self):
        for arg_value in self.arg_return_values:
            return_value = self.arg_return_values[arg_value]
            if len(return_value) >= 2:
                print('Returns:', len(return_value))
                print('Argument:', arg_value)
                for each_return in return_value:
                    print(each_return)

    def add_new(self, v):
        if v.arg_value in self.arg_return_values:
            self.arg_return_values[v.arg_value].append(v)
        else:
            self.arg_return_values[v.arg_value] = [v]

    def add_old(self, v):
        if v.arg_value in self.arg_return_values:
            self.arg_return_values[v.arg_value].append(v)



