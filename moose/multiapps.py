#!/usr/env/python3

from enum import IntEnum, auto

class MultiAppTypes(IntEnum):
    CentroidMultiApp = auto()
    FullSolveMultiApp = auto()
    TransientMultiApp = auto()

class AppTypes(IntEnum):
    CombinedApp = auto()
    CombinedTestApp = auto()
    ThermalHydraulicsApp = auto()

class MultiApp:
    def __init__(self, name = "", input_files = [], **kwargs):
        self.name = name
        self.input_files = input_files
        
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

class CentroidMultiApp(MultiApp):
    def __init__(self, name = "", input_files = [], **kwargs):
        super().__init__(name,input_files, **kwargs)
        self.type = MultiAppTypes.CentroidMultiApp

class FullSolveMultiApp(MultiApp):
    def __init__(self, name = "", input_files = [], **kwargs):
        super().__init__(name,input_files,**kwargs)    
        self.type = MultiAppTypes.FullSolveMultiApp

class TransientMultiApp(MultiApp):
    def __init__(self, name = "", input_files = [], **kwargs):
        super().__init__(name,input_files,**kwargs)  
        self.type = MultiAppTypes.TransientMultiApp  

class MultiApps:
    def __init__(self):
        self.name = "MultiApps"
        self.multiapps = {}

    def __str__(self):
        string = f'[{self.name}]\n'
        for multiapp in self.multiapps.keys():
            string += self.multiapps[multiapp].__str__()
        string += f'[]\n'
        return string