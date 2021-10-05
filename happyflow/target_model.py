import trace
import types
from happyflow.utils import line_intersection
from happyflow.utils import function_metadata, method_metadata


class TargetBaseEntity:

    def __init__(self, name, filename):
        self.name = name
        self.filename = filename

    def __str__(self):
        return self.full_name()

    def global_flows(self, trace_result):
        return trace_result.global_sut_flows(self)

    def local_flows(self, trace_result):
        return trace_result.local_sut_flows(self)

    def loc(self):
        pass

    def executable_lines(self):
        pass

    def full_name(self):
        pass


class TargetContainerEntity(TargetBaseEntity):

    def __init__(self, name, filename):
        super().__init__(name, filename)
        self.target_entities = []

    def __iter__(self):
        return iter(self.target_entities)

    def add_entity(self, func_or_method):
        self.target_entities.append(func_or_method)

    def loc(self):
        total_loc = 0
        for target_entity in self.target_entities:
            total_loc += target_entity.loc()
        return total_loc

    def executable_lines(self):
        all_executable_lines = []
        for target_entity in self.target_entities:
            all_executable_lines.append(target_entity.executable_lines())
        return tuple(all_executable_lines)

    def summary(self):
        return f'{self.full_name()} (target entities: {len(self.target_entities)})'


class TargetEntity(TargetBaseEntity):
    start_line = 0
    end_line = 0

    def __iter__(self):
        return iter([self])

    def executable_lines(self):
        executable_lines = trace._find_executable_linenos(self.filename)
        # remove the target_entity definition, eg, def, class
        return tuple(self.intersection(executable_lines)[1:])

    def intersection(self, other_lines):
        my_lines = range(self.start_line, self.end_line + 1)
        return line_intersection(my_lines, other_lines)

    def loc(self):
        return self.end_line - self.start_line

    def line_is_executable(self, line):
        return line in self.executable_lines()

    def line_is_definition(self, line):
        return line == self.start_line

    def has_line(self, line):
        return line in range(self.start_line, self.end_line + 1)

    def summary(self):
        return f'{self.full_name()} (lines: {self.start_line}-{self.end_line})'

    @classmethod
    def build_from_func(cls, func_or_method):

        target_entity = None

        if isinstance(func_or_method, types.MethodType):
            module_name, class_name, name, filename, start_line, end_line = method_metadata(func_or_method)
            target_entity = TargetMethod(module_name, class_name, name, filename)

        if isinstance(func_or_method, types.FunctionType):
            module_name, name, filename, start_line, end_line = function_metadata(func_or_method)
            target_entity = TargetFunction(module_name, name, filename)

        target_entity.start_line = start_line
        target_entity.end_line = end_line

        return target_entity

    @classmethod
    def name(cls):
        return cls.__name__


class TargetModule(TargetContainerEntity):

    def __init__(self, name, filename=''):
        super().__init__(name, filename)

    def full_name(self):
        return f'{self.name}'


class TargetClass(TargetContainerEntity):

    def __init__(self, module_name, name, filename=''):
        super().__init__(name, filename)
        self.module_name = module_name

    def full_name(self):
        return f'{self.module_name}.{self.name}'


class TargetMethod(TargetEntity):

    def __init__(self, module_name, class_name, name, filename=''):
        super().__init__(name, filename)
        self.module_name = module_name
        self.class_name = class_name

    def full_name(self):
        return f'{self.module_name}.{self.class_name}.{self.name}'


class TargetFunction(TargetEntity):

    def __init__(self, module_name, name, filename=''):
        super().__init__(name, filename)
        self.module_name = module_name

    def full_name(self):
        return f'{self.module_name}.{self.name}'


class TargetEntityResult:

    def __init__(self):
        self.target_entities = []
        self.target_entities_map = {}

    def full_name(self):
        return 'TargetEntityResult'

    def __str__(self):
        return f'target entities: {len(self.target_entities)}'

    def get(self, entity_name):
        return self.target_entities_map[entity_name]

    def add_module(self, module_name, filename):
        m = TargetModule(module_name)
        m.filename = filename
        self.target_entities.append(m)
        self.target_entities_map[str(m)] = m
        return m

    def add_class(self, module_name, class_name, start_line, end_line, filename):
        c = TargetClass(module_name, class_name)
        c.start_line = start_line
        c.end_line = end_line
        c.filename = filename
        self.target_entities_map[str(c)] = c
        return c

    def add_method(self, module_name, method_name, start_line, end_line, clazz, module, filename):
        m = TargetMethod(module_name, clazz.name, method_name)
        m.start_line = start_line
        m.end_line = end_line
        m.filename = filename

        clazz.add_entity(m)
        module.add_entity(m)

        self.target_entities.append(m)
        self.target_entities_map[str(m)] = m
        return m

    def add_function(self, module_name, function_name, start_line, end_line, module, filename):
        f = TargetFunction(module_name, function_name)
        f.start_line = start_line
        f.end_line = end_line
        f.filename = filename

        module.add_entity(f)

        self.target_entities.append(f)
        self.target_entities_map[str(f)] = f
        return f

    def run(self, result):
        for target_entity in self.target_entities:
            target_entity.run(result)



