import inspect
import copy


class SUTStateResult:

    def __init__(self, name):
        self.sut_name = name
        self.vars = {}

    def add(self, name, value, line):
        self.vars[name] = self.vars.get(name, SUTVarStateHistory(name, []))
        self.vars[name].add(name, value, line)


class SUTVarStateHistory:

    def __init__(self, name, states):
        self.name = name
        self.states = states

    def add(self, name, value, line):
        state = SUTVarState(name, value, line)
        self.states.append(state)


    def first_last(self):
        if len(self.values) == 1:
            return self.values[0], self.values[0]
        return self.values[0], self.values[-1]

    def distinct_values_str(self):
        str_values = {}
        for value in self.values:
            if str(value) not in str_values:
                str_values[str(value)] = None
        return str_values.keys()

    def distinct_sequential_values(self):
        distinct = []
        b = None
        for a in self.values:
            if a != b:
                distinct.append(a)
            b = a
        return distinct

    def distinct_values(self):
        str_values = {}
        for value in self.values:
            if value not in str_values:
                str_values[value] = None
        return str_values.keys()

    def __str__(self):
        return f'name: {self.name}, values: {len(self.states)}'


class SUTVarState:

    def __init__(self, name, value, line):
        self.name = name
        self.value = value
        self.line = line

def find_module_name(filename):
    return filename.split('/')[-1].split('.')[0]


def find_class_name(frame):
    args = inspect.getargvalues(frame)
    if 'self' in args.locals:
        obj = args.locals['self']
        return str(obj.__class__.__name__)
    return None


def find_full_func_name(frame):
    code = frame.f_code
    module_name = find_module_name(code.co_filename)
    class_name = find_class_name(frame)
    function_name = code.co_name
    if class_name:
        return f'{module_name}.{class_name}.{function_name}'
    return f'{module_name}.{function_name}'


SUT_NAME = ''
all_sut_flows = {}
all_sut_states = {}
COLLECT_STATE = False


def clean_inspection():
    global all_sut_flows, all_sut_states
    all_sut_flows = {}
    all_sut_states = {}


def collect_flow_and_state(frame, data_type, test_name, why):

    entity_name = find_full_func_name(frame)

    if entity_name.startswith(SUT_NAME):
        if entity_name not in all_sut_flows:
            all_sut_flows[entity_name] = []

        if data_type == 'global':
            sut_flows = all_sut_flows[entity_name]

            state = None
            if COLLECT_STATE:
                state = SUTStateResult(entity_name)

            sut_flows.append((test_name, [], state))

        if data_type == 'local':
            sut_flows = all_sut_flows[entity_name]
            # get the last flow and update it
            test_name, last_flow, last_state_result = sut_flows[-1]

            lineno = frame.f_lineno
            if why == 'line':
                last_flow.append(lineno)

            if last_state_result:

                argvalues = inspect.getargvalues(frame)

                if 'self' in argvalues.locals:
                    self = argvalues.locals['self']
                    value = copy.copy(self)
                    last_state_result.add(name='self', value=value, line=lineno)

                for argvalue in argvalues.locals:
                    value = copy.copy(argvalues.locals[argvalue])
                    last_state_result.add(name=argvalue, value=value, line=lineno)