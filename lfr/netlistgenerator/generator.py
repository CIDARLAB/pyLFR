from typing import Dict, FrozenSet, List, Optional, Set, Tuple

from pymint.mintdevice import MINTDevice
from pymint.mintlayer import MINTLayerType

from lfr.compiler.module import Module
from lfr.fig.simplification import remove_passthrough_nodes
from lfr.graphmatch.interface import get_fig_matches
from lfr.netlistgenerator import LibraryPrimitivesEntry
from lfr.netlistgenerator.constructiongraph.edge_generation import (
    generate_construction_graph_edges,
)
from lfr.netlistgenerator.constructiongraph.variant_generator import (
    generate_match_variants,
)
from lfr.netlistgenerator.flownetworkmatching import add_flow_flow_matching_candidates
from lfr.netlistgenerator.gen_strategies.dropxstrategy import DropXStrategy
from lfr.netlistgenerator.gen_strategies.dummy import DummyStrategy
from lfr.netlistgenerator.gen_strategies.marsstrategy import MarsStrategy
from lfr.netlistgenerator.mappinglibrary import MappingLibrary
from lfr.netlistgenerator.namegenerator import NameGenerator
from lfr.netlistgenerator.netlist_generation import generate_device
from lfr.postprocessor.mapping import (
    FluidicOperatorMapping,
    NetworkMapping,
    NodeMappingInstance,
    NodeMappingTemplate,
    PumpMapping,
    StorageMapping,
)
from lfr.utils import printgraph


def generate(module: Module, library: MappingLibrary) -> List[MINTDevice]:
    # In order to create the device, we do the following
    # STEP 1 - Simplify the Fluid Interaction Graphs
    # STEP 2 - Initialize the active strategy
    # STEP 3 - Get all the technology mapping matches for the FIG
    # STEP 4 - Eliminate the matches that are exactly the same as the explicit matches
    # STEP 5 - Generate the waste outputs
    # STEP 6 - Generate the mapping variants
    # STEP 6.5 - Generate the flow subgraph matches (TODO - Add test cases for this)
    # STEP 6.10 - Before generating teh device, delete all the variants with incomplete mappings
    # STEP 7 - Generate the control logic network
    # STEP 8 - Generate the connections
    # STEP 9 - Size the components
    # STEP 10 - Size the connections

    # construction_graph = ConstructionGraph()

    # Step 1 - Simplify the Fluid Interaction Graphs
    printgraph(module.FIG, f"{module.name}_FIG")
    remove_passthrough_nodes(module.FIG)
    printgraph(module.FIG, f"{module.name}_FIG_simplified")

    # STEP 2 - Initialize the active strategy
    # TODO - I need to change this DummyStrategy later on
    if library.name == "dropx":
        active_strategy = DropXStrategy(module.FIG)
    elif library.name == "mars":
        # raise NotImplementedError()
        active_strategy = MarsStrategy(module.FIG)
    elif library.name == "hmlp":
        raise NotImplementedError()
    else:
        active_strategy = DummyStrategy(module.FIG)

    # STEP 3 - Get all the technology mapping matches for the FIG
    # Do the reggie matching to find the mapping options
    # This means that we might need to have a forest of construction of graphs
    # as there would be alternatives for each type of mapping
    matches = get_fig_matches(module.FIG, library)
    print(f"Total Matches against library : {len(matches)}")
    for match in matches:
        # Generate an object that is usable going forward (mapping template perhaps)
        print(match)

    # STEP 4 - Eliminate the matches that are exactly the same as the explicit matches
    # Get the explicit mapping and find the explicit mappings here
    explicit_mappings = module.get_explicit_mappings()
    matches, explict_cover_sets = eliminate_explicit_match_alternates(
        matches, explicit_mappings, library
    )

    print(
        "Total matches against library after explicit mapping eliminations:"
        f" {len(matches)}"
    )
    for match in matches:
        print(match)

    # STEP 5 - Generate the waste outputs
    # TODO - Add fignodes to all the orphaned flow nodes for this to function
    # connect_orphan_IO()

    # STEP 6 - Generate the mapping variants
    variants = generate_match_variants(
        matches, module.FIG, library, active_strategy, explict_cover_sets
    )

    # STEP 6.5 -Generate the matches for the flow subgraphs
    add_flow_flow_matching_candidates(module.FIG, variants, active_strategy)

    # STEP 8 - Generate the edges in the construction graph
    print("Generating the construction graph edges...")
    for variant in variants:
        generate_construction_graph_edges(module.FIG, variant)
        variant.print_graph(f"{variant.ID}_construction_graph.dot")

    # STEP 6.10 - Before generating the device, delete all the variants with incomplete coverage of the FIG
    variants = [variant for variant in variants if variant.is_fig_fully_covered()]

    # Perform the various validate using the active strategy
    validated_variants = []
    for variant in variants:
        flow_validation_success = active_strategy.validate_construction_graph_flow(
            variant
        )

        # TODO - Add other kinds of validation here
        # Eg. active_strategy.whatever_else_validation()

        if flow_validation_success:
            validated_variants.append(variant)

    # Now generate the devices for each of the variants
    generated_devices = []
    for variant in validated_variants:
        # Create the device for each of the variants
        name_generator = NameGenerator()

        cur_device = MINTDevice(module.name)

        # Add a MINT Layer so that the device has something to work with
        cur_device.create_mint_layer("0", "0", 0, MINTLayerType.FLOW)

        generate_device(
            construction_graph=variant,
            scaffhold_device=cur_device,
            name_generator=name_generator,
            mapping_library=library,
        )
        # STEP 8 - Generate the control logic network
        # TODO - Whatever this entails (put in the implementation)

        # STEP 9 - Generate the connection optimizations
        # TODO - write the algorithm for carriers and optimize the flows
        # Generate all the unaccounted carriers and waste output lines necessary

        # STEP 10 - Size the components
        # TODO - Size the component netlist

        generated_devices.append(cur_device)

    return generated_devices


def eliminate_explicit_match_alternates(
    matches: List[LibraryPrimitivesEntry],
    explict_mappings: List[NodeMappingTemplate],
    library: MappingLibrary,
) -> Tuple[List[LibraryPrimitivesEntry], List[Set[str]]]:
    """Eliminates the alternatives for explicit matches from the list of matches.

    Args:
        matches (List[LibraryPrimitivesEntry]): List of matches to eliminate from
        explict_mappings (List[NodeMappingTemplate]): The mappings that are explicitly
        defined by the user

    Returns:
        List[Tuple[str, Dict[str, str]]]: _description_
    """
    # extract the fignode ID set from matches
    match_node_set_dict: Dict[FrozenSet, List[LibraryPrimitivesEntry]] = {}
    for match in matches:
        frozen_set = frozenset(match[2].keys())
        if frozen_set not in match_node_set_dict:
            match_node_set_dict[frozen_set] = []
            match_node_set_dict[frozen_set].append(match)
        else:
            match_node_set_dict[frozen_set].append(match)

    # This is the explit match store that we keep track of explicitly defined mappings
    explicit_matches: List[LibraryPrimitivesEntry] = []

    # This is the set of cover sets that are found and returned
    explicit_cover_sets: List[Set[str]] = []

    # Go through each of the explict matches, generate a subgraph and compare against
    # all the matches
    for explicit_mapping in explict_mappings:
        # Only do the explicit mapping if the the mapping object has a technology
        # associated with it else skip it
        if explicit_mapping.technology_string is None:
            continue

        # Generate a subgraph for each of the mapping instance fig
        for instance in explicit_mapping.instances:
            node_set = set()

            # Check what kind of an instance this is
            if isinstance(instance, NodeMappingInstance):
                # This is a single node scenario
                node_set.add(instance.node.ID)
            elif isinstance(instance, FluidicOperatorMapping):
                node_set.add(instance.node.ID)

            elif isinstance(instance, StorageMapping):
                node_set.add(instance.node.ID)

            elif isinstance(instance, PumpMapping):
                node_set.add(instance.node.ID)

            elif isinstance(instance, NetworkMapping):
                node_set = set()
                node_set.union(set([node.ID for node in instance.input_nodes]))
                node_set.union(set([node.ID for node in instance.output_nodes]))

            if frozenset(node_set) in match_node_set_dict:
                # This is an explicit match
                # Remove the explicit match from the list of matches
                print(
                    "Eliminating match: {}".format(
                        match_node_set_dict[frozenset(node_set)]
                    )
                )
                match_node_set_dict[frozenset(node_set)].clear()

            # Now generate a match tuple for this instance
            match_primitive_uid: Optional[str] = None
            match_technology_string = explicit_mapping.technology_string
            match_mapping: Dict[str, str] = {}

            # TODO - Retouch this part if we ever go into modifying how the matches are
            # generated if we use the match string coordinates (use the match interface
            # for this) (function - generate_single_match)

            # Check what kind of an instance this is
            if isinstance(instance, NodeMappingInstance):
                # This is a single node scenario
                match_mapping[instance.node.ID] = "v1"
            elif isinstance(instance, FluidicOperatorMapping):
                match_mapping[instance.node.ID] = "v1"

            elif isinstance(instance, StorageMapping):
                match_mapping[instance.node.ID] = "v1"

            elif isinstance(instance, PumpMapping):
                match_mapping[instance.node.ID] = "v1"

            elif isinstance(instance, NetworkMapping):
                for i in range(len(instance.input_nodes)):
                    node = instance.input_nodes[i]
                    match_mapping[node.ID] = f"vi{i}"
                for i in range(len(instance.output_nodes)):
                    node = instance.output_nodes[i]
                    match_mapping[node.ID] = f"vo{i}"

            # Rewrite the matchid for the explicit matches
            # based on the library entry
            if frozenset(node_set) in match_node_set_dict:
                # Find the primitive that matches the technology string
                for primitive in match_node_set_dict[frozenset(node_set)]:
                    if primitive[1] == explicit_mapping.technology_string:
                        # This is the match we want to replace
                        # Replace the match id with the match tuple
                        match_primitive_uid = primitive[0]
                # This is an explicit match
                # Remove the explicit match from the list of matches
                print(
                    "Eliminating match: {}".format(
                        match_node_set_dict[frozenset(node_set)]
                    )
                )
                match_node_set_dict[frozenset(node_set)].clear()

            # If the match_primitive ID is None, we need to query a match from the
            # library
            if match_primitive_uid is None:
                primitives_with_technology = library.get_primitives(
                    match_technology_string
                )
                # TODO - We need to have a better way to pick between the primitives
                # as a temprorary fix we just pick the first one
                match_primitive_uid = primitives_with_technology[0].uid

            # Add this match tuple to the list of matches
            match_tuple: LibraryPrimitivesEntry = (
                match_primitive_uid,
                match_technology_string,
                match_mapping,
            )

            explicit_matches.append(match_tuple)
            # This is something we need to return to the to the caller
            explicit_cover_sets.append(node_set)

    # Modify the matches list
    eliminated_matches = []
    for match_tuple_list in match_node_set_dict.values():
        for match_tuple in match_tuple_list:
            eliminated_matches.append(match_tuple)

    # Add the explicit matches to the list of matches
    eliminated_matches.extend(explicit_matches)

    return (eliminated_matches, explicit_cover_sets)


def connect_orphan_IO():
    print("Implement the orphan io generation system")


def __check_if_passthrough(sub) -> bool:
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
