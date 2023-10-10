#!/usr/env/python3

from enum import IntEnum, auto

class ScalarType(IntEnum):
    VonMisesStress = auto()
    EffectiveStrain = auto()
    Hydrostatic = auto()
    L2norm = auto()
    MaxPrincipal= auto()
    MidPrincipal = auto()
    MinPrincipal = auto()
    VolumetricStrain = auto() 
    FirstInvariant = auto()
    SecondInvariant = auto() 
    ThirdInvariant = auto() 
    AxialStress = auto()
    HoopStress = auto()
    RadialStress = auto()
    TriaxialityStress = auto()
    Direction = auto()
    MaxShear = auto()
    StressIntensity = auto()

class AuxKernelTypes(IntEnum):
    ParsedAux = auto()
    ADRankTwoAux = auto()
    ADRankTwoScalarAux = auto()

class KernelTypes(IntEnum):
    ADHeatConduction  = auto()
    ADHeatConductionTimeDerivative = auto()
    TensorMechanics = auto()
    ADGravity = auto()
    
class Kernel():
    def __init__(self, name = "", variable = None, block = None,
            **kwargs):
        self.name = name
        self.variable = variable
        self.block = block

class ADHeatConduction(Kernel):
    def __init__(self, name = "", variable = None, block = None,
            **kwargs):
        super().__init__(name, variable, block, **kwargs)
        self.kernel_type = KernelTypes.ADHeatConduction

        if "thermal_conductivity" in kwargs.keys():
            self.thermal_conductivity = kwargs.pop("thermal_conductivity")  
        else:
            self.thermal_conductivity = None

    def __str__(self):
        string = f'[{self.name}]\n'
        string += f'type={self.kernel_type.name}\n'
        string += f'variable={self.variable.name}\n'
        # write the block if provided
        if self.block is not None:
            string += f'block={self.block}\n'
        if self.thermal_conductivity:
            string += f'thermal_conductivity={self.thermal_conductivity}\n'
        string += "[]\n"
        return string       

class ADHeatConductionTimeDerivative(Kernel):
    def __init__(self, name = "", variable = None, block = None,
            **kwargs):
        super().__init__(name, variable, block, **kwargs)
        self.kernel_type = KernelTypes.ADHeatConductionTimeDerivative

        if "density_name" in kwargs.keys():
            self.density_name = kwargs.pop('density_name')
        else:
            self.density_name = ""

        if "specific_heat" in kwargs.keys():
            self.specific_heat = kwargs.pop('specific_heat')
        else:
            self.specific_heat = ""

    def __str__(self):
        string = f'[{self.name}]\n'
        string += f'type={self.kernel_type.name}\n'
        string += f'variable={self.variable.name}\n'
        if self.density_name:
            string += f'density_name={self.density_name}\n'
        if self.specific_heat:
            string += f'specific_heat={self.specific_heat}\n'
        # write the block if provided
        if self.block is not None:
            string += f'block={self.block}\n'
        string += "[]\n"
        return string          

class TensorMechanics(Kernel):
    def __init__(self, name = "", variable = None, block = None,
            **kwargs):
        super().__init__(name, variable, block, **kwargs)
        self.kernel_type = KernelTypes.TensorMechanics
        self.name = 'TensorMechanics'

        if 'displacements' in kwargs.keys():
            self.displacements = kwargs.pop('displacements')

        if 'generate_output' in kwargs.keys():
            self.generate_output = kwargs.pop('generate_output')

        if "eigenstrain_names" in kwargs.keys():
            self.eigenstrain_names = kwargs.pop('eigenstrain_names')

    def __str__(self):
        string = f'[{self.name}]\n'
        displacements = ' '.join([x.name for x in self.displacements])
        string += f'displacements="{displacements}"\n'
        output = ' '.join([x for x in self.generate_output])
        string += f'generate_output="{output}"\n'
        string += f'eigenstrain_names="{self.eigenstrain_names}"\n'
        string += 'use_automatic_differentiation=true\n'
        # write the block if provided
        if self.block is not None:
            string += f'block={self.block}\n'
        string += "[]\n"
        return string  

class ADGravity(Kernel):
    def __init__(self, name = "", variable = None, block = None,
            **kwargs):
        super().__init__(name, variable, block, **kwargs)

        self.kernel_type = KernelTypes.ADGravity    
        self.value = kwargs.pop('value')

    def __str__(self):
        string = f'[{self.name}]\n'
        string += f'type={self.kernel_type.name}\n'
        string += f'variable={self.variable.name}\n'
        string += f'value="{self.value}"\n'
        if self.block:
            string += f'block={self.block}\n'
        string += "[]\n"
        return string  

class AuxKernel(Kernel):
    def __init__(self, name = "", variable = None, block = None,
            **kwargs):
        super().__init__(name,variable,block,**kwargs)

class ParsedAux(AuxKernel):
    def __init__(self, name = "", variable = None, block = None,
            **kwargs):
        super().__init__(name,variable,block,**kwargs) 
        self.aux_kernel_type = AuxKernelTypes.ParsedAux
        self.function = kwargs.pop('function')
        self.args = kwargs.pop('args')

    def __str__(self):
        string  = f'[{self.name}]\n'
        string += f'type={self.aux_kernel_type.name}\n'
        string += f'variable={self.variable.name}\n'
        string += f'function={self.function.__str__()}\n'
        string += f'args={self.args.name}\n'
        string += '[]\n'
        return string

class ADRankTwoAux(AuxKernel):
    def __init__(self, name = "", variable = None, block = None,
            **kwargs):
        super().__init__(name,variable,block,**kwargs)   
        self.aux_kernel_type = AuxKernelTypes.ADRankTwoAux
        self.rank_two_tensor = kwargs.pop('rank_two_tensor')
        self.index_i = kwargs.pop('index_i')
        self.index_j = kwargs.pop('index_j')

    def __str__(self):
        string  = f'[{self.name}]\n'
        string += f'type={self.aux_kernel_type.name}\n'
        string += f'rank_two_tensor={self.rank_two_tensor}\n'
        string += f'variable={self.variable.name}\n'
        string += f'index_i={self.index_i}\n'
        string += f'index_j={self.index_j}\n'
        string += '[]\n'
        return string

class ADRankTwoScalarAux(AuxKernel):
    def __init__(self, name = "", variable = None, block = None,
            **kwargs):
        super().__init__(name,variable,block,**kwargs)   
        self.aux_kernel_type = AuxKernelTypes.ADRankTwoScalarAux
        self.rank_two_tensor = kwargs.pop('rank_two_tensor')

        if isinstance(kwargs['scalar_type'],int): 
            self.scalar_type = ScalarType(kwargs.pop('scalar_type'))
        else:
            self.scalar_type = kwargs.pop('scalar_type')

    def __str__(self):
        string  = f'[{self.name}]\n'
        string += f'type={self.aux_kernel_type.name}\n'
        string += f'rank_two_tensor={self.rank_two_tensor}\n'
        string += f'variable={self.variable.name}\n'
        string += f'scalar_type={self.scalar_type.name}\n'
        string += '[]\n'        
        return string

class Kernels():
    def __init__(self):
        self.name = "Kernels"
        self.kernels = {}

    def add_kernel(self,name,type,variable,block, **kwargs):
        if name in self.kernels.keys():
            print(f'kernel name {name} already in use')

        if type == KernelTypes.ADHeatConduction:
            kernel = ADHeatConduction(name,variable,block, **kwargs)
        elif type == KernelTypes.ADHeatConductionTimeDerivative:
            kernel = ADHeatConductionTimeDerivative(name,variable,block, **kwargs)
        elif type == KernelTypes.TensorMechanics:
            kernel = TensorMechanics(name,variable,block, **kwargs)
        elif type == KernelTypes.ADGravity:
            kernel = ADGravity(name,variable,block, **kwargs)
   
        self.kernels[name] = kernel
            
    def __str__(self):
        string = f'[{self.name}]\n'
        for kernel in self.kernels.keys():
            string += self.kernels[kernel].__str__()
        string += f'[]\n'
        return string

class AuxKernels(Kernels):
    def __init__(self):
        super().__init__()
        self.name = 'AuxKernels'
    
    def add_kernel(self, name, type, variable, block, **kwargs):
        if name in self.kernels.keys():
            print(f'aux kernel name {name} already in use')

        if type == AuxKernelTypes.ParsedAux:
            kernel = ParsedAux(name,variable,block, **kwargs)
        elif type == AuxKernelTypes.ADRankTwoAux:
            kernel = ADRankTwoAux(name,variable,block, **kwargs)
        elif type == AuxKernelTypes.ADRankTwoScalarAux:
            kernel = ADRankTwoScalarAux(name,variable,block, **kwargs)

        self.kernels[name] = kernel  
