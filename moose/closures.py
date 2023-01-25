#!/usr/env/python3

from enum import IntEnum, auto

class ClosureType(IntEnum):
    Closures1PhaseNone = auto()
    Closures1PhaseSimple = auto()
    
class Closure:
    def __init__(self, name = ""):
        self.name = name

    def __str__(self):
        string =  f'[{self.name}]\n'
        string += f'type={self.type.name}\n'
        string += '[]\n'
        return string

class Closures1PhaseSimple(Closure):
    def __init__(self, name):
        super().__init__(name)
        self.type = ClosureType.Closures1PhaseSimple

class Closures1PhaseNone(Closure):
    def __init__(self, name):
        super().__init__(name)
        self.type = ClosureType.Closures1PhaseNone

class Closures:
    def __init__(self):
        self.name = "Closures"
        self.closures = {}

    def __str__(self):
        string =  f'[{self.name}]\n'
        for closure in self.closures.keys():
            string += self.closures[closure].__str__()
        string += '[]\n'
        return string