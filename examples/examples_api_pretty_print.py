from spotflow.api import pprint


def absolute(x):
    if x < 0:
        return -x
    return x


def inputs_aboslute():
    absolute(10)
    absolute(-10)


def count_uppercase_words(text):
    counter = 0
    for word in text.split():
        if word.isupper():
            counter += 1
    return counter


def inputs_count():
    count_uppercase_words('')
    count_uppercase_words('ABC DEF')
    count_uppercase_words('abc')


pprint(inputs_aboslute, [absolute])
pprint(inputs_count, [count_uppercase_words])
