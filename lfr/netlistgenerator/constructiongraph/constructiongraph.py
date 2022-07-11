from __future__ import annotations
import os

from typing import FrozenSet, List

import networkx as nx
from lfr import parameters

from lfr.fig.fluidinteractiongraph import FluidInteractionGraph
from lfr.netlistgenerator.constructiongraph.constructionnode import ConstructionNode


class ConstructionGraph(nx.DiGraph):
    """
    This class is a sub-class of networkx.DiGraph.
    It acts as a proxy datastructure for generating the device netlist.
    """

    def __init__(self, id: str, fig: FluidInteractionGraph) -> None:
        """Initializes the construction graph

        Args:
            id (str): ID of the construction graph
            fig (FluidInteractionGraph): Fluid interaction graph which the construction
        """
        super().__init__()
        self._id = id
        self._fig = fig
        self._construction_nodes: List[ConstructionNode] = []

    @property
    def ID(self) -> str:
        """Returns the ID of the construction graph

        Returns:
            str: ID of the construction graph
        """
        return self._id

    def add_construction_node(self, construction_node: ConstructionNode) -> None:
        """Adds a construction node to the graph

        Args:
            construction_node (ConstructionNode): Node to add the the construction graph
        """

        self._construction_nodes.append(construction_node)
        self.add_node(construction_node.ID)

    def remove_construction_node(self, construction_node: ConstructionNode) -> None:
        """Remove a construction node from the graph

        Args:
            construction_node (ConstructionNode): Node to remove from the construction
            graph
        """
        # Remove the construction node from the graph
        self.remove_node(construction_node.ID)
        self._construction_nodes.remove(construction_node)

    def get_construction_node(self, id: str) -> ConstructionNode:
        """Returns the construction node with the given id

        Args:
            id (str): ID of the construction node to return

        Raises:
            ValueError: If the construction node with the given id does not exist

        Returns:
            ConstructionNode: Construction node with the given id
        """
        for cn in self._construction_nodes:
            if cn.ID == id:
                return cn
        else:
            raise ValueError("No construction node with id: " + id)

    def connect_nodes(self, node_a: ConstructionNode, node_b: ConstructionNode) -> None:
        """
        This method connects two nodes in the graph.
        """
        self.add_edge(node_a.ID, node_b.ID)

    def is_fig_fully_covered(self) -> bool:
        """
        This method checks if the FIG is fully covered by the construction graph
        """
        # Check if all the fig nodes are covered by construction nodes fig_subgraph
        # Create a set of all the fig node ids
        # Go through each of the construction nodes and the corresponding fig subgraph
        # nodes if the fig subgraph node is not in the list of fig node ids, then the
        # graph is not fully covered
        fig_node_set = set([node for node in self._fig.nodes])
        for cn in self._construction_nodes:
            fig_subgraph = cn.fig_subgraph
            for node in fig_subgraph.nodes:
                if node not in fig_node_set:
                    return False
        else:
            return True

    def generate_variant(self, new_id: str) -> ConstructionGraph:
        # Generate a variant of the construction graph
        ret = ConstructionGraph(new_id, self._fig)
        for cn in self._construction_nodes:
            ret.add_construction_node(cn)
        # Get the existing edges and add them to the new graph
        for edge in self.edges:
            ret.add_edge(edge[0], edge[1])
        return ret

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, ConstructionGraph):
            if self.ID == __o.ID:
                return True
            else:
                return False
        else:
            return False

    def remove_node_for_exact_fig_cover(self, fig_node_cover: FrozenSet[str]) -> None:
        """Removes the construction node which contains the exact fig node cover
        provided.

        This method Removes the construction node which contains the exact fig node
        cover provided. i.e. if the fig_node_cover is {'A', 'B'} and the construction
        should have a fig node mapping of {'A', 'B'}. This covers the cases where the
        mapping is an exact match and you need to substitute the entire construction
        node.

        Use other methods when you need to account for partial cover matches.

        Args:
            fig_node_cover (FrozenSet[str]): A frozen set of fig node IDs which
                represents the exact fig node cover.
        """

        for cn in self._construction_nodes:
            if frozenset(list(cn.fig_subgraph.nodes)) == fig_node_cover:
                self.remove_node(cn.ID)
                break

    def __str__(self):
        ret = "Construction Graph: " + self.ID
        return ret

    def print_graph(self, filename: str) -> None:
        """Prints the graph to a file

        Args:
            filename (str): Name of the file to print the graph to
        """
        tt = os.path.join(parameters.OUTPUT_DIR, filename)
        print("File Path:", tt)
        nx.nx_agraph.to_agraph(self).write(tt)
