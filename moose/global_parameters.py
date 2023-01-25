#!/usr/env/python3

class GlobalParameters():
    def __init__(self, **kwargs):
        self.name = "GlobalParams"
        self.members = kwargs

    def __str__(self):
        string =  f'[{self.name}]\n'
        for key in self.members.keys():
            if key == "displacements":
                displacements =  ' '.join([x.name for x in self.members["displacements"]])
                string += f'displacements="{displacements}"\n'
            if key == "volumetric_locking_correction":
                string += f'volumetric_locking_correction=true\n'
        string += '[]\n'
        return string