#!/usr/env/python3

from moose import MOOSEInput
from variables import Variable, Variables, Order, Family

class MooseThermoMechanicalProblem():
    def __init__(self, dependent_input = ""):
        self.moose = MOOSEInput()
        self.dependent_input = dependent_input

    def make_input(self, material_dictionary):
        # make the problem variables
        variables = Variables()
        disp_x = Variable(name="disp_x", order = Order.FIRST, family = Family.LAGRANGE)
        disp_y = Variable(name="disp_y", order = Order.FIRST, family = Family.LAGRANGE)
        disp_z = Variable(name="disp_z", order = Order.FIRST, family = Family.LAGRANGE)

        variables.variables[disp_x.name] = disp_x
        variables.variables[disp_y.name] = disp_y
        variables.variables[disp_z.name] = disp_z

        self.moose.variables = variables

        #### make the global parameters
        from global_parameters import GlobalParameters
        global_params = GlobalParameters(displacements=[disp_x,disp_y,disp_z], volumetric_locking_correction=True)
        self.moose.global_params = global_params

        #### make the mesh
        from mesh import Mesh, MeshObjectTypes, TransformGenerator, TransformTypes
        mesh = Mesh()
        mesh.add_mesh_object("filemesh", type = MeshObjectTypes.FileMeshGenerator, \
            filename = "../divertor-monoblock.e")
        #mesh.add_mesh_object("scale", type = MeshObjectTypes.TransformGenerator, \
        #    input = mesh.mesh_objects["filemesh"], transform = TransformTypes.SCALE, \
        #    vector_value = [1.e-3,1.e-3,1.e-3])
        self.moose.mesh = mesh

        #### make some aux_variables
        from variables import AuxVariable, AuxVariables
        temperature = Variable(name="temperature", order = Order.FIRST, family = Family.LAGRANGE)
        temp_in_C = Variable(name="temp_in_C", order = Order.FIRST, family = Family.LAGRANGE)
        stress_xx = Variable(name="stress_xx_nodal", order = Order.FIRST, family = Family.MONOMIAL)
        stress_yy = Variable(name="stress_yy_nodal", order = Order.FIRST, family = Family.MONOMIAL)
        stress_zz = Variable(name="stress_zz_nodal", order = Order.FIRST, family = Family.MONOMIAL)
        strain_xx = Variable(name="strain_xx_nodal", order = Order.FIRST, family = Family.MONOMIAL)
        strain_yy = Variable(name="strain_yy_nodal", order = Order.FIRST, family = Family.MONOMIAL)
        strain_zz = Variable(name="strain_zz_nodal", order = Order.FIRST, family = Family.MONOMIAL)
        von_mises = Variable(name="vonmises_nodal", order = Order.FIRST, family = Family.MONOMIAL)

        aux_variables = AuxVariables()
        aux_variables.variables[temperature.name] = temperature
        aux_variables.variables[temp_in_C.name] = temp_in_C
        aux_variables.variables[stress_xx.name] = stress_xx
        aux_variables.variables[stress_yy.name] = stress_yy
        aux_variables.variables[stress_zz.name] = stress_zz
        aux_variables.variables[strain_xx.name] = strain_xx
        aux_variables.variables[strain_yy.name] = strain_yy
        aux_variables.variables[strain_zz.name] = strain_zz
        aux_variables.variables[von_mises.name] = von_mises

        self.moose.aux_variables = aux_variables

        #### make some kernels
        from kernels import Kernels, Kernel, ADHeatConduction, ADHeatConductionTimeDerivative, TensorMechanics, ADGravity
        #heat = ADHeatConduction("heat-conduction", variable = temperature, thermal_conductivity = "thermal_conductivity")
        #heat_dt = ADHeatConductionTimeDerivative("heat-conduction-dt", variable = temperature, density = "density", \
        #        specific_heat="specific_heat")
        output = ["strain_xx","strain_yy","strain_zz","vonmises_stress"]
        tensor_mechanics = TensorMechanics(displacements=[disp_x,disp_y,disp_z],generate_output=output,\
                eigenstrain_names="eigenstrain")
        gravity_z = ADGravity("gravity",variable=disp_y, value=-9.81)

        physics_kernels = Kernels()
        #physics_kernels.kernels[heat.name] = heat
        #physics_kernels.kernels[heat_dt.name] = heat_dt
        physics_kernels.kernels["tensor_mechanics"] = tensor_mechanics
        physics_kernels.kernels[gravity_z.name] = gravity_z

        self.moose.kernels = physics_kernels

        #### make some aux kernels
        from kernels import AuxKernels, ParsedAux, ADRankTwoAux, ADRankTwoScalarAux, ScalarType
        from functions import PolynomialFunction
        tempfunction = PolynomialFunction("",[0.0,0.0,0.0,temperature,],\
            coefficients=[0.,0.,0.,1.,-273.15])

        ktoc = ParsedAux("K_to_C", variable=temp_in_C, function=tempfunction, args=temperature)
        aux_stress_xx = ADRankTwoAux(name = "nodal_stress_xx", rank_two_tensor = "stress", variable = stress_xx, index_i = 0, index_j = 0)
        aux_stress_yy = ADRankTwoAux(name = "nodal_stress_yy",rank_two_tensor = "stress", variable = stress_yy, index_i = 1, index_j = 1)
        aux_stress_zz = ADRankTwoAux(name = "nodal_stress_zz",rank_two_tensor = "stress", variable = stress_zz, index_i = 2, index_j = 2)
        aux_strain_xx = ADRankTwoAux(name = "nodal_strain_xx",rank_two_tensor = "total_strain", variable = strain_xx, index_i = 0, index_j = 0)
        aux_strain_yy = ADRankTwoAux(name = "nodal_strain_yy",rank_two_tensor = "total_strain", variable = strain_yy, index_i = 1, index_j = 1)
        aux_strain_zz = ADRankTwoAux(name = "nodal_strain_zz",rank_two_tensor = "total_strain", variable = strain_zz, index_i = 2, index_j = 2)
        aux_von_mises = ADRankTwoScalarAux(name = "nodal_vonmises",rank_two_tensor = "stress", variable = von_mises, scalar_type = ScalarType.VonMisesStress)

        aux_kernels = AuxKernels()
        aux_kernels.kernels[ktoc.name] = ktoc
        aux_kernels.kernels[aux_stress_xx.name] = aux_stress_xx
        aux_kernels.kernels[aux_stress_yy.name] = aux_stress_yy
        aux_kernels.kernels[aux_stress_zz.name] = aux_stress_zz
        aux_kernels.kernels[aux_strain_xx.name] = aux_strain_xx
        aux_kernels.kernels[aux_strain_yy.name] = aux_strain_yy
        aux_kernels.kernels[aux_strain_zz.name] = aux_strain_zz
        aux_kernels.kernels[aux_von_mises.name] = aux_von_mises

        self.moose.aux_kernels = aux_kernels

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
                name = f'{block}-{key}'
                if "density" in key:
                    material = ADPiecewiseLinearInterpolationMaterial(name = name, \
                        variable = temperature, data = material_dictionary[block][key], property = "density", block=block)
                    materials.materials[material.name] = material
                if "youngsmodulus" in key:  
                    material = ADPiecewiseLinearInterpolationMaterial(name = name, \
                        variable = temperature, data = material_dictionary[block][key], property = name, block=block)
                    materials.materials[material.name] = material
                    material = ADComputeVariableIsotropicElasticityTensor(name=f'{block}-elasticity',youngs_modulus=name, \
                        poissons_ratio = 0.33, block=block)
                    materials.materials[material.name] = material   
                    material = ADComputeSmallStrain(name=f'{block}-strain', displacements=[disp_x, disp_y, disp_z], \
                        eigenstrain_names = "eigenstrain", block=block)
                    materials.materials[material.name] = material
                    material = ADComputeLinearElasticStress(name = f'{block}-stress', block=block)
                    materials.materials[material.name] = material   
                if "thermalexpansion" in key:
                    #sh_func = PiecewiseLinear(name=f'{block}-specific_heat-function', \
                    #    function = material_dictionary[block]["specificheat"])
                    #functions.functions[sh_func.name] = sh_func
                    #tc_func = PiecewiseLinear(name=f'{block}-thermal_conductivity-function', \
                    #    function = material_dictionary[block]["thermalconductivity"])
                    #functions.functions[tc_func.name] = tc_func
                    #material = ADHeatConductionMaterial(name = f'{block}-heat', variable = temperature, \
                    #    specific_heat = sh_func,\
                    #    thermal_conductivity = tc_func, block=block)
                    #materials.materials[material.name] = material
                    te_func = PiecewiseLinear(name=f'{block}-thermal_expansion-function', \
                        function = material_dictionary[block]["thermalexpansion"])
                    functions.functions[te_func.name] = te_func
                    material = ADComputeMeanThermalExpansionFunctionEigenstrain(name = f'{block}-thermal_strain',\
                        variable = temperature, thermal_expansion_function_reference_temperature=293.15,\
                        stress_free_temperature = 293.15, eigenstrain_name = "eigenstrain", \
                        thermal_expansion = te_func, block=block)
                    materials.materials[material.name] = material

        
        #### Functions
        #htc_func = PiecewiseFunction(x_data = "293.15 294.15 295.15 296.15 297.15 298.15 299.15 300.15 301.15 302.15 303.15 304.15 305.15 306.15 307.15 308.15 309.15 310.15 311.15 312.15 313.15 314.15 315.15 316.15 317.15 318.15 319.15 320.15 321.15 322.15 323.15 324.15 325.15 326.15 327.15 328.15 329.15 330.15 331.15 332.15 333.15 334.15 335.15 336.15 337.15 338.15 339.15 340.15 341.15 342.15 343.15 344.15 345.15 346.15 347.15 348.15 349.15 350.15 351.15 352.15 353.15 354.15 355.15 356.15 357.15 358.15 359.15 360.15 361.15 362.15 363.15 364.15 365.15 366.15 367.15 368.15 369.15 370.15 371.15 372.15 373.15 374.15 375.15 376.15 377.15 378.15 379.15 380.15 381.15 382.15 383.15 384.15 385.15 386.15 387.15 388.15 389.15 390.15 391.15 392.15 393.15 394.15 395.15 396.15 397.15 398.15 399.15 400.15 401.15 402.15 403.15 404.15 405.15 406.15 407.15 408.15 409.15 410.15 411.15 412.15 413.15 414.15 415.15 416.15 417.15 418.15 419.15 420.15 421.15 422.15 423.15 424.15 425.15 426.15 427.15 428.15 429.15 430.15 431.15 432.15 433.15 434.15 435.15 436.15 437.15 438.15 439.15 440.15 441.15 442.15 443.15 444.15 445.15 446.15 447.15 448.15 449.15 450.15 451.15 452.15 453.15 454.15 455.15 456.15 457.15 458.15 459.15 460.15 461.15 462.15 463.15 464.15 465.15 466.15 467.15 468.15 469.15 470.15 471.15 472.15 473.15 474.15 475.15 476.15 477.15 478.15 479.15 480.15 481.15 482.15 483.15 484.15 485.15 486.15 487.15 488.15 489.15 490.15 491.15 492.15 493.15 494.15 495.15 496.15 497.15 498.15 499.15 500.15 501.15 502.15 503.15 504.15 505.15 506.15 507.15 508.15 509.15 510.15 511.15 512.15",\
        #    y_data = "2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.420000e+04 2.451700e+04 2.546500e+04 2.703400e+04 2.920600e+04 3.195700e+04 3.525800e+04 3.907200e+04 4.335700e+04 4.806700e+04 5.315000e+04 5.855000e+04 6.420800e+04 7.006200e+04 7.604800e+04 8.210000e+04 8.815200e+04 9.413800e+04 9.999200e+04 1.056500e+05 1.110500e+05 1.161300e+05 1.208400e+05 1.251300e+05 1.289400e+05 1.322400e+05 1.349900e+05 1.371700e+05 1.387300e+05 1.396800e+05 1.400000e+05 1.399700e+05 1.398600e+05 1.396900e+05 1.394500e+05 1.391500e+05 1.387800e+05 1.383400e+05 1.378300e+05 1.372600e+05 1.366200e+05 1.359200e+05 1.351600e+05 1.343400e+05 1.334500e+05 1.325100e+05 1.315100e+05 1.304500e+05 1.293400e+05 1.281700e+05 1.269500e+05 1.256800e+05 1.243600e+05 1.230000e+05 1.215900e+05 1.201300e+05 1.186400e+05 1.171000e+05 1.155300e+05 1.139300e+05 1.122900e+05 1.106200e+05 1.089200e+05 1.072000e+05 1.054500e+05 1.036800e+05 1.019000e+05 1.000900e+05 9.827800e+04 9.645000e+04 9.461300e+04 9.277100e+04 9.092400e+04 8.907600e+04 8.722900e+04 8.538700e+04 8.355000e+04 8.172200e+04 7.990600e+04 7.810300e+04 7.631700e+04 7.454900e+04 7.280300e+04 7.107900e+04 6.938200e+04 6.771300e+04 6.607400e+04 6.446800e+04 6.289700e+04 6.136300e+04 5.986800e+04 5.841400e+04 5.700400e+04 5.563800e+04 5.431900e+04 5.305000e+04 5.183000e+04 5.066300e+04 4.954900e+04 4.849100e+04 4.748900e+04 4.654600e+04 4.566100e+04 4.483800e+04 4.407600e+04 4.337600e+04 4.274100e+04 4.217000e+04 4.166400e+04 4.122400e+04 4.085100e+04 4.054500e+04 4.030700e+04 4.013700e+04 4.003400e+04 4.000000e+04 4.003400e+04 4.013700e+04 4.030700e+04 4.054500e+04 4.085100e+04 4.122400e+04 4.166400e+04 4.217000e+04 4.274100e+04 4.337600e+04 4.407600e+04 4.483800e+04 4.566100e+04 4.654600e+04 4.748900e+04 4.849100e+04 4.954900e+04 5.066300e+04 5.183000e+04 5.305000e+04 5.431900e+04 5.563800e+04 5.700400e+04 5.841400e+04")
        #htc_function = PiecewiseLinear(name = "water_htc_function", function = htc_func )
        #functions.functions[htc_function.name] = htc_function
        #htc_material = ADGenericFunctionMaterial(name = "htc_function",\
        #    prop_names = ["htc_function"], prop_values = [htc_function], \
        #    block="cucrzr")
        #materials.materials[htc_material.name] = htc_material

        self.moose.materials = materials
        self.moose.functions = functions

        ####  boundary conditions
        from boundary_conditions import BoundaryCondition, BoundaryConditions, BoundaryConditionTypes, ADNeumannBC, ADDirichletBC, ADConvectiveHeatFluxBC, Pressure
        #heat_load = ADNeumannBC(name="heat_load",variable = temperature, boundary = "heat-load", value ="5e6")
        #htc_bc = ADConvectiveHeatFluxBC(name="htc_bc", variable=temperature, boundary = 'pressure-bc', heat_transfer_coefficient=htc_material, t_infinity=293.15)
        fixed_x = ADDirichletBC(name="fixed-x", variable=disp_x, boundary="fixed-disp", value=0.0)
        fixed_y = ADDirichletBC(name="fixed-y", variable=disp_y, boundary="fixed-y-disp fixed-disp", value=0.0)
        #fixed_z = ADDirichletBC(name="fixed-z", variable=disp_z, boundary="fixed-node-bc", value=0.0)
        pressure = Pressure(name="water-pressure", variable = None, boundary = 'pressure-bc', displacements = [disp_x, disp_y, disp_z], value=0.4e6)

        bcs = BoundaryConditions()
        #bcs.boundary_conditions[heat_load.name] = heat_load
        #bcs.boundary_conditions[htc_bc.name] = htc_bc
        bcs.boundary_conditions[fixed_x.name] = fixed_x
        bcs.boundary_conditions[fixed_y.name] = fixed_y
        #bcs.boundary_conditions[fixed_z.name] = fixed_z
        bcs.boundary_conditions[pressure.name] = pressure

        self.moose.boundary_conditions = bcs

        #### post processors
        from postprocessors import PostProcessor,PostProcessors,PostProcessorTypes, \
            ElementAverageValue, ElementExtremeValue

        min_temp = ElementExtremeValue("min_temp", variable = temp_in_C, value_type = "min")
        ave_temp = ElementAverageValue("ave_temp", variable = temp_in_C)
        max_temp = ElementExtremeValue("max_temp", variable = temp_in_C, value_type = "max")

        min_stress = ElementExtremeValue("min_stress", variable = von_mises, value_type = "min")
        ave_stress = ElementAverageValue("ave_stress", variable = von_mises)
        max_stress = ElementExtremeValue("max_stress", variable = von_mises, value_type = "max")

        post_processors = {}
        post_processors[min_temp.name] = min_temp
        post_processors[ave_temp.name] = ave_temp
        post_processors[max_temp.name] = max_temp
        post_processors[min_stress.name] = min_stress
        post_processors[ave_stress.name] = ave_stress
        post_processors[max_stress.name] = max_stress

        postprocs = PostProcessors()
        postprocs.post_processors = post_processors
        self.moose.post_processors = postprocs

        #### multiapps
        from executioner import ExectutionTypes
        from multiapps import MultiApps, TransientMultiApp, AppTypes
        multi = MultiApps()
        thm = TransientMultiApp(name = "thm", app_type = AppTypes.ThermalHydraulicsApp, \
            input_files = [self.dependent_input], \
            execute_on = ExectutionTypes.TIMESTEP_BEGIN)
        multi.multiapps[thm.name] = thm
        self.moose.multiapps = multi

        #### transfers
        from transfers import MultiAppNearestNodeTransfer,Transfers
        trans = Transfers()
        t_solid = Variable(name = 'T_solid', order = Order.FIRST, family = Family.LAGRANGE )
        transfer = MultiAppNearestNodeTransfer(name = "T_from_thm", source_variable = t_solid, \
            aux_variable = temperature, from_multi_app = thm)
        trans.transfers[transfer.name] = transfer
        self.moose.transfers = trans

        #### executioner
        from executioner import Executioner
        exec = Executioner()
        solve_options = {}
        solve_options["automatic_scaling"] = "true"
        solve_options["solve_type"] = "NEWTON"
        solve_options["type"] = "Transient"
        solve_options["steady_state_detection"] = "true"
        solve_options["line_search"] = "none"
        solve_options["nl_abs_tol"] = "1e-6"
        solve_options["nl_rel_tol"] = "1e-8"
        solve_options["l_tol"] = "1e-6"
        solve_options["l_max_its"] = "100"
        solve_options["nl_max_its"] = "10"
        solve_options["dt"] = "100"
        solve_options["num_steps"] = "20"
        solve_options["petsc_options_iname"] = "-pc_type -pc_hypre_type -pc_hypre_boomeramg_strong_threshold -pc_hypre_boomeramg_coarsen_type -pc_hypre_boomeramg_interp_type"
        solve_options["petsc_options_value"] = "hypre boomeramg 0.7 HMIS ext+i"  
        exec.solve_objects = solve_options
        self.moose.executioner = exec

        #### outputs
        from outputs import Outputs
        output = Outputs(exodus=True, csv=True)
        self.moose.outputs = output

    def write_input(self,filename = "test.i"):
        self.moose.write(filename)
