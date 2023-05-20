#!/usr/env/python3

from enum import IntEnum, auto

class Order(IntEnum):
    CONSTANT = auto()
    FIRST = auto()
    SECOND = auto()
    THIRD = auto()
    FOURTH = auto()

class Family(IntEnum):
    LAGRANGE = auto()
    MONOMIAL = auto()
    HERMITE = auto()
    SCALAR = auto()
    HIERARCHIC = auto()
    CLOUGH = auto()
    XYZ = auto()
    SZABAB = auto()
    BERNSTEIN = auto()
    L2_LAGRANGE = auto()
    L2_HIERARCHIC = auto()
    NEDELEC_ONE = auto()
    LAGRANGE_VEC = auto()
    MONOMIAL_VEC = auto()
    RATIONAL_BERNSTEIN = auto()
    SIDE_HIERARCHIC = auto()
    
class Variable():
    def __init__(self, name="", order=None, family=None, block="", initial_condition=""):
        self.name = name
        self.order = Order(order) if order is not None else None
        self.family = Family(family) if family is not None else None
        self.block = block
        self.initial_condition = initial_condition

    def __str__(self):
        string = f'[{self.name}]\n'
        if self.order:
            string += f'order = {self.order.name}\n'
        if self.family:
            string += f'family = {self.family.name}\n'
        if self.initial_condition:
            string += f'initial_condition = "{self.initial_condition}"\n'
        if self.block:
            string += f'block = "{self.block}"\n'
        string += '[]\n'
        return string
        
class AuxVariable(Variable):
    def __init__(self, name="", order=None, family=None, block="", initial_condition=""):
        super().__init__(name, order, family, block, initial_condition)

class Variables():
    def __init__(self):
        self.name = "Variables"
        self.variables = {}

    def add_variable(self, name, order=None, family=None, block="", initial_condition=""):
        variable = Variable(name=name, order=order, family=family, block=block, initial_condition=initial_condition)
        if variable.name in self.variables.keys():
            print("variable name already in use")
            
        self.variables[variable.name] = variable

    def __str__(self):
        string = f'[{self.name}]\n'
        for variable in self.variables.keys():
            string += self.variables[variable].__str__()
        string += f'[]\n'
        return string

class AuxVariables(Variables):
    def __init__(self):
        super().__init__()
        self.name = "AuxVariables"    
        
