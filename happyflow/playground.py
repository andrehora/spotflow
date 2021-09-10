from happyflow.flow import *
import happyflow.trace_inspect

trace_inspect.SUT_NAME = 'message.Message.add_header'

trace_result = TestRunner.trace('test.test_email.test_email.TestMessageAPI')
sut = SUTLoader.find_sut(trace_inspect.SUT_NAME)
flow_result = sut.local_flows(trace_result)
executable_lines = sut.executable_lines()

print(len(flow_result.flows))
for each in flow_result.flows:
    print(len(each.distinct_lines()), each.distinct_lines(), each.test_name)
print('executable_lines', len(executable_lines), executable_lines)
