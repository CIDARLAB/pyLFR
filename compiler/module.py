from .fluidinteractiongraph import FluidInteractionGraph
from .fluid import Fluid
from .fluidinteraction import FluidInteraction, InteractionType


class Module(object):
    def __init__(self, name):
        self.name = name
        self.io = dict()
        self.intermediates = []
        self.G = FluidInteractionGraph()
        self.fluids = dict()

    def addio(self, io):
        self.io[io.name] = io
        f = Fluid(io.name)
        self.G.addfluidnode(f)

    def getio(self, name):
        return self.io[name]

    def addintermediate(self, intermeidate):
        #TODO: Make the fluid interaction graph
        self.intermediates.append(intermeidate)
        f = Fluid(intermeidate)
        self.G.add_node(f)

    def getfluid(self, name: str):
        return self.G.getfluid(name)

    def addfluidcustominteraction(self, fluid1: Fluid, fluid2: Fluid, interaction: str):
        finteraction = FluidInteraction(fluid1, fluid2, InteractionType.TECHNOLOGY_PROCESS, interaction)
        self.G.addfluidinteraction(fluid1, fluid2, finteraction)

    def printgraph(self):
        print(self.G)

    def __str__(self):
        ret = "Name : " + self.name + "\n"
        for key in self.io.keys():
            ret += self.io[key].__str__()
            ret += "\n"
        return ret





