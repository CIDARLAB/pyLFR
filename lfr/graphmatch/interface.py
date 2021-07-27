from lfr.fig.annotation import DistributeAnnotation
from lfr.graphmatch.figmappingmatcher import FIGMappingMatcher
from typing import Any, Dict, FrozenSet, List, Tuple
from lfr.netlistgenerator.mappinglibrary import MappingLibrary
from lfr.fig.fluidinteractiongraph import FluidInteractionGraph
from lfr.graphmatch.matchpattern import MatchPattern
from lfr.graphmatch.nodefilter import NodeFilter


def bijective_match_node_constraints(
    fig: FluidInteractionGraph,
    semantic_information: Dict[str, NodeFilter],
    subgraph: Dict[str, str],
) -> bool:
    # TODO - Check if the constraints match for the subgraph
    # STEP 1 - generate new unique names for each node to simplify the matching
    # algorihtm

    # STEP 2 - Create a dictionary match_node_dict that has keys which are the set of
    # all the renamed match graph node ID's and values to be the list of all the
    # relationships for those nodes

    # STEP 3 - Create a dictionary fig_node_dict that has keys which are the set of all
    # the renamed FIGNode ID's and values to be the list of all the relationships for
    # those nodes (use DISTRIBUTE ANNOTATION MATCH STRING)

    # STEP 4 - Check if the dictionaries match :

    # RETURN TRUE CONDITIONS
    # 1 - Exact match in the final dictionary (the mapping between the two dictionary
    # keys is a bijection)
    # 2 - TODO - Mapping between the two dictionary keys is a surjection (This will
    # allow us to have composable functiontions)

    # RETIRN FALSE CONDITIONS:
    # 1 - Cannot find node in one of the annotations (this will limit the types of
    # matches) and not allow composable matches for disribution annotations networks
    # 2 - Final dictionary entries do not match:
    # 2.1 - Every entry in teh match node dictionary should be present in the
    # fig_node_dict
    # 2.2 - Assuming coverage is limited to the exact match subgraph in the fig, we
    # need to ensure that

    # Step 1 - Generate new unique names for each node to simplify the matching
    # algorihtm
    # Loop through each of the nodes in the fig and the mapping
    new_ids = {}
    # new_id_counter = 0
    for key, value in subgraph.items():
        # new_ids[key] = str(new_id_counter)
        # new_ids[value] = str(new_id_counter)
        # new_id_counter += 1
        # TODO - easier to debug revert back to counter based system
        new_ids[key] = "{}_{}".format(key, value)
        new_ids[value] = "{}_{}".format(key, value)

    # Step 2 - Create a dictionary match_node_dict that has keys which are the set of
    # all the renamed match graph node ID's and values to be the list of all the
    # relationships for those nodes
    match_node_dict: Dict[FrozenSet[str], List[str]] = {}

    # Create a dictionary to keep all the match_node relationships
    # Stores {relationship_id: [matchnode ids]}
    match_node_relationships: Dict[str, List[str]] = {}
    # Create a dictionary to keep all the node relationship types
    # Stores {relationship_id: relationship_type}
    node_relationship_types: Dict[str, str] = {}

    # Loop through each of the NodeFilters in the semantic information
    for match_node_id, node_filter in semantic_information.items():
        # Put the relationship_id and relationship_type into the coresponding dicts
        # Go through each of the tuples in the node_filter constraints
        for relationship_type, relationship_id in node_filter.get_constraints():
            # If the relationship_id is not in the relationship_id dict, add it
            if relationship_id not in match_node_relationships:
                match_node_relationships[relationship_id] = []
                node_relationship_types[relationship_id] = relationship_type
            # Add the match_node_id to the list of match_node_ids for the
            # relationship_id (We add the newly generated ids to the match_node_dict).
            match_node_relationships[relationship_id].append(new_ids[match_node_id])

    # Populate the match_node_dict with the data from the match_node_relationships
    for (
        relationship_id,
        relationship_match_node_ids,
    ) in match_node_relationships.items():
        # generate a set of all the match_node_ids for the relationship_id
        match_node_ids_set = frozenset(relationship_match_node_ids)
        if match_node_ids_set not in match_node_dict:
            match_node_dict[match_node_ids_set] = []
        # Add the relationship type into the list corresponding to the ids set
        match_node_dict[match_node_ids_set].append(
            node_relationship_types[relationship_id]
        )

    # Step 3 - Create a dictionary fig_node_dict that has keys which are the set of all
    fig_node_dict: Dict[FrozenSet[str], List[str]] = {}
    # Loop throught the fignodes in the subgraph find the corresponding annotations and
    # populate the fig_node_dict
    checked_annotations = []
    for fig_node_id in subgraph.keys():
        fig_node = fig.get_fignode(fig_node_id)
        annotations = fig.get_fig_annotations(fig_node)
        # Generate the set of all the items in the fig_node annotation
        for annotation in annotations:
            # Check if the annotation has already been checked
            if annotations not in checked_annotations:
                checked_annotations.append(annotations)
            else:
                continue

            annotation_set = set()
            skip_annotation = False
            for item in annotation.get_items():
                if isinstance(item, DistributeAnnotation):
                    raise NotImplementedError(
                        "Need to figure out how to define/process nested relationship"
                    )
                else:
                    # TODO - Handle scenarios where the Item is not found in the
                    # mapping scope
                    if item[0].ID in new_ids.keys() and item[1].ID in new_ids.keys():
                        annotation_set.add(new_ids[item[0].ID])
                        annotation_set.add(new_ids[item[1].ID])
                    else:
                        print(
                            'Warning! Rejecting annotation "{}" for consideration in'
                            " DISTRIBUTE RELATIONSHIP Matching since it has items not"
                            " covered by the Primitive".format(annotation)
                        )
                        skip_annotation = True
                        break

            if skip_annotation:
                # Skip adding the annotation since there were fig items outside of the
                # current mapping domain
                continue

            # Add the annotation_set to the fig_node_dict with the corresponding
            # annotation type
            if frozenset(annotation_set) not in fig_node_dict:
                fig_node_dict[frozenset(annotation_set)] = []

            fig_node_dict[frozenset(annotation_set)].append(annotation.match_string)

    # Step 4 - Check if the dictionaries match (is a bijection)
    # Step 4.1 - Check if the relatships between the fig and the match networks are
    # surjective
    # Step 4.1.1 - Check if each of the keys in the match_node_dict is in the
    # fig_node_dict
    for ids_set in match_node_dict.keys():
        if ids_set not in fig_node_dict:
            return False
        # Step 4.1.2 - Check if each of the values in the fig_node_dict is in the
        # match_node_dict
        fig_rels_list = fig_node_dict[ids_set].sort()
        match_rels_list = match_node_dict[ids_set].sort()
        if fig_rels_list != match_rels_list:
            return False
    # Step 4.2 - Check if the relationships between the fig and the match networks are
    # injective
    # Step 4.2.1 - Check if each of the keys in the fig_node_dict is in the
    # match_node_dict
    for ids_set in fig_node_dict.keys():
        if ids_set not in match_node_dict:
            return False
        # Step 4.2.2 - Check if each of the values in the match_node_dict is in the
        # fig_node_dict
        fig_rels_list = fig_node_dict[ids_set].sort()
        match_rels_list = match_node_dict[ids_set].sort()
        if fig_rels_list != match_rels_list:
            return False

    # If we get to this point, then the match network is a bijection
    return True


def get_fig_matches(
    fig: FluidInteractionGraph, library: MappingLibrary
) -> List[Tuple[str, Any]]:
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
            # Compare the constraints on all the nodes for this for subgraph to
            # confirm the match

            distribution_constaints = []
            distribution_annotations = []
            for node_filter in semantic_information.values():
                distribution_constaints.extend(node_filter.get_constraints())

            for fig_id in subgraph.keys():
                fig_node = fig.get_fignode(fig_id)
                distribution_annotations.extend(fig.get_fig_annotations(fig_node))

            # Constraint matching Logic - This logic allows for annotated fig_nodes to
            # be matched against match patterns that dont have any distribtion
            # constraints. The 4 cases shown here describe the different ways in which
            # this logic can work.

            # Case 1 - if subgraph has no distribution annotations and match template
            # has no distribution constraints - SKIP | MATCH

            # Case 2 - if subgraph has no distribution annotations and match template
            # has distribtion constraints - SKIP | NO-MATCH

            # Case 3 - if subgraph has distribution annotations and match
            # template has no distribution constraints - SKIP | MATCH

            # Case 4 - if subgraph has distribution annotations and match template
            # has distribution constraints - NO-SKIP | CHECK-MATCH

            # Case 1 + Case 3 Logic - We only need to check if the distribution
            # constraints are zero (LOGIC REDUCTION)
            if len(distribution_constaints) == 0:
                # No distribution constraints, so we can skip node constraint matching
                print("Found Match: {}".format(mint))
                print(subgraph)

                # MATCH
                ret.append((mint, subgraph))
                # SKIP
                continue

            # Case 2 Logic
            if len(distribution_annotations) == 0 and len(distribution_constaints) > 0:
                # NO-MATCH, SKIP
                continue

            # Case 4 Logic
            if len(distribution_annotations) > 0 and len(distribution_constaints) > 0:
                # Check if the subgraph annotations matche the distribution constraints
                # TODO - Also expand this algorithm to allow for surjective matches.
                # This would allow us to verify the composability of the matches with
                # the library
                if bijective_match_node_constraints(
                    fig, semantic_information, subgraph
                ):
                    # TODO - Extract the specific mapping for the subgraph
                    print("Found Match: {}".format(mint))
                    print(subgraph)

                    ret.append((mint, subgraph))
                else:
                    # NO-MATCH, SKIP
                    continue

    return ret
