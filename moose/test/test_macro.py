#!/usr/env/python
import sys

sys.path.append("..")

from unittest import TestCase

def test_mesh():
    from moose.mesh import Mesh
    mesh = Mesh()
    mesh.add_mesh_object("filemesh",1,filename="mesh.e")
    mesh.add_mesh_object("scale",2,input=mesh.mesh_objects["filemesh"], vector_value=[0.01,0.01,0.01], transform=5)
    print(mesh)

def test_variables(): 
    from moose.variables import Variables
    variables = Variables()
    variables.add_variable("disp_x",1,1,"")
    variables.add_variable("disp_y",1,1,"")
    variables.add_variable("disp_z",1,1,"")
    print(variables)

def test_globalparams():
    from moose.variables import Variables
    variables = Variables()
    variables.add_variable("disp_x",1,1,"")
    variables.add_variable("disp_y",1,1,"")
    variables.add_variable("disp_z",1,1,"")

    from moose.global_parameters import GlobalParameters
    globalparams = GlobalParameters(displacements=[variables.variables["disp_x"],variables.variables["disp_y"],variables.variables["disp_z"]], volumetric_locking_correction=True)
    print(globalparams)

def test_auxvariables():
    from moose.variables import AuxVariables
    aux_variables = AuxVariables()
    aux_variables.add_variable("tempinc",2,2,"")
    print(aux_variables)

def test_kernels():
    from moose.kernels import Kernels
    kernels = Kernels()

    from moose.variables import Variables
    variables = Variables()

    variables.add_variable("disp_x",1,1,"")
    variables.add_variable("disp_y",1,1,"")
    variables.add_variable("disp_z",1,1,"")

    variables.add_variable("temperature",1,1,"")
    kernels.add_kernel("test",1,variables.variables["disp_x"],block=None, thermal_conductivity = 'thermal_conductivity')
    kernels.add_kernel("test2",2,variables.variables["temperature"],block=None, specific_heat="specific_heat", density_name="density")
    kernels.add_kernel('test3',3,None,block=None,displacements=[variables.variables["disp_x"],variables.variables["disp_y"],variables.variables["disp_z"]], generate_output=["strain_xx","strain_yy","strain_zz","vonmises_stress"],eigenstrain_names="eigenstrain")
    kernels.add_kernel('test4',4,variables.variables["disp_z"],block=None,value=-9.81)
    print(kernels)

def test_functions():
    from moose.variables import Variables
    from moose.functions import PolynomialFunction
    variables = Variables()
    variables.add_variable("temperature",1,1,"")
    tempfunction = PolynomialFunction("",[0.0,0.0,0.0,variables.variables["temperature"]], \
    coefficients=[0.,0.,0.,1.,-273.15])
    
def test_auxkernels():
    from moose.kernels import AuxKernels
    aux_kernels = AuxKernels()

    from moose.variables import AuxVariables
    aux_variables = AuxVariables()
    aux_variables.add_variable("tempinc",1,1,"")
    
    from moose.variables import Variables
    variables = Variables()
    variables.add_variable("temperature",1,1,"")

    from moose.functions import PolynomialFunction
    tempfunction = PolynomialFunction("",[0.0,0.0,0.0,variables.variables["temperature"]], \
    coefficients=[0.,0.,0.,1.,-273.15])

    aux_kernels.add_kernel("test1",1,aux_variables.variables["tempinc"],block=None,function=tempfunction,args=variables.variables["temperature"])
    aux_kernels.add_kernel("test2",2,aux_variables.variables["tempinc"],block=None, rank_two_tensor="stress", index_i=0, index_j=0 )
    aux_kernels.add_kernel("test3",3,aux_variables.variables["tempinc"],block=None, rank_two_tensor="stress", scalar_type=1)
    
    print(aux_kernels)

def test_boundaryconditions():
    from moose.variables import Variables
    variables = Variables()
    variables.add_variable("temperature",1,1,"")
    variables.add_variable("disp_x",1,1,"")
    variables.add_variable("disp_y",1,1,"")
    variables.add_variable("disp_z",1,1,"")
    from moose.boundary_conditions import BoundaryConditions
    bcs = BoundaryConditions()
    bcs.add_boundary_condition("test",1,variables.variables["temperature"],\
                               "side",value="7.0")
    bcs.add_boundary_condition("test2",2,variables.variables["temperature"],\
                               "side",value="7.0") 
    bcs.add_boundary_condition("test3",3,variables.variables["temperature"],\
                               "side",heat_transfer_coefficient="7.0", t_infinity="273.15")  
    bcs.add_boundary_condition("test4",4,None,\
                               "side",displacements=[variables.variables["disp_x"],variables.variables["disp_y"],variables.variables["disp_z"]], value="7.0") 
        
    print(bcs)

def test_components():
    from moose.components import (
        Components,
        FlowChannel1Phase,
        InletMassFlowRateTemperature1Phase,
        Outlet1Phase,
        JunctionOneToOne1Phase,
        VolumeJunction1Phase,
        HeatTransferFromExternalAppTemperature1Phase,
        HeatTransferFromSpecifiedTemperature1Phase
    )
    components = {}
    component = FlowChannel1Phase(
        name="pipe1",
        position=[0,0,0],
        orientation=[1, 0, 0],
        length=1.0,
        n_elems=20,
        A=0.1,
        D_h=1,
        f=0.01,
    )
    components[component.name] = component
    component = HeatTransferFromSpecifiedTemperature1Phase("heattrans", "pipe1", 300.0)
    components[component.name] = component
    component = HeatTransferFromExternalAppTemperature1Phase("heattrans", "pipe1")
    components[component.name] = component
    component = InletMassFlowRateTemperature1Phase("inlet", temperature=300, input="pipe1:in", m_dot=10.0)
    component = InletMassFlowRateTemperature1Phase("inlet", temperature=300, input=components["pipe1"], m_dot=10.0)
    components[component.name] = component
    try:
        component = InletMassFlowRateTemperature1Phase("inlet", temperature=300, input="pipe1", m_dot=10.0)
    except ValueError:
        pass
    else:
        raise AssertionError("Missed ValueError for InletMassFlowRateTemperature1Phase with incorrect kwarg 'input'")

    component = VolumeJunction1Phase("junction1", "pipe1:in pipe2:out", volume=10.0, position=[1,0,0])
    components[component.name] = component
    component = JunctionOneToOne1Phase("junction1", "pipe1:in pipe2:out")
    components[component.name] = component
    component = Outlet1Phase("outlet", "pipe1:out", 1e5)
    components[component.name] = component

    comps = Components()
    comps.components = components
    print(comps)

def test_materials():
    from moose.variables import Variables
    variables = Variables()
    variables.add_variable("temperature",1,1,"")
    
    from moose.functions import ParsedFunction, PolynomialFunction, PiecewiseFunction, PiecewiseLinear
    poly = PolynomialFunction([variables.variables["temperature"],0.0,0.0, \
                               variables.variables["temperature"]], \
                               coefficients=[1.,2.,3.,4.,5.])
    
    func = ParsedFunction("specific_heat",poly)

    from moose.materials import Materials
    mats = Materials()
    mats.add_material(name="name1",type=2,block="block1",data=poly,property="specific_heat", \
                      variable=variables.variables["temperature"])

    piece = PiecewiseFunction("sh",[300,500],[10,12])
    piece_linear = PiecewiseLinear("sh", axis="x", x=[300,500],y=[10,12])
    mats.add_material("name2",type=1,block="block1",data=piece,property="thermal_conductivity", \
                      variable=variables.variables["temperature"])
    mats.add_material("name3",type=3,block="block1",specific_heat=piece,thermal_conductivity=piece, \
                      variable=variables.variables["temperature"])
    mats.add_material("name4",type=3,block="block1",specific_heat=piece_linear,thermal_conductivity=piece_linear, \
                      variable=variables.variables["temperature"])
    print(mats)

def test_outputs():
    from moose.outputs import Outputs
    output = Outputs(csv=True,exodus=True,print_linear_residuals=False)
    print(output)
