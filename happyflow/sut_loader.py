import ast
from happyflow.utils import *
from happyflow.sut_model import SUTContainer


class SUTLoader:

    def __init__(self, dir='.'):
        self.dir = dir
        self.sut_container = SUTContainer()

    def load_sut(self):
        python_files = find_python_files(self.dir)
        for filename in python_files:
            module_code = open_file(filename)
            if module_code:
                module_node = ast.parse(module_code)
                module_name = find_module_name(filename)

                visitor = SUTVisitor(self.sut_container, module_name, filename)
                visitor.visit(module_node)

    @staticmethod
    def find_sut(sut_name, dir='.'):
        loader = SUTLoader(dir)
        loader.load_sut()
        return loader.sut_container.get(sut_name)


class SUTVisitor(ast.NodeVisitor):

    def __init__(self, sut, module_name, filename):
        self.sut = sut
        self.module_name = module_name
        self.filename = filename
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

