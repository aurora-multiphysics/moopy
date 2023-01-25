#!/usr/env/python3

from enum import IntEnum, auto

class ExectutionTypes(IntEnum):
    NONE = auto() 
    INITIAL = auto()
    LINEAR = auto() 
    NONLINEAR = auto()
    TIMESTEP_END = auto()
    TIMESTEP_BEGIN = auto()
    FINAL = auto()
    CUSTOM = auto() 
    ALWAYS = auto()

class Executioner():
    def __init__(self, **kwargs):
        self.name = "Executioner"
        self.solve_objects = kwargs

    def __str__(self):
        string =  f'[{self.name}]\n'
        for key in self.solve_objects.keys():
            string += f'{key}="{self.solve_objects[key]}"\n'
        string += '[]\n'
        return string