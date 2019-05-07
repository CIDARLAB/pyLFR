from networkx import nx
from .fluid import Fluid
from .fluidinteraction import FluidInteraction


class FluidInteractionGraph(nx.DiGraph):

    def __init__(self):
        super(FluidInteractionGraph, self).__init__()
        self.fluids = dict()
        self.fluidinteractions = dict()

    def addfluidnode(self, fluid: Fluid):
        self.fluids[fluid.id] = fluid
        self.add_node(fluid.id)

    def getfluid(self, name):
        if name in self.fluids.keys():
            return self.fluids[name]
        else:
            return None

    def addfluidinteraction(self, fluid: Fluid, fluid2: Fluid, interaction: FluidInteraction):
        if fluid.id not in self.fluids.keys():
            raise Exception("Cannot add interaction because " + fluid.id + " is not in the fluid interaction graph")
        if fluid2.id not in self.fluids.keys():
            raise Exception("Cannot add interaction because " + fluid2.id + " is not in the fluid interaction graph")

        if interaction.id in self.fluidinteractions.keys():
            raise Exception("Cannot add interaction because " + interaction.id + " is already present")
        else:
            self.fluidinteractions[interaction.id] = interaction
            self.add_node(interaction.id)
            self.add_edge(fluid.id, interaction.id)
            self.add_edge(fluid2.id, interaction.id)

    def __str__(self):
        return self.nodes
