from lfr.graphmatch.figmappingmatcher import FIGMappingMatcher
from typing import Dict
from lfr.netlistgenerator.mappinglibrary import MappingLibrary
from lfr.fig.fluidinteractiongraph import FluidInteractionGraph
from lfr.graphmatch.matchpattern import MatchPattern
from lfr.graphmatch.nodefilter import NodeFilter


def match_node_constraints(
    fig: FluidInteractionGraph,
    structural_template,
    semantic_information: Dict[str, NodeFilter],
    subgraph,
    mapping,
) -> bool:
    # TODO - Check if the constraints match for the subgraph
    # Loop through each of the unique constraints in the overall semantic information
    # Check if the 1) Constraint type matches, 2) if the same nodes in the GM.mapping
    # match the ones denoted by the subgraph LFR

    # Extract the subgraph pairings in the to know what fig node matches what matchnode
    pattern_graph_coloring_map = dict()
    pattern_graph_node_filters = dict()

    for fig_vertex_id, parttern_vertex_id in mapping.items():
        # Get Constraints for fig_vertex_id and the NodeFilter for the pattern_vertex_id
        fig_node = fig.get_fignode(fig_vertex_id)
        node_filter = semantic_information[parttern_vertex_id]

        # Load up all the constraints for this particular fignode
        pattern_graph_coloring_map[fig_node] = node_filter.get_constriants()
        pattern_graph_node_filters[fig_node] = node_filter

    # TODO - Now check to see if all the constraints are a match in node filter
    for fig_node in pattern_graph_coloring_map.keys():
        # Get the constraints on the fig
        fig_constraints = fig.get_fig_annotations(fig_node)

    return True


def get_fig_matches(fig: FluidInteractionGraph, library: MappingLibrary):
    patterns: Dict[
        str, MatchPattern
    ] = dict()  # Store the mint and the match pattern object here

    ret = []

    # TODO - Retrun the networkx subgraph views of the of the FIG
    # Step 1 - Generate the match candidates by running the subgraph isomerism for all
    # the items stored in the library
    for (mint, match_pattern_string) in library.get_match_patterns():
        if match_pattern_string == "" or match_pattern_string is None:
            print("Warning ! - Missing match string for mint- {}".format(mint))
            continue
        pattern = MatchPattern(match_pattern_string)
        patterns[mint] = pattern
        structural_template = pattern.get_structural_template()
        semantic_information = pattern.get_semantic_template()
        GM = FIGMappingMatcher(fig, structural_template, semantic_information)

        for subgraph in GM.subgraph_isomorphisms_iter():
            # Work with these subgraphs at the end and then push them through the
            # constraint checking phase

            # This would be a match, figure out how to get the mapping from GM.mapping

            # Loop through each of the candates
            # TODO - Compare the constraints on all the nodes for this for subgraph to
            # confirm the match
            if match_node_constraints(
                fig, structural_template, semantic_information, subgraph, GM.mapping
            ):
                # TODO - Extract the specific mapping for the subgraph
                print("Found Match: {}".format(mint))
                print(subgraph)

                ret.append((mint, subgraph))

    return ret
