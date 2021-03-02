from networkx.classes.function import restricted_view
from lfr.graphmatch.figmappingmatcher import FIGMappingMatcher
from typing import Dict
from lfr.netlistgenerator.mappinglibrary import MappingLibrary
from lfr.fig.fluidinteractiongraph import FluidInteractionGraph
from reggie.matchpattern import MatchPattern


def match_node_constraints(semantic_information, subgraph, mapping) -> bool:
    # TODO - Check if the constraints match for the subgraph
    # Loop through each of the unique constraints in the overall semantic information
    # Check if the 1) Constraint type matches, 2) if the same nodes in the GM.mapping
    # match the ones denoted by the subgraph LFR
    raise NotImplementedError()


def extract_subgraph_mapping(subgraph, mapping) -> Dict[str, str]:
    ret = dict()
    raise NotImplementedError()
    return ret


def match(fig: FluidInteractionGraph, library: MappingLibrary):
    patterns: Dict[
        str, object
    ] = dict()  # Store the mint and the match pattern object here

    ret = []

    # TODO - Retrun the networkx subgraph views of the of the FIG
    # Step 1 - Generate the match candidates by running the subgraph isomerism for all the items stored in the library
    for (mint, match_pattern_string) in library.get_match_patterns():
        pattern = MatchPattern(match_pattern_string)
        patterns[mint] = pattern
        structural_template = pattern.get_structural_template()
        semantic_information = pattern.get_semantic_template()
        GM = FIGMappingMatcher(fig, structural_template, semantic_information)
        for subgraph in GM.subgraph_isomorphisms_iter():
            print(subgraph)
            # TODO - Not sure what, but work with these subgraphs at the end and then push them through the constraint checking phase
            # This would be a match, figure out how to get the mapping from GM.mapping

            # Loop through each of the candates
            # TODO - Compare the constraints on all the nodes for this for subgraph to confirm the match
            if match_node_constraints(semantic_information, subgraph, GM.mapping):
                # TODO - Extract the specific mapping for the subgraph
                subgraph_mapping = extract_subgraph_mapping(subgraph, GM.mapping)
                ret.append((subgraph, subgraph_mapping))

    return ret
