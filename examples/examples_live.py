from happyflow.api import live


def count_uppercase_words(text):
    counter = 0
    for word in text.split():
        if word.isupper():
            counter += 1
    return counter


def inputs_count():
    # count_uppercase_words('')
    count_uppercase_words('ABC DEF')
    print()
    count_uppercase_words('abc')

live(inputs_count, [count_uppercase_words])
