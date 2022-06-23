from typing import List

import networkx as nx

from lfr.fig.fluidinteractiongraph import FluidInteractionGraph
from lfr.netlistgenerator.constructiongraph.constructiongraph import \
    ConstructionGraph
from lfr.netlistgenerator.constructiongraph.constructionnode import \
    ConstructionNode
from lfr.netlistgenerator.gen_strategies.genstrategy import GenStrategy
from lfr.netlistgenerator.networkmappingoption import (
    NetworkMappingOption, NetworkMappingOptionType)
from lfr.netlistgenerator.primitive import NetworkPrimitive


def add_flow_flow_matching_candidates(
    fig: FluidInteractionGraph,
    variants: List[ConstructionGraph],
    gen_strategy: GenStrategy,
) -> None:
    flow_cns = get_flow_flow_candidates(fig, gen_strategy)
    print("Found New Flow-Flow match nodes:", flow_cns)
    add_flow_flow_candadates_to_variants(variants, flow_cns)
    print("New variant Mappings:", [str(v) for v in variants])


def add_flow_flow_candadates_to_variants(
    variants: List[ConstructionGraph], flow_cns: List[ConstructionNode]
) -> None:
    pass


def get_flow_flow_candidates(
    fig: FluidInteractionGraph, gen_strategy: GenStrategy
) -> List[ConstructionNode]:
    # TODO - go through all the edges and see which ones are between flow-flow graphs
    # If these connectsions are between flow-flow nodes then we need to figure out
    # which ones are part of the same network/connected graphs with only flow nodes
    # The networks with only the flow nodes will need to be covered as a part of.
    # these construction nodes.

    ret = []

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

    # Step 3. Now get the all the disconnected pieces of the graph
    i = 0
    for component in nx.connected_components(fig_copy.to_undirected()):
        print("Flow candidate", component)
        sub = fig_original.subgraph(component)
        # TODO - Decide what the mapping type should be. for now assume that we just a single
        # passthrough type scenario where we don't have to do much work
        nprimitive = NetworkPrimitive(sub, gen_strategy)
        nprimitive.generate_netlist()
        # mapping_option = NetworkMappingOption(nprimitive, mapping_type, sub)
        # Step 4. Create a Construction node for each of the disconnected pieces
        # TODO - Check and see what happens here
        cn = ConstructionNode("flow_network_{}".format(i), nprimitive, sub)

        i += 1
        ret.append(cn)

    return ret
