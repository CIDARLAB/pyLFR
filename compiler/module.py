from .fluidinteractiongraph import FluidInteractionGraph
from .fluid import Fluid
from .moduleio import ModuleIO
from .fluidinteraction import FluidInteraction, InteractionType


class Module(object):
    def __init__(self, name):
        self.name = name
        self.io = dict()
        self.intermediates = []
        self.FIG = FluidInteractionGraph()
        self.fluids = dict()

    def add_io(self, io: ModuleIO):
        self.io[io.id] = io
        f = Fluid(io.id)
        self.FIG.addfluidnode(f)

    def get_io(self, name: str) -> ModuleIO:
        if name in self.io:
            return self.io[name]
        else:
            raise Exception("ModuleIO:{0} not found !".format(name))

    # def addintermediate(self, intermeidate):
    #     # TODO: Make the fluid interaction graph
    #     self.intermediates.append(intermeidate)
    #     f = Fluid(intermeidate)
    #     # TODO: Create an example with intermediates
    #     self.G.add_node(f)

    def add_fluid(self, fluid: Fluid):
        self.FIG.addfluidnode(fluid)

    def get_fluid(self, name: str):
        return self.FIG.getfluid(name)

    def add_fluid_connection(self, item1id: str, item2id: str) -> None:
        self.FIG.add_fluid_connection(item1id, item2id)


    def add_fluid_custom_interaction(self, item: Fluid, operator: str, interaction_type: InteractionType )-> FluidInteraction:
        #Check if the item exists
        finteraction = FluidInteraction(item, interactiontype=interaction_type, custominteraction= operator)
        self.FIG.add_singlefluid_interaction(item, finteraction)
        return finteraction


    def add_finteraction_custom_interaction(self, item: FluidInteraction, operator: str, interaction_type: InteractionType )-> FluidInteraction:
        #Check if the item exists
        #TODO: create finteraction factory method and FluidInteraction
        finteraction = FluidInteraction(fluid1=item, interactiontype=interaction_type, custominteraction= operator)
        self.FIG.add_singleinteraction_interaction(item, finteraction)
        return finteraction

    def add_fluid_custominteraction(self, fluid1: Fluid, fluid2: Fluid, interaction: str) -> FluidInteraction:
        finteraction = FluidInteraction(
            fluid1, fluid2, InteractionType.TECHNOLOGY_PROCESS, interaction)
        self.FIG.add_fluid_interaction(fluid1, fluid2, finteraction)
        return finteraction

    def add_fluid_fluid_interaction(self, fluid1: Fluid, fluid2: Fluid, interaaction_type: InteractionType) -> FluidInteraction:
        
        fluid_interaction = FluidInteraction(fluid1, fluid2, interaaction_type)

        self.FIG.add_fluid_interaction(fluid1, fluid2, fluid_interaction)

        return fluid_interaction

    def add_fluid_finteraction_interaction(self, fluid1: Fluid, finteraction: FluidInteraction, interaction_type: InteractionType):
        #TODO: Create new factory method for creating this kind of fluid interaction
        new_fluid_interaction = FluidInteraction(fluid1, finteraction, interaction_type)

        self.FIG.add_fluid_finteraction_interaction(fluid1, finteraction, new_fluid_interaction)

        return new_fluid_interaction

    def add_interaction_output(self, output: Fluid, interaction: FluidInteraction):
        self.FIG.attach_interaction_output(output, interaction)

    def add_fluid_numeric_interaction(self, fluid1: Fluid, number, interaction: InteractionType)-> FluidInteraction:
        finteraction = FluidInteraction(fluid1 = fluid1, interactiontype=interaction)
        finteraction.interaction_data['value'] = number

        self.FIG.add_singlefluid_interaction(fluid1, finteraction)

        return finteraction

    def __str__(self):
        ret = "Name : " + self.name + "\n"
        for key in self.io.keys():
            ret += self.io[key].__str__()
            ret += "\n"
        return ret
