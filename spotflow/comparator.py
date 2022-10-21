OLD_FILE = 'old.txt'
NEW_FILE = 'new.txt'


def find_distinct_in_file(old_file=OLD_FILE, new_file=NEW_FILE):
    old = set(_read_file_lines(old_file))
    new = set(_read_file_lines(new_file))
    return find_distinct_in_set(old, new)


def find_distinct_in_set(old, new):
    return new ^ old


def _read_file_lines(filename):
    with open(filename, 'r', encoding="utf-8") as f:
        return f.read().splitlines()
