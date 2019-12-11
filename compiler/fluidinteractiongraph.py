from networkx import nx
from .fluid import Fluid
from .fluidinteraction import FluidInteraction


# TODO - Make this subclass nx.multigraph at a later point
class FluidInteractionGraph(object):

    def __init__(self):
        self.G = nx.DiGraph()
        self.fluids = dict()
        self.fluidinteractions = dict()

    def addfluidnode(self, fluid: Fluid) -> None:
        self.fluids[fluid.id] = fluid
        self.G.add_node(fluid.id)

    def getfluid(self, name):
        if name in self.fluids.keys():
            return self.fluids[name]
        else:
            return None

    def add_fluid_connection(self, item1id: str, item2id: str) -> None:
        if item1id not in self.fluids.keys() and item1id not in self.fluidinteractions.keys():
            raise Exception("Cannot add interaction because " +
                            item1id + " is not in the fluid interaction graph")
        if item2id not in self.fluids.keys() and item2id not in self.fluidinteractions.keys():
            raise Exception("Cannot add interaction because " +
                            item2id + " is not in the fluid interaction graph")

        self.G.add_edge(item1id, item2id)

    def add_fluid_interaction(self, fluid: Fluid, fluid2: Fluid, interaction: FluidInteraction) -> None:
        if fluid.id not in self.fluids.keys():
            raise Exception("Cannot add interaction because " +
                            fluid.id + " is not in the fluid interaction graph")
        if fluid2.id not in self.fluids.keys():
            raise Exception("Cannot add interaction because " +
                            fluid2.id + " is not in the fluid interaction graph")

        if interaction.id in self.fluidinteractions.keys():
            # raise Exception("Cannot add interaction because " + interaction.id + " is already present")
            print("Warning: {0} is already present in the fluid interaction graph".format(
                interaction.id))
        else:
            self.fluidinteractions[interaction.id] = interaction
            self.G.add_node(interaction.id)
            self.G.add_edge(fluid.id, interaction.id)
            self.G.add_edge(fluid2.id, interaction.id)

    def attach_interaction_output(self, output: Fluid, interaction: FluidInteraction) -> None:
        if output.id not in self.fluids.keys():
            raise Exception("Cannot add interaction because " +
                            output.id + " is not in the fluid interaction graph")
        else:
            self.G.add_edge(interaction.id, output.id)

    def add_singlefluid_interaction(self, fluid1: Fluid, interaction: FluidInteraction) -> None:
        if fluid1.id not in self.fluids.keys():
            raise Exception("Cannot add interaction because " +
                            fluid1.id + " is not in the fluid interaction graph")
        
        if interaction.id in self.fluidinteractions.keys():
            # raise Exception("Cannot add interaction because " + interaction.id + " is already present")
            print("Warning: {0} is already present in the fluid interaction graph".format(
                interaction.id))
        else:
            self.fluidinteractions[interaction.id] = interaction
            self.G.add_node(interaction.id)
            self.G.add_edge(fluid1.id, interaction.id)


    def add_fluid_finteraction_interaction(self, fluid1: Fluid, finteraction: FluidInteraction, newinteraction: FluidInteraction):
        if fluid1.id not in self.fluids.keys():
            raise Exception("Cannot add interaction because " +
                            fluid1.id + " is not in the fluid interaction graph")

        if finteraction.id not in self.fluidinteractions.keys():
            # raise Exception("Cannot add interaction because " + interaction.id + " is already present")
            print("Warning: {0} is already present in the fluid interaction graph".format(
                finteraction.id))

        if newinteraction.id in self.fluidinteractions.keys():
            # raise Exception("Cannot add interaction because " + interaction.id + " is already present")
            print("Warning: {0} is already present in the fluid interaction graph".format(
                newinteraction.id))
        else:
            self.fluidinteractions[newinteraction.id] = newinteraction
            self.G.add_node(newinteraction.id)
            self.G.add_edge(fluid1.id, newinteraction.id)
            self.G.add_edge(finteraction.id, newinteraction.id)
        

    def get_input_nodes(self, interaction: str):
        edges = self.G.in_edges(interaction)
        ret = [u for (u, v) in edges]
        # print("TEST3", ret)
        return ret

    def merge_interactions(self, interactions) -> None:
        keep = interactions[0]
        print("Merging interactions:", keep)
        print("All the interactions:", interactions)
        # print("TEST1", self.G.edges())
        # NOTE - Skip the first one because that's the interaction you don't want to mess up
        for interaction in interactions[1:]:

            # Add the incoming input nodes of the fluid interactions to a list
            fluid_inputs = self.get_input_nodes(interaction)
            # print("Removing:", interaction)
            self.G.remove_node(interaction)

            # Add Edges from all input nodes to the fluid interactions
            for fluid_input in fluid_inputs:
                self.G.add_edge(fluid_input, keep)

        # Remove the fluid interactions from the interaction graphs
        for interaction in interactions[1:]:
            del self.fluidinteractions[interaction]

        # print("TEST2", self.G.edges())

    def __str__(self):
        return self.G.edges.__str__()
