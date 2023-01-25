#!/usr/env/python3

from moose import MOOSEInput
from variables import Variable, Variables, Order, Family

class MooseTHMProblem():
    def __init__(self):
        self.moose = MOOSEInput()

    def make_input(self, material_dictionary):
        #### make some variables
        # NB in the TH all variables are automatically created by MOOSE, you
        # only need to store any that you create for auxkernels

        t_solid = Variable(name = "T_solid", order = 1, family = 1)

        #### make the fluid properties
        from fluidproperties import FluidProperties, FluidProperty, SimpleFluidProperties, StiffenedGasFluidProperties
        fluid_properties = FluidProperties()
        #fluid = SimpleFluidProperties(name = "water", bulk_modulus = 2.0e9, \
        #    cp = 4194, cv = 4186, density0 = 1000, fp_type = "single-phase-fp", \
        #    molar_mass = 0.018, porepressure_coefficient = 1.0, specific_entropy = 300, \
        #    thermal_conductivity = 0.6, thermal_expansion = 0.000214, viscosity = 0.001)
        fluid = StiffenedGasFluidProperties(name = "water", gamma = 2.35, cv = 4187, \
            q = -0.1167e7, p_inf = 1.e9, q_prime = 0, M = 0.018, k = 0.6, mu = 1.0e-3, \
            rho_c = 1149.9, T_c = 648.05)
        fluid_properties.fluidproperties[fluid.name] = fluid
        self.moose.fluid_properties = fluid_properties

        #### closures 
        from closures import Closures, Closures1PhaseSimple
        closures = Closures()
        simple_fluid = Closures1PhaseSimple(name="simple_closure")
        closures.closures[simple_fluid.name] = simple_fluid
        self.moose.closures = closures

        #### Materials and Functions
        from materials import Materials, Material, ADHeatConductionMaterial, \
            ADPiecewiseLinearInterpolationMaterial, ADComputeVariableIsotropicElasticityTensor, \
            ADComputeLinearElasticStress,ADComputeSmallStrain, ADComputeMeanThermalExpansionFunctionEigenstrain, \
            ADGenericFunctionMaterial
        from functions import Functions, PiecewiseFunction, PolynomialFunction, PiecewiseLinear

        materials = Materials()
        functions = Functions()

        # assumes materials are in the form [block][property]
        for block in material_dictionary.keys():
            for key in material_dictionary[block].keys():
                # in the thermal hydraulics problem the material belongs to a block
                # called 'hs:blockname
                name = f'{block}-{key}'
                blockname = f'hs:{block}'
                if "density" in key:
                    material = ADPiecewiseLinearInterpolationMaterial(name = name, \
                        variable = t_solid, data = material_dictionary[block][key], property = "density", block=blockname)
                    materials.materials[material.name] = material
                if "specificheat" in key:
                    material = ADPiecewiseLinearInterpolationMaterial(name = name, \
                        variable = t_solid, data = material_dictionary[block][key], property = "specific_heat", block=blockname)
                    materials.materials[material.name] = material
                if "thermalconductivity" in key:
                    material = ADPiecewiseLinearInterpolationMaterial(name = name, \
                        variable = t_solid, data = material_dictionary[block][key], property = "thermal_conductivity", block=blockname)
                    materials.materials[material.name] = material   

        # set the moose materials
        self.moose.materials = materials

        # add some components
        from components import Components, HeatStructureFromFile3D, \
            HSBoundaryRadiation, HSBoundaryHeatFlux, FlowChannel1Phase, \
            InletMassFlowRateTemperature1Phase, Outlet1Phase, \
            HeatTransferFromHeatStructure3D1Phase

        components = {}
        heat_structure = HeatStructureFromFile3D(name = "hs", file = "../divertor-monoblock.e", \
            position = [0,0,0], initial_T = 300.0)
        components[heat_structure.name] = heat_structure
        component = HSBoundaryRadiation(name = "radiation_boundary", \
            boundary = "hs:radiation-bc", heat_structure = heat_structure, \
            t_ambient = 300, emissivity = 0.8)    
        components[component.name] = component
        component = HSBoundaryHeatFlux(name = "heat_flux_boundary", \
            boundary = "hs:heat-load", heat_structure = heat_structure, \
            q = 1.0e6)
        components[component.name] = component
        component = FlowChannel1Phase(name = "pipe1", position = [0,0,0], \
            orientation = [0,0,1], length = 0.2, n_elems = 200, \
            closures = simple_fluid, \
            A = "${fparse pi * 0.006 * 0.006}", \
            D_h = "${fparse 4. * pi * 0.006 * 0.006 / 0.012 }", \
            f = 0.0, fp = fluid, initial_T = 300, \
            initial_p = 1e5, initial_vel = 0.1)
        components[component.name] = component
        component = InletMassFlowRateTemperature1Phase(name = "inlet", \
            input = components["pipe1"], m_dot = 0.1, temperature = 300)
        components[component.name] = component
        component = Outlet1Phase(name = "outlet", input = components["pipe1"], \
            pressure = 1e5)
        components[component.name] = component
        component = HeatTransferFromHeatStructure3D1Phase(name = "hxconn", \
            heat_flux_perimeter = "${fparse 4 * 0.0094248}", \
            flow_channels = [components["pipe1"]], boundary = "hs:pressure-bc", \
            Hw = 12.e3, heat_structure = heat_structure)
        components[component.name] = component
        comps = Components()
        comps.components = components
        self.moose.components = comps

        #### post processors
        from postprocessors import PostProcessor,PostProcessors,PostProcessorTypes, \
            ElementAverageValue, ElementExtremeValue

        blocks = ""
        for block in material_dictionary.keys():
            blockname = f'hs:{block}'
            blocks = blockname + " "

        min_temp = ElementExtremeValue("min_temp", variable = t_solid, value_type = "min", block = blocks)
        ave_temp = ElementAverageValue("ave_temp", variable = t_solid, block = blocks)
        max_temp = ElementExtremeValue("max_temp", variable = t_solid, value_type = "max", block = blocks)

        post_processors = {}
        post_processors[min_temp.name] = min_temp
        post_processors[ave_temp.name] = ave_temp
        post_processors[max_temp.name] = max_temp

        postprocs = PostProcessors()
        postprocs.post_processors = post_processors
        self.moose.post_processors = postprocs

        #### executioner
        from executioner import Executioner
        exec = Executioner()
        solve_options = {}
        solve_options["type"] = "Transient"
        solve_options["dt"] = "100"
        solve_options["num_steps"] = "20"
        solve_options["steady_state_detection"] = "true"
        solve_options["abort_on_solve_fail"] = "true"
        solve_options["solve_type"] = 'NEWTON'
        solve_options["line_search"] = 'basic'
        solve_options["nl_rel_tol"] = '1e-6'
        solve_options["nl_abs_tol"] = '5e-7'
        solve_options["nl_max_its"] = '40'
        solve_options["l_tol"] = '1e-7'
        solve_options["l_max_its"] = '100'
        exec.solve_objects = solve_options
        self.moose.executioner = exec

        #### outputs
        from outputs import Outputs
        output = Outputs(exodus=True, csv=True)
        self.moose.outputs = output

    def write_input(self,filename = "test.i"):
        self.moose.write(filename)

