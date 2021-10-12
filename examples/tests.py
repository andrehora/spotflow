
def count_uppercase_words(text):
    counter = 0
    for word in text.split():
        if word.isupper():
            counter += 1
    return counter


def test_count_0():
    print('test_count_0')
    assert count_uppercase_words('a b') == 0


def test_count_1():
    print('test_count_1')
    assert count_uppercase_words('A b') == 1


def test_count_2():
    print('test_count_2')
    assert count_uppercase_words('A B') == 2
