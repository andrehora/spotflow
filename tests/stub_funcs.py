def inputs_count():
    count_uppercase_words('')
    count_uppercase_words('a b')
    count_uppercase_words('A B C')


def count_uppercase_words(text):
    counter = 0
    for word in text.split():
        if word.isupper():
            counter += 1
    return counter


def inputs_parseparam():
    parseparam('a')
    parseparam('a=1;b=2')
    parseparam('a="1;1"')


def parseparam(s):
    s = ';' + str(s)
    plist = []
    while s[:1] == ';':
        s = s[1:]
        end = s.find(';')
        while end > 0 and (s.count('"', 0, end) - s.count('\\"', 0, end)) % 2:
            end = s.find(';', end + 1)
        if end < 0:
            end = len(s)
        f = s[:end]
        if '=' in f:
            i = f.index('=')
            f = f[:i].strip().lower() + '=' + f[i+1:].strip()
        plist.append(f.strip())
        s = s[end:]
    return plist


def inputs_splitparam():
    splitparam("a;b")
    splitparam("a")


def splitparam(param):
    a, sep, b = str(param).partition(';')
    if not sep:
        return a.strip(), None
    return a.strip(), b.strip()





