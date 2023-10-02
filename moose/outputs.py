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
            elif key == "csv":
                string += 'csv=true\n'
            else:
                value = self.outputs[key]
                if type(value) is bool:
                    value = str(value).lower()
                string += f'{key}={value}\n'

        string += '[]\n'
        return string