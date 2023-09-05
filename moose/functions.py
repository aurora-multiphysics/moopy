#!/usr/env/python3

from enum import IntEnum, auto
from moose.variables import Variable

class MooseFunctionTypes(IntEnum):
    PiecewiseLinear = auto()
    ParsedFunction = auto()

class PiecewiseFunction:
    def __init__(self, name = "", x_data = None, y_data = None):
        self.name = name
        self.x_data = x_data
        self.y_data = y_data

    def __str__(self):

        if isinstance(self.x_data,list):
            if isinstance(self.x_data[0],(int,float)):
                x_str = [ str(x) for x in self.x_data]
                y_str = [ str(x) for x in self.y_data]
                string  = 'x="' + ' '.join(x_str) + '"\n'
                string += 'y="' + ' '.join(y_str) + '"\n'
            elif isinstance(self.x_data[0],str):  
                string  = 'x="' + ' '.join(x_str) + '"\n'
                string += 'y="' + ' '.join(y_str) + '"\n'

        if isinstance(self.x_data,str):
            string  = 'x="' + self.x_data + '"\n'
            string += 'y="' + self.y_data + '"\n'
            
        return string

class PolynomialFunction:
    def __init__(self, name = "", arguments = [None,None,None,None], coefficients = [0,0,0,0,0]):
        self.name = name
        self.coefficients = coefficients
        self.arguments = arguments

    def __str__(self):
        string = 'function="'
        for idx,arg in enumerate(self.arguments):
            if type(arg) is Variable:
                string += "pow(" + arg.name + "," + str(4 - idx) +")" + "*" + str(self.coefficients[idx]) + " + "
            else:
                if self.coefficients[idx] != 0.0 and arg != 0.0:
                    string += str(arg) + "*" + str(self.coefficients[idx]) + " + "

        string += str(self.coefficients[4])
        string += '"\n'
        return string

    def non_variable_arguments(self):
        string = ""
        for i in self.arguments:
            if i is not type(Variable):
                string += str(i) + " "
        return string

    def get_coefficients(self):
        string = ' '.join(str(x) for x in self.coefficients)
        return string

class GenericFunction:
    def __init__(self, name = "", **kwargs):
        self.name = name

        # set the kwargs into names        
        for arg in kwargs.keys():
            self.__setattr__(arg, kwargs[arg])
    
    def __str__(self):
        string =  f'[{self.name}]\n'
        string += f'type={self.type.name}\n'
        
        objects = ["name", "type"]
        
        for key in self.__dict__.keys():
            if key not in objects:
                data = self.__dict__[key]
                if isinstance(data,list):
                    if hasattr(data[0], '__dict__'):
                        data = [x.name for x in data]
                    else:
                        data = [str(x) for x in data]
                    data = ' '.join(data)
                if hasattr(data, '__dict__'):
                    data = data.name
                string += f'{key}="{data}"\n'

        string += '[]\n'
        return string

class ParsedFunction(GenericFunction):
    def __init__(self,name = "", function = None):
        super().__init__(name)
        self.type = MooseFunctionTypes.ParsedFunction
        self.function = function

    def __str__(self):
        string = f'[{self.name}]\n'
        string += f'type={self.type.name}\n'
        string += f'value={self.function.__str__()}\n'
        string += f'vars={self.function.non_variable_arguments()}\n'
        string += f'vals={self.function.get_coefficients()}\n'
        string += '[]\n'
        
        return string

class PiecewiseLinear(GenericFunction):
    def __init__(self,name = "", **kwargs):
        super().__init__(name, **kwargs)
        self.type = MooseFunctionTypes.PiecewiseLinear

class Functions:
    def __init__(self):
        self.name = "Functions"
        self.functions = {}

    def __str__(self):
        string  = f'[{self.name}]\n'
        for func in self.functions.keys():
            string += self.functions[func].__str__()
        string += "[]\n"
        return string

    
