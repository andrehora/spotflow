[![Tests](https://github.com/andrehora/happyflow/actions/workflows/main.yml/badge.svg)](https://github.com/andrehora/happyflow/actions/workflows/main.yml)

# SpotFlow
SpotFlow is a tool to ease the runtime analysis of Python programs.
SpotFlow runs and monitors a target Python program.
With SpotFlow, you can easily extract information about executed lines, argument values, return values, variable states, and thrown exceptions.

## Install
```
pip install spotflow
```

## A quick example

```python
# content of demo.py
def sum(iter, start=0):
    count = start
    for i in iter:
        count += i
    return count

sum([1, 2]) # 3
```
To run and monitor it:
```
$ python -m happyflow -t sum demo
Running and monitoring: demo
================================
MonitoredProgram
- methods: 1
- calls: 1
MonitoredMethod
- name: __main__.sum
- calls: 1
MethodCall
- distinct_run_lines: [2, 3, 4, 5]
- run_lines: [2, 3, 4, 3, 4, 3, 5]
ArgState
- iter=[1, 2]
- start=0
VarStateHistory
- name: iter | values: [1, 2]
- name: start | values: 0
- name: count | values: 0, 1, 3
- name: i | values: 1, 2
ReturnState: 3

```