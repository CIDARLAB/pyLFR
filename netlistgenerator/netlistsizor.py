from .dafd import DAFDSizingAdapter, PerformanceConstraint, FunctionalConstraint, GeometryConstraint, ConstraintList 
from mint.mintdevice import MINTDevice
from compiler.fluidinteractiongraph import FluidInteractionGraph

class NetlistSizor:

    def __init__(self, netlist_generator):
        super().__init__()
        self.device = netlist_generator.device
        self.fig = netlist_generator.devicemodule.FIG
        self.constraints = []
        self.primitive_map = netlist_generator.primitive_map
        self.blacklist_map = netlist_generator.blacklist_map


    def size_netlist(self):
        print("Sizing the device...")
        #TODO: Make this general
        droplet_adapter = DAFDSizingAdapter(self.device)

        #Generate the functional constriants
        print("Sizing the Fluidic Operations...")
        #1.1: First go through each of the operators to size them for functionality
        constraint_list = ConstraintList()
        for interaction in self.fig.get_interactions():
            print("Interaction Type: ", interaction.interactionType)
            print("Interaction Data: ", interaction.interaction_data)
            component = self.device.getComponent(self.blacklist_map[interaction.id]) 
            volume_constraint = FunctionalConstraint()
            volume_constraint.add_target_value('volume', interaction.interaction_data['value'])
            #dummy dafd call
            droplet_adapter.size_component(component.entity, constraint_list)
        
        #1.2: Size the Connections/Channels

        #1.3: Iteratively do something ?

        #1.4: Meh ?

