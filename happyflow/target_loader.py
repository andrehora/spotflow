import ast
from happyflow.utils import *
from happyflow.target_model import TargetEntityResult, TargetEntity


class TargetEntityLoader:

    def __init__(self, dir='.', module_name=None):
        self.dir = dir
        self.module_name = module_name
        self.target_container = TargetEntityResult()

    def load(self):
        python_files = find_python_files(self.dir)
        for filename in python_files:
            if self.module_name:
                target_module_name = find_module_name(filename)
                if self.module_name == target_module_name:
                    self.parse_file(filename)
            else:
                self.parse_file(filename)

    def parse_file(self, filename):
        module_code = open_file(filename)
        if module_code:
            try:
                module_node = ast.parse(module_code)
                visitor = TargetEntityVisitor(self.target_container, filename)
                visitor.visit(module_node)
            except:
                pass

    @staticmethod
    def find(target_entity_name, dir='.', module_name=None):
        try:
            loader = TargetEntityLoader(dir, module_name)
            loader.load()
            return loader.target_container.get(target_entity_name)
        except Exception:
            return None

    @staticmethod
    def load_from_frame(frame):
        func_or_method = find_func_or_method_from_frame(frame)
        if func_or_method:
            return TargetEntityLoader.load_func(func_or_method)
        return None

    @staticmethod
    def load_func(func_or_method):
        return TargetEntity.build_from_func(func_or_method)


class TargetEntityVisitor(ast.NodeVisitor):

    def __init__(self, sut, filename):
        self.sut = sut
        self.filename = filename
        self.module_name = find_module_name(filename)
        self.module = self.sut.add_module(self.module_name, self.filename)

    def visit_Module(self, node):
        for element in node.body:
            if isinstance(element, ast.FunctionDef):
                self.visit_function(element)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_ClassDef(self, node):
        clazz = self.sut.add_class(self.module_name, node.name, node.lineno, node.end_lineno, self.filename)
        for element in node.body:
            if isinstance(element, ast.FunctionDef):
                self.visit_method(element, clazz)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_function(self, node):
        self.sut.add_function(self.module_name, node.name, node.lineno, node.end_lineno, self.module, self.filename)

    def visit_method(self, node, clazz):
        self.sut.add_method(self.module_name, node.name, node.lineno, node.end_lineno, clazz, self.module, self.filename)

