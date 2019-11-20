from .fluidinteractiongraph import FluidInteractionGraph
from .fluid import Fluid
from .moduleio import ModuleIO
from .fluidinteraction import FluidInteraction, InteractionType


class Module(object):
    def __init__(self, name):
        self.name = name
        self.io = dict()
        self.intermediates = []
        self.G = FluidInteractionGraph()
        self.fluids = dict()

    def addio(self, io : ModuleIO):
        self.io[io.name] = io
        f = Fluid(io.name)
        self.G.addfluidnode(f)

    def getio(self, name: str) -> ModuleIO:
        if name in self.io:
            return self.io[name]
        else:
            return None

    def addintermediate(self, intermeidate):
        #TODO: Make the fluid interaction graph
        self.intermediates.append(intermeidate)
        f = Fluid(intermeidate)
        #TODO: Create an example with intermediates
        self.G.add_node(f)

    def addfluid(self, fluid: Fluid):
        self.G.addfluidnode(fluid)

    def getfluid(self, name: str):
        return self.G.getfluid(name)

    def addfluidconnection(self, fluid1id: str, fluid2id: str) -> None:
        self.G.addfluidconnection(fluid1id, fluid2id)

    def addfluidcustominteraction(self, fluid1: Fluid, fluid2: Fluid, interaction: str) -> FluidInteraction:
        finteraction = FluidInteraction(fluid1, fluid2, InteractionType.TECHNOLOGY_PROCESS, interaction)
        self.G.addfluidinteraction(fluid1, fluid2, finteraction)
        return finteraction

    def addinteractionoutput(self, output: Fluid, interaction: FluidInteraction):
        self.G.attachinteractionoutput(output, interaction)

    def __str__(self):
        ret = "Name : " + self.name + "\n"
        for key in self.io.keys():
            ret += self.io[key].__str__()
            ret += "\n"
        return ret





