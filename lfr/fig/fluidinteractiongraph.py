from typing import List
from lfr.fig.fignode import FIGNode, ValueNode
from lfr.fig.interaction import Interaction, FluidFluidInteraction, FluidProcessInteraction, FluidNumberInteraction, FluidIntegerInteraction, InteractionType
from networkx import nx


class FluidInteractionGraph(nx.DiGraph):

    def __init__(self, data=None, val=None, **attr) -> None:
        super(FluidInteractionGraph, self).__init__()
        self._fignodes = dict()
        # self._fluid_interactions = dict()
        self._gen_id = 0

    def add_fignode(self, node: FIGNode) -> None:
        self._fignodes[node.id] = node
        self.add_node(node.id)

    def get_fignode(self, id: str):
        if id in self._fignodes.keys():
            return self._fignodes[id]
        else:
            return None

    def contains_fignode(self, fluid_object: FIGNode) -> bool:
        return fluid_object.id in self.fluids.keys()

    def add_interaction(self, interaction: Interaction):
        if interaction.id not in self._fignodes.keys():
            self._fignodes[interaction.id] = interaction
        else:
            raise Exception("Interaction already present in the FIG: {0}".format(interaction.id))

        if isinstance(interaction, FluidFluidInteraction):
            self.__add_fluid_fluid_interaction(interaction)

        elif isinstance(interaction, FluidProcessInteraction):
            self.__add_single_fluid_interaction(interaction)

        elif isinstance(interaction, FluidNumberInteraction):
            self.__add_fluid_number_interaction(interaction)

        elif isinstance(interaction, FluidIntegerInteraction):
            self.__add_fluid_integer_interaction(interaction)

        else:
            raise Exception("Invalid Interaction Type found here")

    def connect_fignodes(self, source: FIGNode, target: FIGNode):
        if source.id not in self._fignodes.keys():
            raise Exception("Unable to add interaction because of missing flow: {0}".format(source.id))
        if target.id not in self._fignodes.keys():
            raise Exception("Unable to add interaction because of missing flow: {0}".format(target.id))

        self.add_edge(source.id, target.id)

    def get_interactions(self) -> List[Interaction]:
        return [self._fluid_interactions[key] for key in self._fluid_interactions.keys()]

    def __str__(self):
        return self.edges.__str__()

    # ---------- HELPER METHODS -----------

    def __get_val_node_id(self) -> str:
        self._gen_id += 1
        return "val_{0}".format(self._gen_id)

    def __add_fluid_fluid_interaction(self, interaction: FluidFluidInteraction) -> None:
        # Check if flow exists
        if interaction.fluids[0].id not in self._fignodes.keys():
            raise Exception("Unable to add interaction because of missing flow: {0}".format(interaction.fluids[0].id))
        if interaction.fluids[1].id not in self._fignodes.keys():
            raise Exception("Unable to add interaction because of missing flow: {0}".format(interaction.fluids[1].id))

        self.add_node(interaction.id)
        self.add_edge(interaction.fluids[0].id, interaction.id)

        # Figure out how we want to connect FIGNodes
        if interaction.type is InteractionType.SIEVE:
            # In the case of a SIEVE interaction, we need to add the second
            # FIGNode as an output
            self.add_edge(interaction.id, interaction.fluids[1].id)
        else:
            self.add_edge(interaction.fluids[1].id, interaction.id)

        # TODO: Need to add an output node

    def __add_single_fluid_interaction(self, interaction: FluidProcessInteraction) -> None:
        if interaction.fluid.id not in self._fignodes.keys():
            raise Exception("Unable to add interaction because of missing flow: {0}".format(interaction.fluid.id))

        self.add_node(interaction.id)
        self.add_edge(interaction.fluid.id, interaction.id)

        # TODO: Need to add an output node

    def __add_fluid_number_interaction(self, interaction: FluidNumberInteraction) -> None:
        if interaction.fluid.id not in self._fignodes.keys():
            raise Exception("Unable to add interaction because of missing flow: {0}".format(interaction.fluids[0].id))

        # Create new Value node
        val_node = ValueNode(self.__get_val_node_id(), interaction.value)
        self._fignodes[val_node.id] = val_node

        self.add_node(interaction.id)
        self.add_edge(interaction.fluid.id, interaction.id)
        self.add_edge(val_node.id, interaction.id)

    def __add_fluid_integer_interaction(self, interaction: FluidIntegerInteraction) -> None:
        if interaction.fluid.id not in self._fignodes.keys():
            raise Exception("Unable to add interaction because of missing flow: {0}".format(interaction.fluids[0].id))

        # Create new Value node
        val_node = ValueNode(self.__get_val_node_id(), interaction.value)
        self._fignodes[val_node.id] = val_node

        self.add_node(interaction.id)
        self.add_edge(interaction.fluid.id, interaction.id)
        self.add_edge(val_node.id, interaction.id)
