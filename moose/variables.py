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
    
class Variable:
    def __init__(self, name, order=None, **kwargs):
        self.name = name
        self.order = order
        self.kwargs = kwargs

    def __str__(self):
        string = f'[{self.name}]\n'
        if self.order is not None:
            string += f'order = {Order(self.order).name}\n'
        if 'family' in self.kwargs:
            string += f'family = {self.kwargs["family"].name}\n'
        if 'initial_condition' in self.kwargs:
            string += f'initial_condition = "{self.kwargs["initial_condition"]}"\n'
        if 'block' in self.kwargs and self.kwargs['block'] is not None:
            string += f'block = "{self.kwargs["block"]}"\n'
        string += f'[]\n'
        return string

class AuxVariable(Variable):
    def __init__(self, name="",**kwargs):
        super().__init__(name, order, family, block, initial_condition)

class Variables():
    def __init__(self):
        self.name = "Variables"
        self.variables = {}

    def add_variable(self, name, order=None, **kwargs):
        variable = Variable(name=name, order=order, **kwargs)
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
        
