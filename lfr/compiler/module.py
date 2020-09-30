from typing import List
from lfr.netlistgenerator.explicitmapping import ExplicitMapping
from lfr.fig.fignode import FIGNode, IO, Flow
from lfr.fig.fluidinteractiongraph import FluidInteractionGraph
from .moduleio import ModuleIO
from lfr.fig.interaction import FluidFluidCustomInteraction, FluidFluidInteraction, FluidIntegerInteraction, FluidNumberInteraction, FluidProcessInteraction, Interaction, InteractionType


class Module(object):
    def __init__(self, name):
        self.name = name
        self._imported_modules: List[Module] = []
        self._io = dict()
        self.FIG = FluidInteractionGraph()
        self.fluids = dict()
        self.mappings: List[ExplicitMapping] = []

    def add_io(self, io: ModuleIO):
        self._io[io.id] = io
        f = IO(io.id, io.type)
        self.FIG.add_fignode(f)

    def get_io(self, name: str) -> ModuleIO:
        if name in self._io:
            return self._io[name]
        else:
            raise Exception("ModuleIO:{0} not found !".format(name))

    def add_fluid(self, fluid: Flow):
        self.fluids[fluid.id] = fluid
        self.FIG.add_fignode(fluid)

    def get_fluid(self, name: str) -> FIGNode:
        return self.FIG.get_fignode(name)

    def add_fluid_connection(self, item1id: str, item2id: str) -> None:
        source = self.FIG.get_fignode(item1id)
        target = self.FIG.get_fignode(item2id)
        self.FIG.connect_fignodes(source, target)

    def add_fluid_custom_interaction(self, item: Flow, operator: str, interaction_type: InteractionType) -> Interaction:
        # Check if the item exists
        finteraction = FluidProcessInteraction(item, operator)
        self.FIG.add_interaction(finteraction)
        return finteraction

    def add_finteraction_custom_interaction(self, item: Interaction, operator: str, interaction_type: InteractionType) -> Interaction:
        # Check if the item exists
        # TODO: create finteraction factory method and FluidInteraction
        # finteraction = FluidInteraction(fluid1=item, interactiontype=interaction_type, custominteraction= operator)
        finteraction = FluidProcessInteraction(item, operator)
        self.FIG.add_interaction(finteraction)
        return finteraction

    def add_fluid_custominteraction(self, fluid1: Flow, fluid2: Flow, interaction: str) -> Interaction:
        finteraction = FluidFluidCustomInteraction(
            fluid1, fluid2, interaction)
        self.FIG.add_interaction(finteraction)
        return finteraction

    def add_fluid_fluid_interaction(self, fluid1: Flow, fluid2: Flow, interaction_type: InteractionType) -> Interaction:

        fluid_interaction = FluidFluidInteraction(fluid1, fluid2, interaction_type)
        self.FIG.add_interaction(fluid_interaction)

        return fluid_interaction

    def add_fluid_finteraction_interaction(self, fluid1: Flow, finteraction: Interaction, interaction_type: InteractionType):
        # TODO: Create new factory method for creating this kind of fluid interaction
        new_fluid_interaction = FluidFluidInteraction(fluid1, finteraction, interaction_type)

        # self.FIG.add_fluid_finteraction_interaction(fluid1, finteraction, new_fluid_interaction)
        self.FIG.add_interaction(new_fluid_interaction)

        return new_fluid_interaction

    def add_finteraction_finteraction_interaction(self, f_interaction1: Interaction, f_interaction2: Interaction, interaction_type: InteractionType) -> Interaction:
        # TODO - Revisit this to fix the fluid data mappings

        new_fluid_interaction = FluidFluidInteraction(f_interaction1, f_interaction2, interaction_type)

        self.FIG.add_interaction(new_fluid_interaction)

        return new_fluid_interaction

    def add_interaction_output(self, output: Flow, interaction: Interaction):
        self.FIG.connect_fignodes(output, interaction)

    def add_fluid_numeric_interaction(self, fluid1: FIGNode, number, interaction_type: InteractionType) -> Interaction:
        # finteraction = FluidInteraction(fluid1=fluid1, interactiontype=interaction)
        finteraction = None

        if interaction_type is InteractionType.METER:
            finteraction = FluidNumberInteraction(fluid1, number, interaction_type)
        elif interaction_type is InteractionType.DILUTE:
            finteraction = FluidNumberInteraction(fluid1, number, interaction_type)
        elif interaction_type is InteractionType.DIVIDE:
            finteraction = FluidIntegerInteraction(fluid1, number, interaction_type)
        else:
            raise Exception("Unsupported Numeric Operator")

        self.FIG.add_interaction(finteraction)

        return finteraction

    def add_mapping(self, mapping: ExplicitMapping):
        self.mappings.append(mapping)

    def __str__(self):
        ret = "Name : " + self.name + "\n"
        for key in self._io.keys():
            ret += self._io[key].__str__()
            ret += "\n"
        return ret
