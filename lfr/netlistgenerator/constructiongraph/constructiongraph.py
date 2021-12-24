from lfr.fig.fignode import Flow, Signal
from typing import List, Tuple
from lfr.fig.fluidinteractiongraph import FluidInteractionGraph
from lfr.netlistgenerator.constructiongraph.constructionnode import ConstructionNode
from lfr.fig.fignode import FIGNode
import networkx as nx
from enum import Enum


class VariantType(Enum):
    SUBSTITUTION = 1
    ADDITION = 2


class ConstructionGraph(nx.Graph):
    """
    This class is a sub-class of networkx.DiGraph.
    It acts as a proxy datastructure for generating the device netlist.
    """

    def __init__(self, id: str, fig: FluidInteractionGraph) -> None:
        super().__init__()
        self._id = id
        self._fig = fig
        self._construction_nodes: List[ConstructionNode] = []

    @property
    def ID(self) -> str:
        return self._id

    def get_fignode_cn(self, fig_node: FIGNode):
        for cn in self._construction_nodes:
            if fig_node.ID in cn._fig_subgraph.nodes:
                return cn

    def add_construction_node(
        self, construction_node: ConstructionNode, variant_type: VariantType
    ) -> None:

        # TODO - Just add the construction node into the graph
        if variant_type == VariantType.SUBSTITUTION:
            # Remove the existing construction node that has an intersecting fig cover
            # with the new construction node
            for cn in self._construction_nodes:
                if cn.fig_cover.intersection(construction_node.fig_cover):
                    self.remove_construction_node(cn)
                    break
            else:
                raise ValueError(
                    "No construction node found with an intersecting fig cover"
                )
            self._construction_nodes.append(construction_node)
            self.add_node(construction_node.ID)
        elif variant_type == VariantType.ADDITION:
            self._construction_nodes.append(construction_node)
            self.add_node(construction_node.ID)
        else:
            raise ValueError("Invalid variant type")

    def remove_construction_node(self, construction_node: ConstructionNode) -> None:
        # Remove the construction node from the graph
        self.remove_node(construction_node.ID)
        self._construction_nodes.remove(construction_node)

    def generate_construction_edges(self) -> None:
        """
        This method generates the connections between the nodes in the graph.
        """
        # Check if the FIG cover of neighboring construction nodes
        # and generate connection candidates
        self._bridge_channel_networks()
        # Step 1 - Generate a map where the key is a fig node and the value is a list of
        # construction nodes that have a fig node in their fig_subgraph
        fig_node_to_cn_map = self._generate_fignode_to_cn_map()
        # Step 2 - Generate edges for between the construction node with the biggest
        # fig_cover and the rest of the nodes
        for fig_node in fig_node_to_cn_map:
            cn_list = fig_node_to_cn_map[fig_node]
            # Get the construction node with the biggest fig_cover
            cn_with_biggest_fig_cover = max(cn_list, key=lambda x: len(x.fig_cover))
            # Get the rest of the construction nodes
            cn_list.remove(cn_with_biggest_fig_cover)
            # Generate edges between the construction nodes
            for cn in cn_list:
                self.add_edge(cn_with_biggest_fig_cover.ID, cn.ID)

        # Step 3 - Generate edges between the construction nodes that have fig nodes
        # that are neighbors of each other
        # Utilize the networkx.Graph.neighbors method to get the neighbors of each fig
        # node in the fignode map
        for fig_node in fig_node_to_cn_map:
            fig_node_neighbors = self._fig.neighbors(fig_node)
            for fig_node_neighbor in fig_node_neighbors:
                # Get the construction nodes that have the neighbor fig node
                cn_list = fig_node_to_cn_map[fig_node_neighbor]
                # Get the construction nodes that have the original fig node
                cn_list_with_fig_node = fig_node_to_cn_map[fig_node]
                # Generate edges between the construction nodes
                for cn in cn_list_with_fig_node:
                    for cn_neighbor in cn_list:
                        self.add_edge(cn.ID, cn_neighbor.ID)

    def _generate_fignode_to_cn_map(self):
        fig_node_to_cn_map = {}
        for cn in self._construction_nodes:
            for fig_node in cn.fig_subgraph.nodes:
                if fig_node.ID not in fig_node_to_cn_map:
                    fig_node_to_cn_map[fig_node.ID] = []
                fig_node_to_cn_map[fig_node.ID].append(cn)
        return fig_node_to_cn_map

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

    def check_variant_criteria(
        self, node: ConstructionNode
    ) -> Tuple[bool, VariantType]:
        # Check if the node's fig mapping overlaps with the fig cover of the
        # existing construction nodes according to the axioms definined. If it does
        # return True, else return False.
        for cn in self._construction_nodes:
            if cn.fig_cover == node.fig_cover:
                return True, VariantType.SUBSTITUTION
            elif node.has_border_overlap(cn):
                return True, VariantType.ADDITION
        else:
            return False, VariantType.ADDITION

    def generate_variant(self, new_id: str) -> "ConstructionGraph":
        # Generate a variant of the construction graph
        ret = ConstructionGraph(new_id, self._fig)
        for cn in self._construction_nodes:
            ret.add_construction_node(cn, VariantType.ADDITION)
        # Get the existing edges and add them to the new graph
        for edge in self.edges:
            ret.add_edge(edge[0], edge[1])
        return ret

    def _bridge_channel_networks(self) -> None:
        # TODO - Bridge the channel networks
        # Find all the passthrough nodes in the fig
        # Make a copy of the fig and eliminate all the fig nodes that are either not
        # FLOW or are not covered by the construction nodes
        copy_fig = self._fig.copy()
        for cn in self._construction_nodes:
            for fig_node in cn.fig_subgraph.nodes:
                copy_fig.remove_node(fig_node.ID)
        # Delete all the non-flow nodes
        for node in copy_fig.nodes:
            if (
                isinstance(node, Flow) is not True
                and isinstance(node, Signal) is not True
            ):
                copy_fig.remove_node(node.ID)

        # Get all the disconnected components in the fig
        components = list(nx.connected_components(copy_fig))
        # Check if each of the components are pass through or not
        for component in components:
            is_passthrough = self.__check_if_passthrough(component)
            if is_passthrough is True:
                # Generate an edge bewtween the passthrough nodes
                self.__generate_edge_between_passthrough_nodes(component)

    def __check_if_passthrough(self, sub) -> bool:
        """Checks if its a passthrough chain

        Args:
            sub (subgraph): subgraph

        Returns:
            bool: Return true if its a single chain of flow channels
        """
        in_count = 0
        out_count = 0
        for node in list(sub.nodes):
            inedges = list(sub.in_edges(node))
            outedges = list(sub.out_edges(node))
            if len(inedges) == 0:
                in_count += 1
            if len(outedges) == 0:
                out_count += 1

        if in_count == 1 and out_count == 1:
            return True
        else:
            return False

    def __generate_edge_between_passthrough_nodes(
        self,
        sub,
    ) -> None:
        # Get the fig node to cn map
        fig_node_to_cn_map = self._generate_fignode_to_cn_map()
        # Generate a pass through construciton node
        # If it getting till here we know for a fact that the subgraph is a passthrough and has 1 input and 1 output node
        # Get the in node and the out node
        in_node = None
        out_node = None
        for node in list(sub.nodes):
            if sub.in_degree(node) == 0:
                in_node = node
            if sub.out_degree(node) == 0:
                out_node = node

        # Find the neighbooring fig nodes
        if in_node is None or out_node is None:
            raise ValueError(
                "In and out nodes are not found, cannot apply passthrough connection in"
                " construction graph, check passthrough candidate identification logic"
            )
        in_neighbors = list(sub.neighbors(in_node))
        out_neighbors = list(sub.neighbors(out_node))
        # Find the corresponding construction nodes
        in_cn_list = fig_node_to_cn_map[in_neighbors[0].ID]
        out_cn_list = fig_node_to_cn_map[out_neighbors[0].ID]
        # If construction nodes are the same, throw and error since we can cant have
        # passthrough if its looping around
        for in_cn in in_cn_list:
            if in_cn in out_cn_list:
                raise ValueError(
                    "Encountered situation where in_cn is also out_cn, cannot have self"
                    " loops"
                )
        # Now for each of the cases 1->1 , 1->n, n->1, n->n, n->m cases generate
        # connections
        if len(in_cn_list) == 1 and len(out_cn_list) == 1:
            # 1->1
            self.add_edge(in_cn_list[0], out_cn_list[0])
        elif len(in_cn_list) == 1 and len(out_cn_list) > 1:
            # 1->n
            for out_cn in out_cn_list:
                self.add_edge(in_cn_list[0], out_cn)
        elif len(in_cn_list) > 1 and len(out_cn_list) == 1:
            # n->1
            for in_cn in in_cn_list:
                self.add_edge(in_cn, out_cn_list[0])
        elif len(in_cn_list) > 1 and len(out_cn_list) == len(in_cn_list):
            # n->n
            for in_cn, out_cn in zip(in_cn_list, out_cn_list):
                self.add_edge(in_cn, out_cn)
        elif (
            len(in_cn_list) > 1
            and len(out_cn_list) > 1
            and len(in_cn_list) != len(out_cn_list)
        ):
            # n->m
            for in_cn in in_cn_list:
                for out_cn in out_cn_list:
                    self.add_edge(in_cn, out_cn)

        raise NotImplementedError()
