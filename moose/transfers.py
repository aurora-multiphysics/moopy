#!/usr/env/python3

from enum import IntEnum, auto

class TransferType(IntEnum):
    MultiAppCloneReporterTransfer = auto()
    MultiAppCopyTransfer = auto()
    MultiAppGeometricInterpolationTransfer = auto()
    MultiAppInterpolationTransfer = auto()
    MultiAppMeshFunctionTransfer = auto()
    MultiAppNearestNodeTransfer = auto()
    MultiAppPostprocessorInterpolationTransfer = auto()
    MultiAppPostprocessorToAuxScalarTransfer = auto()
    MultiAppPostprocessorTransfer = auto()
    MultiAppProjectionTransfer = auto()
    MultiAppReporterTransfer = auto()
    MultiAppScalarToAuxScalarTransfer = auto()
    MultiAppShapeEvaluationTransfer = auto()
    MultiAppUserObjectTransfer = auto()
    MultiAppVariableValueSamplePostprocessorTransfer = auto()
    MultiAppVariableValueSampleTransfer = auto()
    MultiAppVectorPostprocessorTransfer = auto()

class Transfer:
    def __init__(self, name = "", source_variable = "", aux_variable = "", \
        **kwargs):
        self.name = name
        self.type = None
        self.source_variable = source_variable
        self.variable = aux_variable

        # set the kwargs into names        
        for arg in kwargs.keys():
            self.__setattr__(arg, kwargs[arg])

    def __str__(self):
        string =  f'[{self.name}]\n'
        string += f'type={self.type.name}\n'
        string += f'source_variable={self.source_variable.name}\n'
        string += f'variable={self.variable.name}\n'

        objects = ["name", "type", "source_variable", "variable"]
        
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

class MultiAppNearestNodeTransfer(Transfer):
    def __init__(self, name="", source_variable = "", aux_variable = "", \
        **kwargs):
        super().__init__(name,source_variable,aux_variable,**kwargs)
        self.type = TransferType.MultiAppNearestNodeTransfer

class Transfers:
    def __init__(self):
        self.name = "Transfers"
        self.transfers = {}

    def __str__(self):
        string =  f'[{self.name}]\n'
        for transfer in self.transfers.keys():
            string += self.transfers[transfer].__str__()
        string += '[]\n'
        return string