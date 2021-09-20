import ast
from happyflow.utils import *
from happyflow.target_model import TargetEntityResult, TargetEntity


class TargetEntityLoader:

    def __init__(self, dir='.'):
        self.dir = dir
        self.target_container = TargetEntityResult()

    def load(self):
        python_files = find_python_files(self.dir)
        for filename in python_files:
            module_code = open_file(filename)
            if module_code:
                try:
                    module_node = ast.parse(module_code)

                    visitor = TargetEntityVisitor(self.target_container, filename)
                    visitor.visit(module_node)
                except:
                    pass

    @staticmethod
    def find(target_entity_name, dir='.'):
        loader = TargetEntityLoader(dir)
        loader.load()
        return loader.target_container.get(target_entity_name)

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

