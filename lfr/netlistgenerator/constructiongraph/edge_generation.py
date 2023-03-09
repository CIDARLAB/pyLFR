from typing import List

from lfr.fig.fluidinteractiongraph import FluidInteractionGraph
from lfr.netlistgenerator.constructiongraph.constructiongraph import ConstructionGraph
from lfr.netlistgenerator.constructiongraph.constructionnode import ConstructionNode

# def _bridge_channel_networks(construction_graph: ConstructionGraph) -> None:
#     # TODO - Bridge the channel networks
#     # Find all the passthrough nodes in the fig
#     # Make a copy of the fig and eliminate all the fig nodes that are either not
#     # FLOW or are not covered by the construction nodes
#     copy_fig = self._fig.copy(as_view=False)
#     for cn in self._construction_nodes:
#         for fig_node in cn.fig_subgraph.nodes:
#             copy_fig.remove_node(fig_node.ID)
#     # Delete all the non-flow nodes
#     for node in copy_fig.nodes:
#         if isinstance(node, Flow) is not True and isinstance(node, Signal) is not True:
#             copy_fig.remove_node(node.ID)

#     # Get all the disconnected components in the fig
#     components = list(nx.connected_components(copy_fig))
#     # Check if each of the components are pass through or not
#     for component in components:
#         is_passthrough = self.__check_if_passthrough(component)
#         if is_passthrough is True:
#             # Generate an edge bewtween the passthrough nodes
#             self.__generate_edge_between_passthrough_nodes(component)


#     def generate_construction_edges(self) -> None:
#         """
#         This method generates the connections between the nodes in the graph.
#         """
#         # Step 1 - Generate a map where the key is a fig node and the value is a list of
#         # construction nodes that have a fig node in their fig_subgraph
#         fig_node_to_cn_map = self._generate_fignode_to_cn_map()

#         # Step 2 - Generate edges for between the construction node with the biggest
#         # fig_cover and the rest of the nodes
#         for fig_node in fig_node_to_cn_map:
#             cn_list = fig_node_to_cn_map[fig_node]
#             # Get the construction node with the biggest fig_cover
#             cn_with_biggest_fig_cover = max(cn_list, key=lambda x: len(x.fig_cover))
#             # Get the rest of the construction nodes
#             cn_list.remove(cn_with_biggest_fig_cover)
#             # Generate edges between the construction nodes
#             for cn in cn_list:
#                 self.add_edge(cn_with_biggest_fig_cover.ID, cn.ID)

#         # Step 3 - Generate edges between the construction nodes that have fig nodes
#         # that are neighbors of each other
#         # Utilize the networkx.Graph.neighbors method to get the neighbors of each fig
#         # node in the fignode map
#         for fig_node in fig_node_to_cn_map:
#             fig_node_neighbors = self._fig.neighbors(fig_node)
#             for fig_node_neighbor in fig_node_neighbors:
#                 # Get the construction nodes that have the neighbor fig node
#                 cn_list = fig_node_to_cn_map[fig_node_neighbor]
#                 # Get the construction nodes that have the original fig node
#                 cn_list_with_fig_node = fig_node_to_cn_map[fig_node]
#                 # Generate edges between the construction nodes
#                 for cn in cn_list_with_fig_node:
#                     for cn_neighbor in cn_list:
#                         self.add_edge(cn.ID, cn_neighbor.ID)

#     def _generate_fignode_to_cn_map(self):
#         fig_node_to_cn_map = {}
#         for cn in self._construction_nodes:
#             for fig_node in cn.fig_subgraph.nodes:
#                 if fig_node.ID not in fig_node_to_cn_map:
#                     fig_node_to_cn_map[fig_node.ID] = []
#                 fig_node_to_cn_map[fig_node.ID].append(cn)
#         return fig_node_to_cn_map


# def __generate_edge_between_passthrough_nodes(
#     construction_graph: ConstructionGraph,
#     sub,
# ) -> None:
#     # Get the fig node to cn map
#     fig_node_to_cn_map = construction_graph: ConstructionGraph._generate_fignode_to_cn_map()
#     # Generate a pass through construciton node
#     # If it getting till here we know for a fact that the subgraph is a passthrough
#     # and has 1 input and 1 output node
#     # Get the in node and the out node
#     in_node = None
#     out_node = None
#     for node in list(sub.nodes):
#         if sub.in_degree(node) == 0:
#             in_node = node
#         if sub.out_degree(node) == 0:
#             out_node = node

#     # Find the neighbooring fig nodes
#     if in_node is None or out_node is None:
#         raise ValueError(
#             "In and out nodes are not found, cannot apply passthrough connection in"
#             " construction graph, check passthrough candidate identification logic"
#         )
#     in_neighbors = list(sub.neighbors(in_node))
#     out_neighbors = list(sub.neighbors(out_node))
#     # Find the corresponding construction nodes
#     in_cn_list = fig_node_to_cn_map[in_neighbors[0].ID]
#     out_cn_list = fig_node_to_cn_map[out_neighbors[0].ID]
#     # If construction nodes are the same, throw and error since we can cant have
#     # passthrough if its looping around
#     for in_cn in in_cn_list:
#         if in_cn in out_cn_list:
#             raise ValueError(
#                 "Encountered situation where in_cn is also out_cn, cannot have construction_graph: ConstructionGraph"
#                 " loops"
#             )
#     # Now for each of the cases 1->1 , 1->n, n->1, n->n, n->m cases generate
#     # connections
#     if len(in_cn_list) == 1 and len(out_cn_list) == 1:
#         # 1->1
#         self.add_edge(in_cn_list[0], out_cn_list[0])
#     elif len(in_cn_list) == 1 and len(out_cn_list) > 1:
#         # 1->n
#         for out_cn in out_cn_list:
#             self.add_edge(in_cn_list[0], out_cn)
#     elif len(in_cn_list) > 1 and len(out_cn_list) == 1:
#         # n->1
#         for in_cn in in_cn_list:
#             self.add_edge(in_cn, out_cn_list[0])
#     elif len(in_cn_list) > 1 and len(out_cn_list) == len(in_cn_list):
#         # n->n
#         for in_cn, out_cn in zip(in_cn_list, out_cn_list):
#             self.add_edge(in_cn, out_cn)
#     elif (
#         len(in_cn_list) > 1
#         and len(out_cn_list) > 1
#         and len(in_cn_list) != len(out_cn_list)
#     ):
#         # n->m
#         for in_cn in in_cn_list:
#             for out_cn in out_cn_list:
#                 self.add_edge(in_cn, out_cn)

#     raise NotImplementedError()


# def generate_construction_graph_edges(construction_graph: ConstructionGraph) -> None:
#     """
#     This method generates the connections between the nodes in the graph.
#     """
#     # Check if the FIG cover of neighboring construction nodes
#     # and generate connection candidates
#     self._bridge_channel_networks()
#     # Step 1 - Generate a map where the key is a fig node and the value is a list of
#     # construction nodes that have a fig node in their fig_subgraph
#     fig_node_to_cn_map = self._generate_fignode_to_cn_map()
#     # Step 2 - Generate edges for between the construction node with the biggest
#     # fig_cover and the rest of the nodes
#     for fig_node in fig_node_to_cn_map:
#         cn_list = fig_node_to_cn_map[fig_node]
#         # Get the construction node with the biggest fig_cover
#         cn_with_biggest_fig_cover = max(cn_list, key=lambda x: len(x.fig_cover))
#         # Get the rest of the construction nodes
#         cn_list.remove(cn_with_biggest_fig_cover)
#         # Generate edges between the construction nodes
#         for cn in cn_list:
#             self.add_edge(cn_with_biggest_fig_cover.ID, cn.ID)

#     # Step 3 - Generate edges between the construction nodes that have fig nodes
#     # that are neighbors of each other
#     # Utilize the networkx.Graph.neighbors method to get the neighbors of each fig
#     # node in the fignode map
#     for fig_node in fig_node_to_cn_map:
#         fig_node_neighbors = self._fig.neighbors(fig_node)
#         for fig_node_neighbor in fig_node_neighbors:
#             # Get the construction nodes that have the neighbor fig node
#             cn_list = fig_node_to_cn_map[fig_node_neighbor]
#             # Get the construction nodes that have the original fig node
#             cn_list_with_fig_node = fig_node_to_cn_map[fig_node]
#             # Generate edges between the construction nodes
#             for cn in cn_list_with_fig_node:
#                 for cn_neighbor in cn_list:
#                     self.add_edge(cn.ID, cn_neighbor.ID)


# def _generate_fignode_to_cn_map(construction_graph: ConstructionGraph):
#     fig_node_to_cn_map = {}
#     for cn in construction_graph.construction_nodes:
#         for fig_node in cn.fig_subgraph.nodes:
#             if fig_node.ID not in fig_node_to_cn_map:
#                 fig_node_to_cn_map[fig_node.ID] = []
#             fig_node_to_cn_map[fig_node.ID].append(cn)
#     return fig_node_to_cn_map


def check_overlap_criteria_1(
    construction_node_a: ConstructionNode, construction_node_b: ConstructionNode
) -> bool:
    """
    This method checks if the two construction nodes overlap in the following
    criteria:
    1.  if the the two nodes have any common fig nodes
    2.  if the overlapping fig nodes are border nodes
    """
    cover_a = set(construction_node_a.fig_subgraph.nodes)
    cover_b = set(construction_node_b.fig_subgraph.nodes)
    overlap_nodes_set = cover_a.intersection(cover_b)

    # TODO - Figure if we need to check if the overlapping nodes are border nodes
    return len(overlap_nodes_set) > 0


def check_adjecent_criteria_1(
    construction_node_a: ConstructionNode,
    construction_node_b: ConstructionNode,
    fig: FluidInteractionGraph,
) -> bool:
    """
    This method checks if the two construction nodes are adjacent in the following
    criteria:

    Args:
        construction_node_a (ConstructionNode): The first construction node
        construction_node_b (ConstructionNode): The second construction node

    Returns:
        bool: True if the two nodes are adjacent, False otherwise
    """
    cover_a = set(construction_node_a.fig_subgraph.nodes)
    cover_b = set(construction_node_b.fig_subgraph.nodes)
    for fig_node_a in cover_a:
        for fig_node_b in cover_b:
            if fig_node_b in fig.neighbors(fig_node_a):
                return True

    return False


def generate_construction_graph_edges(
    fig: FluidInteractionGraph, construction_graph: ConstructionGraph
) -> None:
    # The construction nodes that have overlaps (border nodes) with each other or are
    # neighbors and make the connection between them.

    # Go through all the construction nodes
    cn_nodes = list(construction_graph.nodes)
    for i in range(len(cn_nodes)):
        for j in range(len(cn_nodes)):
            if i == j:
                continue
            source_node_id = cn_nodes[i]
            source_cn_node = construction_graph.get_construction_node(source_node_id)

            target_node_id = cn_nodes[j]
            target_cn_node = construction_graph.get_construction_node(target_node_id)

            # Check if they overlap
            is_overlapped = check_overlap_criteria_1(source_cn_node, target_cn_node)

            if is_overlapped:
                # Check if the two nodes are already connected
                if construction_graph.has_edge(
                    source_node_id, target_node_id
                ) or construction_graph.has_edge(target_node_id, source_node_id):
                    print(
                        f"Nodes {source_node_id}, {target_node_id} has edge, skipping"
                        " adding edge"
                    )
                    continue

                construction_graph.connect_nodes(source_cn_node, target_cn_node)
                continue

            # Check if they are neighbors
            is_neighbor = check_adjecent_criteria_1(source_cn_node, target_cn_node, fig)

            if is_neighbor:
                if construction_graph.has_edge(
                    source_node_id, target_node_id
                ) or construction_graph.has_edge(target_node_id, source_node_id):
                    print(
                        f"Nodes {source_node_id}, {target_node_id} has edge, skipping"
                        " adding edge"
                    )
                    continue

                construction_graph.connect_nodes(source_cn_node, target_cn_node)
                continue
