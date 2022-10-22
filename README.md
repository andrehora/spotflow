[![Tests](https://github.com/andrehora/spotflow/actions/workflows/main.yml/badge.svg)](https://github.com/andrehora/spotflow/actions/workflows/main.yml)

# SpotFlow

SpotFlow is a tool to ease the runtime analysis of Python programs.
With SpotFlow, you can easily extract information about executed lines, argument values, return values, variable states, and thrown exceptions.

## Install

```
pip install spotflow
```

## A quick example

A simple code to be monitored:

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
============= Result =============
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

Another code to be monitored, with two calls:

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
============= Result =============
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