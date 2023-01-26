#!/usr/env/python3

from enum import IntEnum, auto

class BoundaryConditionTypes(IntEnum):
    ADDirichletBC  = auto()
    ADNeumannBC = auto()
    ADConvectiveHeatFluxBC = auto()
    Pressure = auto()

class BoundaryCondition:
    def __init__(self, name = "", variable = None, boundary = "", **kwargs):
        self.name = name
        self.variable = variable
        self.boundary = boundary

class ADDirichletBC(BoundaryCondition):
    def __init__(self, name = "", variable = None, boundary = "", **kwargs):
        super().__init__(name,variable,boundary)
        self.bc_type = BoundaryConditionTypes.ADDirichletBC
        self.value = kwargs.pop("value")

    def __str__(self):
        string =  f'[{self.name}]\n'
        string += f'type={self.bc_type.name}\n'
        string += f'variable={self.variable.name}\n'
        string += f'boundary="{self.boundary}"\n'
        string += f'value={self.value}\n'
        string += f'[]\n'
        return string

class ADNeumannBC(ADDirichletBC):
    def __init__(self, name = "", variable = None, boundary = "", **kwargs):
        super().__init__(name,variable,boundary,**kwargs)
        self.bc_type = BoundaryConditionTypes.ADNeumannBC

class ADConvectiveHeatFluxBC(BoundaryCondition):
    def __init__(self, name = "", variable = None, boundary = "", **kwargs):
        super().__init__(name,variable,boundary,**kwargs)
        self.bc_type = BoundaryConditionTypes.ADConvectiveHeatFluxBC
        self.heat_transfer_coefficient = kwargs.pop("heat_transfer_coefficient")
        self.t_infinity = kwargs.pop("t_infinity")    

    def __str__(self):
        string = f'[{self.name}]\n'
        string += f'type={self.bc_type.name}\n'
        string += f'variable={self.variable.name}\n'
        string += f'boundary="{self.boundary}"\n'
        # its possible htc is a function rather than a value
        if isinstance(self.heat_transfer_coefficient,str):
            string += f'heat_transfer_coefficient={self.heat_transfer_coefficient}\n'
        else:
            string += f'heat_transfer_coefficient={self.heat_transfer_coefficient.name}\n'
        string += f'T_infinity={self.t_infinity}\n'
        string += '[]\n'
        return string       

class Pressure(BoundaryCondition): 
    def __init__(self, name = "", variable = None, boundary = "", **kwargs):
        super().__init__(name,variable,boundary,**kwargs)
        self.bc_type = BoundaryConditionTypes.Pressure
        self.pressure_value = kwargs.pop("value")  
        self.displacements = kwargs.pop('displacements')

    def __str__(self):
        string = f'[Pressure]\n'
        string += f'[{self.name}]\n'
        displacements = ' '.join([x.name for x in self.displacements])
        string += f'displacements="{displacements}"\n'
        string += f'boundary="{self.boundary}"\n'
        string += f'factor={self.pressure_value}\n'
        string += 'use_automatic_differentiation=true\n'
        string += '[]\n'
        string += '[]\n'
        return string  

class BoundaryConditions:
    def __init__(self):
        self.name = "BCs"
        self.boundary_conditions = {}
    
    def add_boundary_condition(self,name,type,variable,boundary,**kwargs):
        if name in self.boundary_conditions.keys():
            print(f'BC name {name} already in use')
        if type == BoundaryConditionTypes.ADDirichletBC:
            bc = ADDirichletBC(name,variable,boundary,**kwargs)
            self.boundary_conditions[name] = bc
        elif type == BoundaryConditionTypes.ADNeumannBC:
            bc = ADNeumannBC(name,variable,boundary,**kwargs)
            self.boundary_conditions[name] = bc
        elif type == BoundaryConditionTypes.ADConvectiveHeatFluxBC:
            bc = ADConvectiveHeatFluxBC(name,variable,boundary,**kwargs)
            self.boundary_conditions[name] = bc    
        elif type == BoundaryConditionTypes.Pressure:
            bc = Pressure(name,variable,boundary,**kwargs)
            self.boundary_conditions[name] = bc  

    def __str__(self):
        string = f'[{self.name}]\n'
        for bc in self.boundary_conditions.keys():
            string += self.boundary_conditions[bc].__str__()
        string += f'[]\n'
        return string