#!/usr/env/python3

class Outputs():
    def __init__(self, **kwargs):
        self.name = "Outputs"
        self.outputs = kwargs
    
    def __str__(self):
        string =  f'[{self.name}]\n'
        for key in self.outputs.keys():
            if key == "exodus":
                string += 'exodus=true\n'
            if key == "csv":
                string += 'csv=true\n'
    
        string += '[]\n'
        return string