import copy
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
from lfr.netlistgenerator.netlist_generation import (
    generate_control_network,
    generate_device,
)
from lfr.netlistgenerator.primitive import ProceduralPrimitive
from lfr.postprocessor.mapping import (
    FluidicOperatorMapping,
    NetworkMapping,
    NodeMappingInstance,
    NodeMappingTemplate,
    PumpMapping,
    StorageMapping,
)
from lfr.postprocessor.constraints import Constraint
from lfr import parameters
from lfr.utils import printgraph
from lfr.fig.autocomplete import connect_orphan_IO


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

    # Standalone 4-port nozzle modules: bind oil IO before FIG simplification
    # so default-netlist oil PORTs are not merged in.
    module.ensure_standalone_diy_component_terminals()
    module.ensure_standalone_droplet_generator_terminals()
    module.ensure_metering_nozzle_terminals()

    # Step 1 - Simplify the Fluid Interaction Graphs
    if getattr(parameters, "PRINT_DEBUG_GRAPHS", False):
        printgraph(module.FIG, f"{module.name}_FIG")
    remove_passthrough_nodes(module.FIG)
    if getattr(parameters, "PRINT_DEBUG_GRAPHS", False):
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
        active_strategy = DummyStrategy(module.FIG, library.name)

    # STEP 3 - Get all the technology mapping matches for the FIG
    # Do the reggie matching to find the mapping options
    # This means that we might need to have a forest of construction of graphs
    # as there would be alternatives for each type of mapping
    matches = get_fig_matches(module.FIG, library)
    print(f"Total Matches against library : {len(matches)}")
    print("Start of Matches")
    for match in matches:
        # Generate an object that is usable going forward (mapping template perhaps)

        print(match)
    print("End of matches")
    # STEP 4 - Eliminate the matches that are exactly the same as the explicit matches
    # Get the explicit mapping and find the explicit mappings here
    explicit_mappings = module.get_explicit_mappings()
    (
        matches,
        explict_cover_sets,
        explicit_constraints_by_cover,
    ) = eliminate_explicit_match_alternates(
        matches, explicit_mappings, library, fig=module.FIG
    )

    print(
        "Total matches against library after explicit mapping eliminations:"
        f" {len(matches)}"
    )

    # STEP 5 - Generate the waste outputs
    # TODO - Add fignodes to all the orphaned flow nodes for this to function
    # connect_orphan_IO()
    connect_orphan_IO(module.FIG)

    # STEP 6 - Generate the mapping variants
    variants = generate_match_variants(
        matches,
        module.FIG,
        library,
        active_strategy,
        explict_cover_sets,
        explicit_constraints_by_cover=explicit_constraints_by_cover,
    )

    for index, variant in enumerate(variants, start=0):
        if getattr(parameters, "PRINT_DEBUG_GRAPHS", False):
            variant_filename = f"variant_{index}_construction.dot"
            variant.print_graph(variant_filename)

    # # STEP 6.5 -Generate the matches for the flow subgraphs
    # add_flow_flow_matching_candidates(module.FIG, variants, active_strategy)

    # STEP 8 - Generate the edges in the construction graph
    for variant in variants:
        generate_construction_graph_edges(module.FIG, variant)

    # STEP 6.10 - Before generating the device, delete all the variants with incomplete coverage of the FIG
    variants = [variant for variant in variants if variant.is_fig_fully_covered()]

    #Skip validation

    # # Perform the various validate using the active strategy
    # validated_variants = []
    # for variant in variants:
    #     flow_validation_success = active_strategy.validate_construction_graph_flow(
    #         variant
    #     )

    #     # TODO - Add other kinds of validation here
    #     # Eg. active_strategy.whatever_else_validation()

    #     if flow_validation_success:
    #         validated_variants.append(variant)

    # Now generate the devices for each of the variants
    generated_devices = []
    #unvalidated variants
    for variant in variants:
        # Create the device for each of the variants
        name_generator = NameGenerator()

        cur_device = MINTDevice(module.name)

        # Add a MINT Layer so that the device has something to work with
        cur_device.create_mint_layer("0", "0", 0, MINTLayerType.FLOW)

        cn_component_mapping = generate_device(
            construction_graph=variant,
            scaffhold_device=cur_device,
            name_generator=name_generator,
            mapping_library=library,
        )
        # STEP 8 - Generate the control logic network (valves + Cport on CONTROL layer)
        generate_control_network(
            module=module,
            variant=variant,
            cn_component_mapping=cn_component_mapping,
            scaffhold_device=cur_device,
        )

        generated_devices.append(cur_device)

    return generated_devices


def eliminate_explicit_match_alternates(
    matches: List[LibraryPrimitivesEntry],
    explict_mappings: List[NodeMappingTemplate],
    library: MappingLibrary,
    fig=None,
) -> Tuple[
    List[LibraryPrimitivesEntry],
    List[Set[str]],
    Dict[FrozenSet[str], List[Constraint]],
]:
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
    explicit_constraints_by_cover: Dict[FrozenSet[str], List[Constraint]] = {}

    alias_map = {}
    if fig is not None:
        alias_map = getattr(fig, "_removed_to_surviving", {}) or {}

    # Go through each of the explict matches, generate a subgraph and compare against
    # all the matches
    for explicit_mapping in explict_mappings:
        # Generate a subgraph for each of the mapping instance fig
        for instance in explicit_mapping.instances:
            node_set = set()

            # Check what kind of an instance this is (most specific first:
            # NetworkMapping is a NodeMappingInstance but uses input/output lists,
            # not the single .node field).
            if isinstance(instance, NetworkMapping):
                node_set = {n.ID for n in instance.input_nodes} | {
                    n.ID for n in instance.output_nodes
                }
            elif isinstance(instance, FluidicOperatorMapping):
                node_set.add(instance.node.ID)
            elif isinstance(instance, StorageMapping):
                node_set.add(instance.node.ID)
            elif isinstance(instance, PumpMapping):
                node_set.add(instance.node.ID)
            elif isinstance(instance, NodeMappingInstance):
                node_set.add(instance.node.ID)

            if not node_set:
                continue

            normalized_node_set = {alias_map.get(node_id, node_id) for node_id in node_set}
            cover_key = frozenset(normalized_node_set)
            if explicit_mapping.constraints:
                explicit_constraints_by_cover.setdefault(cover_key, []).extend(
                    [copy.deepcopy(c) for c in explicit_mapping.constraints]
                )

            # #MATERIAL-style mappings intentionally carry no technology override:
            # they only contribute constraints/metadata to matched construction nodes.
            if explicit_mapping.technology_string is None:
                continue

            if cover_key in match_node_set_dict:
                # This is an explicit match
                # Remove the explicit match from the list of matches
                print(
                    "Eliminating match: {}".format(
                        match_node_set_dict[cover_key]
                    )
                )
                match_node_set_dict[cover_key].clear()

            # Now generate a match tuple for this instance
            match_primitive_uid: Optional[str] = None
            match_technology_string = explicit_mapping.technology_string
            match_mapping: Dict[str, str] = {}

            # TODO - Retouch this part if we ever go into modifying how the matches are
            # generated if we use the match string coordinates (use the match interface
            # for this) (function - generate_single_match)

            if isinstance(instance, NetworkMapping):
                for i, node in enumerate(instance.input_nodes):
                    match_mapping[alias_map.get(node.ID, node.ID)] = f"vi{i}"
                for i, node in enumerate(instance.output_nodes):
                    match_mapping[alias_map.get(node.ID, node.ID)] = f"vo{i}"
            elif isinstance(instance, FluidicOperatorMapping):
                node_id = alias_map.get(instance.node.ID, instance.node.ID)
                match_mapping[node_id] = "v1"
            elif isinstance(instance, StorageMapping):
                node_id = alias_map.get(instance.node.ID, instance.node.ID)
                match_mapping[node_id] = "v1"
            elif isinstance(instance, PumpMapping):
                node_id = alias_map.get(instance.node.ID, instance.node.ID)
                match_mapping[node_id] = "v1"
            elif isinstance(instance, NodeMappingInstance):
                node_id = alias_map.get(instance.node.ID, instance.node.ID)
                match_mapping[node_id] = "v1"

            # Rewrite the matchid for the explicit matches
            # based on the library entry
            if cover_key in match_node_set_dict:
                # Find the primitive that matches the technology string
                for primitive in match_node_set_dict[cover_key]:
                    if primitive[1] == explicit_mapping.technology_string:
                        # This is the match we want to replace
                        # Replace the match id with the match tuple
                        match_primitive_uid = primitive[0]
                # This is an explicit match
                # Remove the explicit match from the list of matches
                print(
                    "Eliminating match: {}".format(
                        match_node_set_dict[cover_key]
                    )
                )
                match_node_set_dict[cover_key].clear()

            # If the match_primitive ID is None, we need to query a match from the
            # library
            if match_primitive_uid is None:
                primitives_with_technology = library.get_primitives(
                    match_technology_string
                )
                if (len(primitives_with_technology) > 0):
                    procedural = [
                        p
                        for p in primitives_with_technology
                        if isinstance(p, ProceduralPrimitive)
                    ]
                    match_primitive_uid = (
                        procedural or primitives_with_technology
                    )[0].uid
                else:
                    primitives_with_technology = library.get_primitives(
                        "REACTION CHAMBER"
                    )
                    match_primitive_uid = primitives_with_technology[0].uid

            # Add this match tuple to the list of matches
            match_tuple: LibraryPrimitivesEntry = (
                match_primitive_uid,
                match_technology_string,
                match_mapping,
            )

            explicit_matches.append(match_tuple)
            # This is something we need to return to the to the caller
            explicit_cover_sets.append(set(normalized_node_set))

    # Modify the matches list
    eliminated_matches = []
    for match_tuple_list in match_node_set_dict.values():
        for match_tuple in match_tuple_list:
            eliminated_matches.append(match_tuple)

    # Add the explicit matches to the list of matches
    eliminated_matches.extend(explicit_matches)

    return (eliminated_matches, explicit_cover_sets, explicit_constraints_by_cover)

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
