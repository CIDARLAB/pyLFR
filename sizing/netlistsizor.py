from .dafd import DAFDSizingAdapter, PerformanceConstraint, FunctionalConstraint, GeometryConstraint 
from compiler.fluidinteractiongraph import FluidInteractionGraph

class NetlistSizor:

    def __init__(self, netlist, fig:FluidInteractionGraph):
        super().__init__()
        self.device = netlist
        self.fig = fig


    def size_netlist(self):
        print("Sizing the device...")
        #TODO: Make this general
        droplet_adapter = DAFDSizingAdapter(self.device)

        #Generate the functional constriants
        print("Sizing the Fluidic Operations...")
        #1.1: First go through each of the operators to size them for functionality
        for interaction in self.fig.get_interactions():
            print("Interaction Data: ", interaction.interaction_data)
        
        #dummy dafd call
        droplet_adapter.size_performance_constraints(None)
        #1.2: Size the Connections/Channels

        #1.3: Iteratively do something ?

        #1.4: Meh ?

