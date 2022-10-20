# Get started with SpotFlow
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
sum([1, 2, 3]) # 7
```
To run and monitor it:
```shell
$ python -m spotflow -t sum demo
Running and monitoring: demo
====================== Result ======================
MonitoredProgram
- methods: 1
- calls: 2
MonitoredMethod
- name: __main__.sum
- calls: 2
MethodCall
- distinct_run_lines: [2, 3, 4, 5]
- run_lines: [2, 3, 4, 3, 4, 3, 5]
ArgState
- iter=[1, 2]
- start=0
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
- iter=[1, 2, 3]
- start=1
VarStateHistory
- iter: [1, 2, 3]
- start: 1
- count: 1, 2, 4, 7
- i: 1, 2, 3
ReturnState: 7
```

## todo