[![Tests](https://github.com/andrehora/spotflow/actions/workflows/main.yml/badge.svg)](https://github.com/andrehora/spotflow/actions/workflows/main.yml)

# SpotFlow

SpotFlow is a tool to ease the runtime analysis of Python programs.
With SpotFlow, you can easily extract information about executed methods, run lines, argument values, return values, variable states, and thrown exceptions.

## Install

```
pip install spotflow
```

## Quick usage

A simple code to be monitored in `sample.py`:

```python
# content of sample.py
def absolute(x):
    if x < 0:
        x = -x
    return x

absolute(-10) # 10
```

To run and monitor function `absolute` in `sample.py`:
```
$ python -m spotflow -t absolute sample
```

The result:
```
Running and monitoring: sample
====================== Result ======================
MonitoredProgram
- methods: 1
- calls: 1
MonitoredMethod
- name: absolute
- calls: 1
MethodCall
- distinct_run_lines: [2, 3, 4]
- run_lines: [2, 3, 4]
ArgState
- x: -10
VarStateHistory
- x: -10, 10
ReturnState: 10
```

---

Another code to be monitored in `sample.py`, with two calls:

```python
# content of sample.py
def sum(iter, start=0):
    count = start
    for i in iter:
        count += i
    return count

sum([1, 2]) # 3
sum([1, 2, 3], 1) # 7
```

To run and monitor function `sum` in `sample.py`:
```
$ python -m spotflow -t sum sample
```

The result:
```
Running and monitoring: sample
====================== Result ======================
MonitoredProgram
- methods: 1
- calls: 2
MonitoredMethod
- name: sum
- calls: 2
MethodCall
- distinct_run_lines: [2, 3, 4, 5]
- run_lines: [2, 3, 4, 3, 4, 3, 5]
ArgState
- iter: [1, 2]
- start: 0
VarStateHistory
- iter: [1, 2]
- start: 0
- count: 0, 1, 3
- i: 1, 2
ReturnState: 3
MethodCall
- distinct_run_lines: [2, 3, 4, 5]
- run_lines: [2, 3, 4, 3, 4, 3, 4, 3, 5]
ArgState
- iter: [1, 2, 3]
- start: 1
VarStateHistory
- iter: [1, 2, 3]
- start: 1
- count: 1, 2, 4, 7
- i: 1, 2, 3
ReturnState: 7
```

---

You can also monitor tests.
For example, to monitor the test case [`TestMessageAPI`](https://github.com/python/cpython/blob/4702552885811d0af8f0e4545f494336801ad4dd/Lib/test/test_email/test_email.py#L55
) of the Python Standard Library [`email`](https://docs.python.org/3/library/email.examples.html):

```
$ python -m spotflow -t email unittest test.test_email.test_email.TestMessageAPI
```

Monitoring other tests of the Python Standard Library:
```
$ python -m spotflow -t ast unittest test.test_ast
$ python -m spotflow -t gzip unittest test.test_gzip
$ python -m spotflow -t urllib unittest test.test_urlparse
$ python -m spotflow -t json unittest test.test_json
$ python -m spotflow -t calendar unittest test.test_calendar
```

## Usage

SpotFlow can be run from the command-line or programmatically via API.

### Command-line

We can use SpotFlow to collect data from the execution of any Python program.
For example, to run `my_program.py`, we could originally use the following command-line:

```
# Running a Python program
$ python -m my_program
```

The same program can be run (and monitored) under SpotFlow with following command-line:
```
# Running a Python program + SpotFlow
$ python -m spotflow -t <target> my_program
```

The argument `-t` represents the target entity to be monitored.
We can pass the full name of the target method (in the format `module.Class.method`) or a prefix to monitor multiple methods.
For example, we can pass the prefix 
`parser` (to monitor all methods of a specific module), 
`parser.StringParser` (to monitor all methods of a specific class),
or the full method name (to monitor a single method).
The final mandatory argument is the original command-line, which is in this case `my_program`.

In a similar way, we can use SpotFlow to monitor the execution of test suites.
For example, to run a test `testX.py` under SpotFlow, the following change would be needed with the unittest framework:

```
# Running unittest
$ python -m unittest testX

# Running unittest + SpotFlow
$ python -m spotflow -t <target> unittest testX
```

### API

The other way to run SpotFlow is via its API.
For example, consider a function called `my_program()`.
It can be run and monitored with SpotFlow with the following code:

```python
flow = SpotFlow()
flow.target_methods(target)

flow.start()

# code to be run and monitored
my_program()

flow.stop()

# the result is a MonitoredProgram object
monitored_program = flow.result()
```

Class `SpotFlow` represents the programmatic access to SpotFlow.
In method `target_methods()`, we can pass the target entities to be monitored, which can be the full name of the target method or a prefix to monitor multiple methods, like in the command-line.
Method `start()` starts the monitoring.
The monitoring only occurs in code called after `start()`.
After calling `start()`, we must also call `stop()` to stop the monitoring.
Lastly, method `result()` provides a `MonitoredProgram` object.

## Monitored entities

- `MonitoredProgram`: This class is a repository of monitored methods, which can be used to access all collected data.

- `MonitoredMethod`: It represents a monitored method (or function). It has method calls and contains static information about the method/function, like name, full name, class name (for methods), file name, LOC, source code, etc.


- `MethodCall`: This class represents a method call that happens at runtime. It includes data about the caller, call stack, and executed lines. A method call also has a call state, which records information like variable and argument states.

- `CallState`: This class holds the state of a method call, with information about argument states (`ArgState`), return states (`ReturnState`), thrown exceptions (`ExceptionState`), and local variable states (`VarStateHistory`).

- `State`: It represents a state at runtime, such as a variable, argument, return, or exception state.
All states have information about its runtime value, runtime type, and line number in code.
In addition, `VarState` and `ArgState` have information about its name.

- `VarStateHistory`: This class holds all the states of a local variable in a method call. Notice that it is composed of variable states, representing the fact that a variable may change its value and therefore can have multiple states over time.