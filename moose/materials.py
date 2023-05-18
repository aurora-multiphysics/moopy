#!/usr/env/python3

from enum import IntEnum, auto

class MaterialTypes(IntEnum):
    ADPiecewiseLinearInterpolationMaterial  = auto()
    ADParsedMaterial  = auto()
    ADHeatConductionMaterial = auto()  
    ADComputeVariableIsotropicElasticityTensor = auto()
    ADComputeMeanThermalExpansionFunctionEigenstrain = auto() 
    ADComputeSmallStrain = auto()
    ADComputeLinearElasticStress = auto()
    ADGenericFunctionMaterial = auto()

class Material(object):
    def __init__(self, name = "", block = ""):
        self.name = name
        self.block = block

class ADPiecewiseLinearInterpolationMaterial(Material):
    def __init__(self, name = "", block = "", **kwargs):
        super().__init__(name , block)    
        self.data = kwargs.pop('data')
        self.material_type = MaterialTypes.ADPiecewiseLinearInterpolationMaterial 
        self.property = kwargs.pop('property')
        self.variable = kwargs.pop('variable')

    def __str__(self):
        string = f'[{self.name}]\n'
        string += f'type={self.material_type.name}\n'
        string += self.data.__str__()
        string += f'property="{self.property}"\n'
        string += f'variable={self.variable.name}\n'
        if self.block:
            string += f'block="{self.block}"\n'
        string += '[]\n'
        return string  

class ADParsedMaterial(Material):
    def __init__(self, name = "", block = "", **kwargs):
        super().__init__(name , block)    
        self.data = kwargs.pop('data')
        self.material_type = MaterialTypes.ADParsedMaterial 
        self.property = kwargs.pop('property')
        self.variable = kwargs.pop('variable')

    def __str__(self):
        string = f'[{self.name}]\n'
        string += f'type={self.material_type.name}\n'
        string += self.data.__str__()
        string += f'f_name="{self.property}"\n'
        string += f'variable={self.variable.name}\n'
        if self.block:
            string += f'block="{self.block}"\n'
        string += '[]\n'
        return string          

class ADHeatConductionMaterial(Material):
    def __init__(self, name = "", block = "", **kwargs):
        super().__init__(name , block)    
        self.material_type = MaterialTypes.ADHeatConductionMaterial 
        self.variable = kwargs.pop('variable')
        self.specific_heat = kwargs.pop('specific_heat')
        self.thermal_conductivity = kwargs.pop('thermal_conductivity')

    def __str__(self):
        string  = f'[{self.name}]\n'
        string += f'type={self.material_type.name}\n'
        string += f'temp={self.variable.name}\n'
        if self.block:
            string += f'block={self.block}\n'
        string += f'specific_heat_temperature_function={self.specific_heat.name}\n'
        string += f'thermal_conductivity_temperature_function={self.thermal_conductivity.name}\n'
        string += '[]\n'
        return string

class ADComputeVariableIsotropicElasticityTensor(Material):
    def __init__(self, name = "", block = "", **kwargs):
        super().__init__(name,block)
        self.material_type = MaterialTypes.ADComputeVariableIsotropicElasticityTensor
        self.poissons_ratio  = kwargs.pop('poissons_ratio')
        self.youngs_modulus = kwargs.pop('youngs_modulus')

    def __str__(self):
        string  = f'[{self.name}]\n'
        string += f'type={self.material_type.name}\n'
        string += f'poissons_ratio={self.poissons_ratio}\n'
        string += f'youngs_modulus={self.youngs_modulus}\n'
        if self.block:
            string += f'block={self.block}\n'
        string += "[]\n"
        return string

class ADComputeMeanThermalExpansionFunctionEigenstrain(Material):
    def __init__(self, name = "", block = "", **kwargs):
        super().__init__(name,block)
        self.material_type = MaterialTypes.ADComputeMeanThermalExpansionFunctionEigenstrain
        self.thermal_expansion = kwargs.pop('thermal_expansion')
        self.thermal_expansion_function_reference_temperature = kwargs.pop('thermal_expansion_function_reference_temperature')
        self.stress_free_temperature = kwargs.pop('stress_free_temperature')
        self.variable = kwargs.pop('variable')
        self.eigenstrain_name = kwargs.pop('eigenstrain_name')

    def __str__(self):
        string  = f'[{self.name}]\n'
        string += f'type={self.material_type.name}\n'
        string += f'thermal_expansion_function={self.thermal_expansion.name}\n'
        string += f'thermal_expansion_function_reference_temperature={self.thermal_expansion_function_reference_temperature}\n'
        string += f'stress_free_temperature={self.stress_free_temperature}\n'
        string += f'eigenstrain_name={self.eigenstrain_name}\n'
        string += f'temperature={self.variable.name}\n'
        if self.block:
            string += f'block={self.block}\n'
        string += "[]\n"
        return string

class ADComputeSmallStrain(Material):
    def __init__(self, name = "", block = "", **kwargs):
        super().__init__(name,block)
        self.material_type = MaterialTypes.ADComputeSmallStrain
        self.displacements = kwargs.pop('displacements')
        self.eigenstrain_names = kwargs.pop('eigenstrain_names')
 
    def __str__(self):
        string  = f'[{self.name}]\n'
        string += f'type={self.material_type.name}\n'
        displacements = ' '.join([x.name for x in self.displacements])
        string += f'displacements="{displacements}"\n'
        string += f'eigenstrain_names={self.eigenstrain_names}\n'
        if self.block:
            string += f'block={self.block}\n'
        string += "[]\n"
        return string

class ADComputeLinearElasticStress(Material):
    def __init__(self, name = "", block = "", **kwargs):
        super().__init__(name,block)
        self.material_type = MaterialTypes.ADComputeLinearElasticStress

    def __str__(self):
        string  = f'[{self.name}]\n'
        string += f'type={self.material_type.name}\n'
        if self.block:
            string += f'block="{self.block}"\n'        
        string += "[]\n"
        return string

class ADGenericFunctionMaterial(Material):
    def __init__(self, name = "", block = "", **kwargs):
        super().__init__(name,block)
        self.material_type = MaterialTypes.ADGenericFunctionMaterial
        self.prop_names = kwargs.pop('prop_names')
        self.prop_values = kwargs.pop('prop_values')
    
    def __str__(self):
        string =  f'[{self.name}]\n'
        string += f'type={self.material_type.name}\n'
        prop_names = ' '.join(self.prop_names)
        string += f'prop_names=\'{prop_names}\'\n'
        prop_values = ' '.join([x.name for x in self.prop_values])
        string += f'prop_values=\'{prop_values}\'\n'
        if self.block:
            string += f'block="{self.block}"\n'
        string += '[]\n'
        return string

class Materials:
    def __init__(self):
        self.name = "Materials"
        self.materials = {}

    def add_material(self,name = "",type = None, block = "", **kwargs):
        if name in self.materials.keys():
            print(f'Material name {name} already in use')
        if MaterialTypes(type) == MaterialTypes.ADPiecewiseLinearInterpolationMaterial:
            material = ADPiecewiseLinearInterpolationMaterial(name,block,**kwargs)
            self.materials[name] = material
        elif MaterialTypes(type) == MaterialTypes.ADParsedMaterial:
            material = ADParsedMaterial(name,block,**kwargs)
            self.materials[name] = material
        elif MaterialTypes(type) == MaterialTypes.ADHeatConductionMaterial:
            material = ADHeatConductionMaterial(name,block,**kwargs)
            self.materials[name] = material
        elif MaterialTypes(type) == MaterialTypes.ADComputeVariableIsotropicElasticityTensor:
            material = ADComputeVariableIsotropicElasticityTensor(name,block,**kwargs)
            self.materials[name] = material
        elif MaterialTypes(type) == MaterialTypes.ADComputeMeanThermalExpansionFunctionEigenstrain:
            material = ADComputeMeanThermalExpansionFunctionEigenstrain(name,block,**kwargs)
            self.materials[name] = material
        elif MaterialTypes(type) == MaterialTypes.ADComputeSmallStrain:
            material = ADComputeSmallStrain(name,block,**kwargs)
            self.materials[name] = material
        elif MaterialTypes(type) == MaterialTypes.ADComputeLinearElasticStress:
            material = ADComputeLinearElasticStress(name,block,**kwargs)
            self.materials[name] = material

    def __str__(self):
        string = f'[{self.name}]\n'
        for material in self.materials.keys():
            string += self.materials[material].__str__()
        string += f'[]\n'
        return string
