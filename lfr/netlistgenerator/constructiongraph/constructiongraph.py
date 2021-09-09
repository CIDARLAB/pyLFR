from lfr.fig.fluidinteractiongraph import FluidInteractionGraph
from lfr.netlistgenerator.constructiongraph.constructionnode import ConstructionNode
import networkx as nx
from enum import Enum


class VariantType(Enum):
    SUBSTITUTION = 1
    ADDITION = 2


class ConstructionGraph(nx.DiGraph):
    """
    This class is a sub-class of networkx.DiGraph.
    It acts as a proxy datastructure for generating the device netlist.
    """

    def __init__(self, fig: FluidInteractionGraph) -> None:
        super().__init__()
        self._fig = fig
        # TODO - figure out if we need to create a new type of construction node
        self._construction_nodes = []

    def add_construction_node(
        self, construction_node: ConstructionNode, variant_type: VariantType
    ) -> None:

        # TODO - Just add the construction node into the graph
        pass

    def substitute_construction_node(
        self, old_construction_node, new_construction_node: ConstructionNode
    ) -> None:
        # TODO - replace the construction node with the new construction node
        pass

    def generate_connections(self) -> None:
        """
        This method generates the connections between the nodes in the graph.
        """
        # TODO - Check if the FIG cover of neighboring construction nodes
        # and generate connection candidates
        pass

    def is_fig_fully_covered(self) -> bool:
        """
        This method checks if the FIG is fully covered by the construction graph
        """
        # TODO - Check if all the fig nodes are covered by construction nodes fig_subgraph
        # Create a list of all the fig node ids
        # Go through each of the construction nodes and the corresponding fig subgraph nodes
        # If the fig subgraph node is not in the list of fig node ids, then the graph is not fully covered
        pass
