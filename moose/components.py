#!/usr/env/python3

from enum import IntEnum, auto

class ComponentType(IntEnum):
    ElbowPipe1Phase = auto()
    FlowChannel1Phase = auto()
    FormLossFromExternalApp1Phase = auto()
    FormLossFromFunction1Phase = auto()
    FreeBoundary = auto()
    FreeBoundary1Phase = auto()
    GateValve = auto()
    GateValve1Phase = auto()
    HSBoundaryAmbientConvection = auto()
    HSBoundaryExternalAppConvection = auto()
    HSBoundaryExternalAppTemperature = auto()
    HSBoundaryHeatFlux = auto()
    HSBoundaryRadiation = auto()
    HSBoundarySpecifiedTemperature = auto()
    HeatGeneration = auto()
    HeatSourceFromPowerDensity = auto()
    HeatSourceFromTotalPower = auto()
    HeatSourceVolumetric = auto()
    HeatSourceVolumetric1Phase = auto()
    HeatStructure2DCoupler = auto()
    HeatStructure2DRadiationCouplerRZ = auto()
    HeatStructureCylindrical = auto()
    HeatStructureFromFile3D = auto()
    HeatStructurePlate = auto()
    HeatTransferFromExternalAppHeatFlux1Phase = auto()
    HeatTransferFromExternalAppTemperature1Phase = auto()
    HeatTransferFromHeatFlux1Phase = auto()
    HeatTransferFromHeatStructure1Phase = auto()
    HeatTransferFromHeatStructure3D1Phase = auto()
    HeatTransferFromSpecifiedTemperature1Phase = auto()
    InletDensityVelocity1Phase = auto()
    InletMassFlowRateTemperature1Phase = auto()
    InletStagnationEnthalpyMomentum1Phase = auto()
    InletStagnationPressureTemperature1Phase = auto()
    InletVelocityTemperature1Phase = auto()
    JunctionOneToOne = auto()
    JunctionOneToOne1Phase = auto()
    JunctionParallelChannels1Phase = auto()
    Outlet1Phase = auto()
    PrescribedReactorPower = auto()
    Pump1Phase = auto()
    Shaft = auto()
    ShaftConnectedCompressor1Phase = auto()
    ShaftConnectedMotor = auto()
    ShaftConnectedPump1Phase = auto()
    ShaftConnectedTestComponent = auto()
    ShaftConnectedTurbine1Phase = auto()
    SimpleTurbine1Phase = auto()
    SolidWall = auto()
    SolidWall1Phase = auto()
    SupersonicInlet = auto()
    TotalPower = auto()
    VolumeJunction1Phase = auto()

class Component:
    def __init__(self, name = "", **kwargs):
        self.name = name

        # set the kwargs into names        
        for arg in kwargs.keys():
            self.__setattr__(arg, kwargs[arg])

    def __str__(self):
        string =  f'[{self.name}]\n'
        string += f'type={self.type.name}\n'
        
        objects = ["name", "type"]
        
        for key in self.__dict__.keys():
            if key not in objects:
                data = self.__dict__[key]
                if isinstance(data,list):
                    if hasattr(data[0], '__dict__'):
                        data = [x.name for x in data]
                    else:
                        data = [str(x) for x in data]
                    data = ' '.join(data)
                if hasattr(data, '__dict__'):
                    data = data.name
                string += f'{key}="{data}"\n'

        string += '[]\n'
        return string

class HeatStructureFromFile3D(Component):
    def __init__(self, name, file = "", position = [0.,0.,0.], **kwargs):
        super().__init__(name, **kwargs)
        self.file = file
        self.position = position
        self.type = ComponentType.HeatStructureFromFile3D

class HeatTransferFromExternalAppTemperature1Phase(Component):
    def __init__(self, name:str, flow_channel:str, **kwargs):
        super().__init__(name, **kwargs)
        self.flow_channel = flow_channel
        self.type = ComponentType.HeatTransferFromExternalAppTemperature1Phase

class HSBoundaryRadiation(Component):
    def __init__(self, name, t_ambient = 300.0, boundary = [], \
        emissivity = 0.0, heat_structure = "",  **kwargs):
        super().__init__(name, **kwargs)
        self.T_ambient = t_ambient
        self.hs = heat_structure
        self.emissivity = emissivity
        self.boundary = boundary

        self.type = ComponentType.HSBoundaryRadiation

class HSBoundaryHeatFlux(Component):
    def __init__(self,name = '', boundary = "", q = 0.0, heat_structure = None, **kwargs):
        super().__init__(name, **kwargs)
        self.boundary = boundary
        self.q = q
        self.hs = heat_structure
        self.type = ComponentType.HSBoundaryHeatFlux

class FlowChannel1Phase(Component):
    def __init__(self, name = "", A = 0., \
        length = 0 , n_elems = 1, orientation = [1,0,0], \
        position = [0,0,0], **kwargs):

        super().__init__(name, **kwargs)
        self.A = A
        # self.closures = closures # removed kwargs since it can be declared in GlobalParams
        # self.fp = fp
        self.length = length
        self.n_elems = n_elems
        self.orientation = orientation
        self.position = position
        self.type = ComponentType.FlowChannel1Phase

class InletMassFlowRateTemperature1Phase(Component):
    def __init__(self, name = "", temperature = 300, input = None, \
        m_dot = 0.,  **kwargs):
        super().__init__(name,**kwargs)
        self.T = temperature
        self.input = f'{input.name}:in'
        self.m_dot = m_dot        
        self.type = ComponentType.InletMassFlowRateTemperature1Phase

class Outlet1Phase(Component):
    def __init__(self, name = "", input = None, pressure = 0, **kwargs):
        super().__init__(name, **kwargs)
        self.input = f'{input.name}:out'
        self.p = pressure
        self.type = ComponentType.Outlet1Phase

class VolumeJunction1Phase(Component):
    def __init__(self, name, connections, volume, position, **kwargs):
        super().__init__(name, **kwargs)
        self.name = name
        self.volume = volume
        self.position = position
        self.connections = connections
        self.type = ComponentType.VolumeJunction1Phase

class JunctionOneToOne1Phase(Component):
    def __init__(self, name, connections, **kwargs):
        super().__init__(name, **kwargs)
        self.name = name
        self.connections = connections
        self.type = ComponentType.JunctionOneToOne1Phase

class HeatTransferFromHeatStructure3D1Phase(Component):
    def __init__(self, name = "", heat_flux_perimeter = 0., boundary = "", \
        flow_channels = None, heat_structure = None, **kwargs):
        super().__init__(name,**kwargs)
        self.P_hf = heat_flux_perimeter
        self.boundary = boundary
        self.flow_channels = flow_channels
        self.hs = heat_structure
        self.type = ComponentType.HeatTransferFromHeatStructure3D1Phase

class Components:
    def __init__(self):
        self.name = "Components"
        self.components = {}

    def __str__(self):
        string =  f'[{self.name}]\n'
        for component in self.components.keys():
            string += self.components[component].__str__()
        string += '[]\n'
        return string