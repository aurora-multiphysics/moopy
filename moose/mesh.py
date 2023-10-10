#!/usr/env/python3

from enum import IntEnum, auto

class MeshObjectTypes(IntEnum):
    FileMeshGenerator = auto()
    TransformGenerator = auto()

class TransformTypes(IntEnum):
    TRANSLATE = auto()
    TRANSLATE_CENTER_ORIGIN = auto()
    TRANSLATE_MIN_ORIGIN = auto()
    ROTATE = auto()
    SCALE = auto()

class MeshObject():
    def __init__(self, name = "", **kwargs):
        self.name = name

class FileMeshGenerator(MeshObject):
    def __init__(self, name="", **kwargs):
        super().__init__(name, **kwargs)
        self.mesh_object_type = MeshObjectTypes.FileMeshGenerator
        self.filename = kwargs.pop('filename')
        self.clear_spline_nodes = False
        self.show_info = False
        if 'clear_spline_nodes' in kwargs.keys():
            self.clear_spline_nodes = True
        if 'show_info' in kwargs.keys():
            self.show_info = True
    
    def __str__(self):
        string  = f'[{self.name}]\n'
        string += f'type={self.mesh_object_type.name}\n'
        string += f'file={self.filename}\n'
        if self.clear_spline_nodes:
            string += 'clear_spline_nodes=true\n'
        if self.show_info:
            string += 'show_info=true\n'
        string += '[]\n'
        return string

class TransformGenerator(MeshObject):

    def __init__(self, name = "", **kwargs):
        super().__init__(name, **kwargs)
        self.mesh_object_type = MeshObjectTypes.TransformGenerator    

        self.input = None
        self.transform = None
        self.vector_value = None

        if 'input' in kwargs.keys():
            self.input = kwargs.pop('input')

        if 'transform' in kwargs.keys():
            transform = kwargs.pop('transform')
            if isinstance(transform,int):
                self.transform = TransformTypes(transform)
            else:
                self.transform = transform

        if 'vector_value' in kwargs.keys():
            self.vector_value = kwargs.pop('vector_value')
                
    def __str__(self):
        string =  f'[{self.name}]\n'
        string += f'type={self.mesh_object_type.name}\n'
        string += f'input="{self.input.name}"\n'
        string += f'transform={self.transform.name}\n'
        vector_value = ' '.join([str(x) for x in self.vector_value])
        string += f'vector_value="{vector_value}"\n'
        string += '[]\n'
        return string

class Mesh():
    def __init__(self):
        self.name = "Mesh"
        self.mesh_objects = {}
        self.second_order = False
        
    def __str__(self):
        string  = f'[{self.name}]\n'
        for mesh in self.mesh_objects.keys():
            string += self.mesh_objects[mesh].__str__()
        
        if self.second_order:
            string += 'second_order=true\n'
        string += '[]\n'

        return string

    def add_mesh_object(self, name = "", type = None, **kwargs):
        if name in self.mesh_objects.keys():
            print (f'name {name} already in use')
            
        mesh = None  # Add a default value for the 'mesh' variable
        
        if type == MeshObjectTypes.FileMeshGenerator:
            mesh = FileMeshGenerator(name=name, **kwargs)
        elif type == MeshObjectTypes.TransformGenerator:
            mesh = TransformGenerator(name=name, **kwargs)
        
        if mesh is not None:
            self.mesh_objects[name] = mesh
        
