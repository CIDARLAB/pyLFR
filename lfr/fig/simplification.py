from typing import List
from lfr.fig.fignode import Flow
from lfr.fig.fluidinteractiongraph import FluidInteractionGraph
import networkx as nx


"""FIG Simplification

This class consists of all the methods that can be used to simplify/reduce 
the fluid interaction graph.
"""


def remove_passthrough_nodes(fig: FluidInteractionGraph) -> None:
    """Remove all the passthrough nodes from the fluid interaction graph.

    Args:
        fig: The fluid interaction graph to remove the passthrough nodes from.
    """

    # Step 1. Do a shallow copy of the graph
    # Step 2. Remove all the fignodes that are not Flow
    # Step 3. Now get the all the disconnected pieces of the graph
    # Step 4. Create a Construction node for each of the disconnected pieces
    # Return all the constructions nodes

    # Step 1. Do a shallow copy of the graph
    fig_original = fig
    fig_copy = fig.copy(
        as_view=False
    )  # Note this does not copy anything besides the nx.DiGraph at the moment

    # Step 2. Remove all the fignodes that are not Flow
    remove_list = []
    for node_id in fig_copy.nodes:
        node = fig_original.get_fignode(node_id)
        if node.match_string != "FLOW":
            remove_list.append(node_id)

    for node_id in remove_list:
        fig_copy.remove_node(node_id)

    i = 0
    # Step 3. Now get the all the disconnected pieces of the graph
    for component in nx.connected_components(fig_copy.to_undirected()):
        print("Flow candidate:", component)
        sub = fig_original.subgraph(component)
        # TODO - Decide what the mapping type should be. for now assume that we just a
        # single passthrough type scenario where we don't have to do much work
        is_passthrough = __check_if_passthrough(sub)
        if is_passthrough:
            print("Passthrough found:", component)
            # Do the required remove candidate
            # Find the input and output nodes
            input_fignode = find_input_node(sub)
            output_fignode = find_output_node(sub)

            # Find which nodes are connected to the input and output nodes
            # Find the incoming neighbors of the input node
            incoming_neighbors = [
                edge[0] for edge in list(fig_original.in_edges(input_fignode))
            ]
            # Find the outgoing neighbors of the output node
            outouting_neighbors = [
                edge[1] for edge in list(fig_original.out_edges(output_fignode))
            ]

            # Delete all the nodes in the component
            for fig_node in component:
                fig_original.remove_node(fig_node)

            # If |incoming_neighbors| == 1 and |outouting_neighbors| == 1 : delete the
            # whole component and connect the input and the output else create a single
            # flow node and make the connections
            if len(incoming_neighbors) == 1 and len(outouting_neighbors) == 1:
                print("Removing the component:", component)
                # Connect the input and output nodes
                fig_original.add_edge(incoming_neighbors[0], outouting_neighbors[0])
            else:
                if input_fignode == output_fignode:
                    print(
                        "Since its a single flow node, we are skipping the component:",
                        component,
                    )
                    continue
                # Create a new FLOW node
                flow_node = Flow(f"FLOW_component_replacement_{i}")
                i += 0
                print("Replacing the component with:", flow_node)
                # Add the flow node to the graph
                fig_original.add_fignode(flow_node)

                # Connect the input and output nodes
                for incoming_neighbor_id in incoming_neighbors:
                    incoming_neighbor = fig_original.get_fignode(incoming_neighbor_id)
                    fig_original.connect_fignodes(incoming_neighbor, flow_node)

                for outouting_neighbor_id in outouting_neighbors:
                    outgoing_neighbor = fig_original.get_fignode(outouting_neighbor_id)
                    fig_original.connect_fignodes(flow_node, outgoing_neighbor)


def __check_if_passthrough(sub: nx.DiGraph) -> bool:
    # Return true if its a single chain of flow channels
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


def find_input_node(sub: nx.DiGraph) -> str:
    for node in list(sub.nodes):
        inedges = list(sub.in_edges(node))
        if len(inedges) == 0:
            return node
    raise Exception("No input node found")


def find_output_node(sub: nx.DiGraph) -> str:
    for node in list(sub.nodes):
        outedges = list(sub.out_edges(node))
        if len(outedges) == 0:
            return node
    raise Exception("No input node found")
