#!/usr/env/python3

import re

def indent(string):
    new_string = string.split('\n')
    indent_count = 0
    for idx,line in enumerate(new_string):
        increments = re.findall('\[.+?\]',line)
        decrements = re.findall('\[\]',line)
        
        if decrements:
            indent_count = indent_count - 2

        if indent_count > 0:
            new_string[idx] = " "*indent_count + line

        if increments:
            indent_count = indent_count + 2

    return '\n'.join(new_string)

class MOOSEInput():
    def __init__(self):
        self.global_params = None
        self.mesh = None
        self.variables = None
        self.aux_variables = None
        self.kernels = None
        self.components = None
        self.closures = None
        self.multiapps = None
        self.aux_kernels = None
        self.functions = None
        self.boundary_conditions = None
        self.materials = None
        self.post_processors = None
        self.fluid_properties = None
        self.transfers = None
        self.problem = None
        self.executioner = None
        self.outputs = None

    def write(self, filename):
        file = open(filename,'w')
        # first the mesh block
        if self.mesh: file.write(indent(self.mesh.__str__()))
        if self.global_params: file.write(indent(self.global_params.__str__()))
        if self.variables: file.write(indent(self.variables.__str__()))
        if self.aux_variables: file.write(indent(self.aux_variables.__str__()))
        if self.closures: file.write(indent(self.closures.__str__()))
        if self.components: file.write(indent(self.components.__str__()))
        if self.kernels: file.write(indent(self.kernels.__str__()))
        if self.aux_kernels: file.write(indent(self.aux_kernels.__str__()))
        if self.functions: file.write(indent(self.functions.__str__()))
        if self.boundary_conditions: file.write(indent(self.boundary_conditions.__str__()))
        if self.fluid_properties: file.write(indent(self.fluid_properties.__str__()))
        if self.materials: file.write(indent(self.materials.__str__()))
        if self.multiapps: file.write(indent(self.multiapps.__str__()))
        if self.transfers: file.write(indent(self.transfers.__str__()))
        if self.post_processors: file.write(indent(self.post_processors.__str__()))
        if self.executioner: file.write(indent(self.executioner.__str__()))
        if self.outputs: file.write(indent(self.outputs.__str__()))

        file.close()

    def read(self, filename):
        file = open(filename,'r')
        file.close()
    
