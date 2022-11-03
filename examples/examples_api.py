from spotflow.api import SpotFlow


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


flow = SpotFlow()
flow.target_methods([count_uppercase_words])

flow.start()

# code to be run and monitored
inputs_count()
flow.stop()

# the result is a MonitoredProgram object
monitored_program = flow.result()
monitored_program.show_objects()

