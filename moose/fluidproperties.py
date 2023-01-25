#!/usr/env/python3

from enum import IntEnum,auto

class FluidPropertyTypes(IntEnum):
    BrineFluidProperties = auto()
    CO2FluidProperties = auto()
    CaloricallyImperfectGas = auto()
    FlibeFluidProperties = auto()
    FlinakFluidProperties = auto()
    HeliumFluidProperties = auto()
    HydrogenFluidProperties = auto()
    IdealGasFluidProperties = auto()
    IdealRealGasMixtureFluidProperties = auto()
    MethaneFluidProperties = auto()
    NaClFluidProperties = auto()
    NitrogenFluidProperties = auto()
    SimpleFluidProperties = auto()
    SodiumProperties = auto()
    SodiumSaturationFluidProperties = auto()
    StiffenedGasFluidProperties = auto()
    StiffenedGasTwoPhaseFluidProperties = auto()
    TabulatedBicubicFluidProperties = auto()
    TabulatedFluidProperties = auto()
    TwoPhaseFluidProperties = auto()
    Water97FluidProperties = auto()

class FluidProperty:
    def __init__(self, name = "", **kwargs):
        self.name = name
        # set the kwargs into names        
        for arg in kwargs.keys():
            self.__setattr__(arg, kwargs[arg])

    def __str__(self):
        string =  f'[{self.name}]\n'
        objects = ["name"]
        for key in self.__dict__.keys():
            if key not in objects:
                data = self.__dict__[key]
                if isinstance(data,list):
                    data = [str(x) for x in data]
                    data = ' '.join(data)
                if hasattr(data, '__dict__'):
                    data = data.name
                string += f'{key}={data}\n'
        string += '[]\n'
        return string

class SimpleFluidProperties(FluidProperty):
    def __init__(self, name = "", **kwargs):
        super().__init__(name,**kwargs)
        self.type = FluidPropertyTypes.SimpleFluidProperties

class IdealGasFluidProperties(FluidProperty):
    def __init__(self, name = "", **kwargs):
        super().__init__(name,**kwargs)
        self.type = FluidPropertyTypes.IdealGasFluidProperties

class StiffenedGasFluidProperties(FluidProperty):
    def __init__(self, name = "", **kwargs):
        super().__init__(name,**kwargs)
        self.type = FluidPropertyTypes.StiffenedGasFluidProperties

class FluidProperties:
    def __init__(self):
        self.name = "FluidProperties"
        self.fluidproperties = {}

    def __str__(self):
        string = f'[{self.name}]\n'
        for fluid in self.fluidproperties.keys():
            string += self.fluidproperties[fluid].__str__()
        string += '[]\n'
        return string