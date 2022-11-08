from spotflow.api import monitor


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


monitored_program = monitor(inputs_count, [count_uppercase_words])
monitored_program.show_objects()

