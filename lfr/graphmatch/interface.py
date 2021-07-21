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

    # Generate new IDs for each of the nodes from the fig and the netlist matches in
    # the mapping
    # Loop through each of the nodes in the fig and the mapping
    new_ids = {}
    new_id_counter = 0
    for key, value in mapping.items():
        new_ids[key] = str(new_id_counter)
        new_ids[value] = str(new_id_counter)
        new_id_counter += 1

    # Extract the subgraph pairings in the to know what fig node matches what matchnode
    fig_distribution_set = {}
    reggie_distribution_annotations = {}

    for fig_id, reggie_id in mapping.items():

        new_id = new_ids[reggie_id]
        node_filter = semantic_information[reggie_id]

        # Skip getting the constraints for the match nodes
        if len(node_filter.get_constriants()) == 0:
            continue

        for constriant in node_filter.get_constriants():
            if new_id not in reggie_distribution_annotations.keys():
                reggie_distribution_annotations[new_id] = {constriant[1]}
            else:
                reggie_distribution_annotations[new_id].add(constriant[1])

        new_id = new_ids[fig_id]

        try:
            annotations = fig.get_fig_annotations(fig_id)
        except KeyError:
            print("Missing annotation for fig node: {}".format(fig_id))
            continue

        for annotation in annotations:
            if new_id not in fig_distribution_set.keys():
                fig_distribution_set[new_id] = {annotation.id}
            else:
                fig_distribution_set[new_id].add(annotation.id)

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
