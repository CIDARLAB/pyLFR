from lfr.netlistgenerator.v2.procedural_component_algorithms.ytree import YTREE
from lfr.netlistgenerator.v2.gen_strategies.dropxstrategy import DropXStrategy
from lfr.fig.fluidinteractiongraph import FluidInteractionGraph
from lfr.postprocessor.mapping import NetworkMapping, NodeMappingTemplate
from pymint.mintlayer import MINTLayerType
from lfr.netlistgenerator.primitive import NetworkPrimitive, Primitive, PrimitiveType
from lfr.netlistgenerator.v2.connectingoption import ConnectingOption
from lfr.netlistgenerator.mappinglibrary import MappingLibrary
from lfr.netlistgenerator.v2.networkmappingoption import (
    NetworkMappingOption,
    NetworkMappingOptionType,
)
from lfr.netlistgenerator.v2.gen_strategies.genstrategy import GenStrategy
from lfr.fig.fignode import IOType, ValueNode
from typing import List
from pymint.mintdevice import MINTDevice
from lfr.netlistgenerator.namegenerator import NameGenerator
from lfr.netlistgenerator.v2.gen_strategies.dummy import DummyStrategy
from lfr.netlistgenerator.v2.constructionnode import ConstructionNode
from lfr.netlistgenerator.v2.constructiongraph import ConstructionGraph
from lfr.fig.interaction import (
    FluidIntegerInteraction,
    FluidNumberInteraction,
    InteractionType,
)
from lfr.netlistgenerator.v2.mappingoption import MappingOption
from lfr.compiler.module import Module
import networkx as nx


# def generate_MARS_library() -> MappingLibrary:
#     # TODO - Programatically create each of the items necessary for the MARS primitive library,
#     # we shall serialize them after experimentation

#     # mix_primitive = MappingOption()


#     # mix_primitive.init_single_component(mint_component)

#     # mix_primitive.add
#     pass


def generate_dropx_library() -> MappingLibrary:

    library = MappingLibrary("dropx")

    # PORT
    port_inputs = []
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))
    port_inputs.append(ConnectingOption(None, [None]))

    port_outputs = []
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))
    port_outputs.append(ConnectingOption(None, []))

    port = Primitive(
        "PORT",
        PrimitiveType.COMPONENT,
        "IO",
        False,
        False,
        port_inputs,
        port_outputs,
        None,
        None,
        None,
        None,
        None,
    )

    library.add_io_entry(port)

    # PICO INJECTOR

    pico_injector_inputs = []

    pico_injector_inputs.append(ConnectingOption(None, ["1"]))
    pico_injector_inputs.append(ConnectingOption(None, ["2"]))

    pico_injector_outputs = []

    pico_injector_outputs.append(ConnectingOption(None, ["3"]))

    pico_injector_loadings = []
    pico_injector_carriers = []

    pico_injector = Primitive(
        "PICO INJECTOR",
        PrimitiveType.COMPONENT,
        "MIX",
        False,
        False,
        pico_injector_inputs,
        pico_injector_outputs,
        pico_injector_loadings,
        pico_injector_carriers,
        None,
    )

    library.add_operator_entry(pico_injector, InteractionType.MIX)

    # DROPLET ELECTROPHORESIS MERGER

    electrophoresis_merger_inputs = []

    electrophoresis_merger_inputs.append(ConnectingOption(None, ["1"]))
    electrophoresis_merger_inputs.append(ConnectingOption(None, ["2"]))

    electrophoresis_merger_outputs = []

    electrophoresis_merger_outputs.append(ConnectingOption(None, ["3"]))

    electrophoresis_merger_loadings = []
    electrophoresis_merger_carriers = []

    electrophoresis_merger = Primitive(
        "DROPLET ELECTROPHORESIS MERGER",
        PrimitiveType.COMPONENT,
        "MIX",
        False,
        False,
        electrophoresis_merger_inputs,
        electrophoresis_merger_outputs,
        electrophoresis_merger_loadings,
        electrophoresis_merger_carriers,
        None,
    )

    library.add_operator_entry(electrophoresis_merger, InteractionType.MIX)

    # DROPLET GENERATOR

    droplet_generator_inputs = []

    droplet_generator_inputs.append(ConnectingOption("default_component", ["1"]))

    droplet_generator_outputs = []

    droplet_generator_outputs.append(ConnectingOption("default_component", ["3"]))

    droplet_generator_loadings = []
    droplet_generator_carriers = []

    droplet_generator = Primitive(
        "NOZZLE DROPLET GENERATOR",
        PrimitiveType.NETLIST,
        "METER",
        False,
        False,
        droplet_generator_inputs,
        droplet_generator_outputs,
        droplet_generator_loadings,
        droplet_generator_carriers,
        "default-netlists/dropletgenerator.mint",
        ["droplet_size", "generation_rate"],
        [
            "orifice_size",
            "aspect_ratio",
            "capillary_number",
            "expansion_ratio",
            "flow_rate_ratio",
            "normalized_oil_inlet",
            "normalized_orifice_length",
            "normalized_water_inlet",
        ],
    )

    library.add_operator_entry(droplet_generator, InteractionType.METER)

    droplet_merger_junction_inputs = []

    droplet_merger_junction_inputs.append(ConnectingOption(None, ["1"]))
    droplet_merger_junction_inputs.append(ConnectingOption(None, ["2"]))

    droplet_merger_junction_outputs = []

    droplet_merger_junction_outputs.append(ConnectingOption(None, ["3"]))

    droplet_merger_junction_loadings = []
    droplet_merger_junction_carriers = []

    droplet_merger_junction = Primitive(
        "DROPLET MERGER JUNCTION",
        PrimitiveType.COMPONENT,
        "MIX",
        False,
        False,
        droplet_merger_junction_inputs,
        droplet_merger_junction_outputs,
        droplet_merger_junction_loadings,
        droplet_merger_junction_carriers,
        None,
    )

    library.add_operator_entry(droplet_merger_junction, InteractionType.MIX)

    # DROPLET MERGER CHANNEL

    droplet_merger_channel_inputs = []

    droplet_merger_channel_inputs.append(ConnectingOption(None, ["1"]))

    droplet_merger_channel_outputs = []

    droplet_merger_channel_outputs.append(ConnectingOption(None, ["2"]))

    droplet_merger_channel_loadings = []
    droplet_merger_channel_carriers = []

    droplet_merger_channel = Primitive(
        "DROPLET MERGER CHANNEL",
        PrimitiveType.COMPONENT,
        "MIX",
        False,
        False,
        droplet_merger_channel_inputs,
        droplet_merger_channel_outputs,
        droplet_merger_channel_loadings,
        droplet_merger_channel_carriers,
        None,
    )

    library.add_operator_entry(droplet_merger_channel, InteractionType.MIX)

    # MIXER - CONTINOUS FLOW ONE

    cf_mixer_inputs = []

    cf_mixer_inputs.append(ConnectingOption(None, ["1"]))
    cf_mixer_inputs.append(ConnectingOption(None, ["1"]))
    cf_mixer_inputs.append(ConnectingOption(None, ["1"]))
    cf_mixer_inputs.append(ConnectingOption(None, ["1"]))
    cf_mixer_inputs.append(ConnectingOption(None, ["1"]))
    cf_mixer_inputs.append(ConnectingOption(None, ["1"]))
    cf_mixer_inputs.append(ConnectingOption(None, ["1"]))
    cf_mixer_inputs.append(ConnectingOption(None, ["1"]))
    cf_mixer_inputs.append(ConnectingOption(None, ["1"]))
    cf_mixer_inputs.append(ConnectingOption(None, ["1"]))

    cf_mixer_outputs = []

    cf_mixer_outputs.append(ConnectingOption(None, ["2"]))

    cf_mixer_loadings = []
    cf_mixer_carriers = []

    cf_mixer = Primitive(
        "MIXER",
        PrimitiveType.COMPONENT,
        "MIX",
        False,
        False,
        cf_mixer_inputs,
        cf_mixer_outputs,
        cf_mixer_loadings,
        cf_mixer_carriers,
        None,
    )

    library.add_operator_entry(cf_mixer, InteractionType.MIX)

    # DROPLET SPLITTER

    droplet_splitter_inputs = []

    droplet_splitter_inputs.append(ConnectingOption(None, ["1"]))

    droplet_splitter_outputs = []

    droplet_splitter_outputs.append(ConnectingOption(None, ["2"]))
    droplet_splitter_outputs.append(ConnectingOption(None, ["3"]))

    droplet_splitter_loadings = []
    droplet_splitter_carriers = []

    droplet_splitter = Primitive(
        "DROPLET SPLITTER",
        PrimitiveType.COMPONENT,
        "DIVIDE",
        False,
        False,
        droplet_splitter_inputs,
        droplet_splitter_outputs,
        droplet_splitter_loadings,
        droplet_splitter_carriers,
        None,
    )

    library.add_operator_entry(droplet_splitter, InteractionType.DIVIDE)

    # DROPLET CAPACITANCE SENSOR

    droplet_capacitance_sensor_inputs = []

    droplet_capacitance_sensor_inputs.append(ConnectingOption(None, ["1"]))

    droplet_capacitance_sensor_outputs = []

    droplet_capacitance_sensor_outputs.append(ConnectingOption(None, ["2"]))

    droplet_capacitance_sensor_loadings = []
    droplet_capacitance_sensor_carriers = []

    droplet_capacitance_sensor = Primitive(
        "DROPLET CAPACITANCE SENSOR",
        PrimitiveType.COMPONENT,
        "PROCESS",
        False,
        False,
        droplet_capacitance_sensor_inputs,
        droplet_capacitance_sensor_outputs,
        droplet_capacitance_sensor_loadings,
        droplet_capacitance_sensor_carriers,
        None,
    )

    library.add_operator_entry(
        droplet_capacitance_sensor, InteractionType.TECHNOLOGY_PROCESS
    )

    # DROPLET FLUORESCENCE SENSOR

    droplet_fluorescence_sensor_inputs = []

    droplet_fluorescence_sensor_inputs.append(ConnectingOption(None, ["1"]))

    droplet_fluorescence_sensor_outputs = []

    droplet_fluorescence_sensor_outputs.append(ConnectingOption(None, ["2"]))

    droplet_fluorescence_sensor_loadings = []
    droplet_fluorescence_sensor_carriers = []

    droplet_fluorescence_sensor = Primitive(
        "DROPLET FLUORESCENCE SENSOR",
        PrimitiveType.COMPONENT,
        "PROCESS",
        False,
        False,
        droplet_fluorescence_sensor_inputs,
        droplet_fluorescence_sensor_outputs,
        droplet_fluorescence_sensor_loadings,
        droplet_fluorescence_sensor_carriers,
        None,
    )

    library.add_operator_entry(
        droplet_fluorescence_sensor, InteractionType.TECHNOLOGY_PROCESS
    )

    # DROPLET LUMINESCENCE SENSOR
    droplet_luminescence_sensor_inputs = []

    droplet_luminescence_sensor_inputs.append(ConnectingOption(None, ["1"]))

    droplet_luminescence_sensor_outputs = []

    droplet_luminescence_sensor_outputs.append(ConnectingOption(None, ["2"]))

    droplet_luminescence_sensor_loadings = []
    droplet_luminescence_sensor_carriers = []

    droplet_luminescence_sensor = Primitive(
        "DROPLET CAPACITANCE SENSOR",
        PrimitiveType.COMPONENT,
        "PROCESS",
        False,
        False,
        droplet_luminescence_sensor_inputs,
        droplet_luminescence_sensor_outputs,
        droplet_luminescence_sensor_loadings,
        droplet_luminescence_sensor_carriers,
        None,
    )

    library.add_operator_entry(
        droplet_luminescence_sensor, InteractionType.TECHNOLOGY_PROCESS
    )

    # DROPLET SPACER

    droplet_spacer_inputs = []

    droplet_spacer_inputs.append(ConnectingOption("default_component", ["1"]))

    droplet_spacer_outputs = []

    droplet_spacer_outputs.append(ConnectingOption("default_component", ["2"]))

    droplet_spacer_loadings = []
    droplet_spacer_carriers = []

    droplet_spacer = Primitive(
        "DROPLET SPACER",
        PrimitiveType.NETLIST,
        "PROCESS",
        False,
        False,
        droplet_spacer_inputs,
        droplet_spacer_outputs,
        droplet_spacer_loadings,
        droplet_spacer_carriers,
        "default-netlists/dropletspacer.mint",
    )

    library.add_operator_entry(droplet_spacer, InteractionType.TECHNOLOGY_PROCESS)

    # YTREE - This is a procedural primitives

    ytree = YTREE()

    library.add_procedural_entry(ytree)

    return library


def generate(module: Module, library: MappingLibrary) -> MINTDevice:

    construction_graph = ConstructionGraph()

    name_generator = NameGenerator()

    cur_device = MINTDevice(module.name)

    # Add a MINT Layer so that the device has something to work with
    cur_device.create_mint_layer("0", "0", 0, MINTLayerType.FLOW)

    # TODO - I need to change this DummyStrategy later on
    if library.name == "dropx":
        active_strategy = DropXStrategy(construction_graph, module.FIG)
    elif library.name == "mars":
        raise NotImplementedError()
    elif library.name == "hmlp":
        raise NotImplementedError()
    else:
        active_strategy = DummyStrategy(construction_graph, module.FIG)

    # First go through all the interactions in the design

    # IF interaction is mix/sieve/divide/dilute/meter look at the library
    # to get all the options available and set them up as options for the
    # construction graph to pick and choose from the options.
    #
    # FUTURE WORK
    #
    # Do the regex matching to find the mapping options
    # This means that we might need to have a forest of construction of graphs
    # as there would be alternatives for each type of mapping
    for interaction in module.FIG.get_interactions():
        operator_candidates = library.get_operators(interaction_type=interaction.type)
        cn = ConstructionNode(interaction.id)
        # if isinstance(interaction, ValueNode):
        #     continue

        for operator_candidate in operator_candidates:
            # TODO: This will change in the future when we can match subgraphs correctly
            if isinstance(interaction, FluidNumberInteraction) or isinstance(
                interaction, FluidIntegerInteraction
            ):
                # Basically add the value node id into the subgraph view also
                node_ids = [
                    module.FIG.get_fignode(edge[0]).id
                    for edge in module.FIG.in_edges(interaction.id)
                    if isinstance(module.FIG.get_fignode(edge[0]), ValueNode)
                ]
                node_ids.append(interaction.id)
                sub_graph = module.FIG.subgraph(node_ids)
            else:
                sub_graph = module.FIG.subgraph(interaction.id)
            mapping_option = MappingOption(operator_candidate, sub_graph)
            cn.add_mapping_option(mapping_option)

        construction_graph.add_construction_node(cn)

    # Generate all ports necessary for the Explicitly declared IO
    # -------
    # Generate the flow layer IO. These are typically declared explicitly
    # TODO - Figure out how we should generate the construction nodes for control networks

    for io in module.io:
        if io.type is IOType.CONTROL:
            continue
        cn = ConstructionNode(io.id)
        sub_graph = module.FIG.subgraph(io.id)
        mapping_candidate = library.get_default_IO()
        mapping_option = MappingOption(mapping_candidate, sub_graph)
        cn.add_mapping_option(mapping_option)

        construction_graph.add_construction_node(cn)

    # TODO - Go through the different flow-flow edge networks to generate construction nodes
    # specific to these networks, Conditions:
    # if its a 1-1 flow-flow connection, then create a construction node for the two flow nodes
    # if its a 1-n / n-1 / n-n construction nodes, then create a construction node capturing the whole network

    # TODO - Deal with coverage issues here since we need to figure out what are the flow networks,
    # that we want to match first and then ensure that they're no included on any list
    cn_nodes = get_flow_flow_candidates(module, active_strategy)
    for cn in cn_nodes:
        construction_graph.add_construction_node(cn)

    # Apply all the explicit mappings in the module to the nodes, overwriting
    # the options from the library to match against
    # TODO - Modify Explicit Mapping Data structure

    # Find all the explicit mappings and override them in the construction graph
    mappings = module.get_explicit_mappings()
    override_mappings(mappings, library, module.FIG, construction_graph)

    # Whittle Down the mapping options here to only include the requried single candidates
    # TODO - Check what library is being used and use the required library here
    active_strategy.reduce_mapping_options()

    # TODO - Consider what needs to get done for a combinatorial design space
    # ----------------
    # Generate edges in the construction graph, these edges will guide the generation/
    # reduction of path and pipelineing that needs to get done for mars devices
    construction_graph.generate_edges(module.FIG)

    # TODO - Extract all pass through networks
    eliminate_passthrough_nodes(construction_graph)

    # Now since all the mapping options are finalized Extract the netlist necessary
    construction_graph.construct_components(name_generator, cur_device)

    construction_graph.construct_connections(name_generator, cur_device)

    # Finally join all the netlist pieces attached to the construction nodes
    # and the input/output/load/carrier flows
    # TODO - MINIMIZE - carrier / load flows - this might require us to generate
    # multiple netlist options and pick the best
    construction_graph.generate_flow_cn_edges(module)

    construction_graph.generate_control_cn_edges(module)

    # Generate all the unaccounted carriers and waste output lines necessary
    # for this to function
    connect_orphan_IO()

    # Size the component netlist
    active_strategy.size_netlist(cur_device)

    return cur_device


def override_mappings(
    mappings: List[NodeMappingTemplate],
    mapping_library: MappingLibrary,
    fig: FluidInteractionGraph,
    construction_graph: ConstructionGraph,
) -> None:
    # Go through the entire set of mappings in the FIG and generate / append the mapping options
    # Step 1 - Loop through each of the mappingtemplates
    # Step 2 - Loop through each of the instances in teh mappingtemplate
    # Step 3 - Find the cn associated with each of the fig nodes and override the explicit mapping if mappingtemplate has an associated technology string

    for mapping in mappings:
        for instance in mapping.instances:

            primitive_to_use = None
            if mapping.technology_string is not None:
                # Create a mapping option from the library with the corresponding info
                primitive_to_use = mapping_library.get_primitive(
                    mapping.technology_string
                )

            node_ids = []
            cn = None  # Get the right construction node for doing the stuff
            cn_mapping_options = []

            if isinstance(instance, NetworkMapping):
                node_ids.extend(n.id for n in instance.input_nodes)
                node_ids.extend(n.id for n in instance.output_nodes)
                subgraph = fig.subgraph(node_ids)
                cn = construction_graph.get_subgraph_cn(subgraph)
                mapping_option = NetworkMappingOption(
                    network_primitive=primitive_to_use,
                    mapping_type=NetworkMappingOptionType.COMPONENT_REPLACEMENT,
                    subgraph_view=subgraph,
                )
                cn.use_explicit_mapping(mapping_option)
                cn_mapping_options.append(mapping_option)
                cn_mapping_options.extend(cn.mapping_options)

            else:
                # Find the construction node assicated with the
                # FIG node and then do the followinging:
                # Step 1 - If the mappingtemplate has no technology string assiciated
                # with the mapping, just apply the constraints to the associated mapping
                # options

                # Step 2 - In there is a string assiciated with the mappingtemplate, we
                # eliminate all mapping options that dont have a matching string / generate
                # a mapping option with the corresponding

                # In the case of an Fluid Value interaction put all valuenodes in the subgraph
                node_ids.extend(
                    [
                        fig.get_fignode(edge[0]).id
                        for edge in fig.in_edges(instance.node.id)
                        if isinstance(fig.get_fignode(edge[0]), ValueNode)
                    ]
                )
                node_ids.append(instance.node.id)
                subgraph = fig.subgraph(node_ids)

                # Get the Construction node that has the corresponding subgraph,
                # and then replace the mapping option
                cn = construction_graph.get_subgraph_cn(subgraph)
                if primitive_to_use is not None:
                    mapping_option = MappingOption(primitive_to_use, subgraph)
                    cn.use_explicit_mapping(mapping_option)
                    cn_mapping_options.append(mapping_option)
                else:
                    # Add the constraints to all the mapping options
                    # This is an example where since no explicit mapping
                    # was specified, we only add the performance/material
                    # constraints. This can be ulitized for whittling down
                    # options later if necessary.
                    cn_mapping_options.extend(cn.mapping_options)

            # Now that we know what the mapping options are (either explicit
            # loaded from the library, we can add the performance constraints)
            for mapping_option in cn_mapping_options:
                # Add all the constraints to the mapping_option
                cn.constraints.extend(mapping.constraints)


def eliminate_passthrough_nodes(construction_graph: ConstructionGraph):
    for node_id in list(construction_graph.nodes):
        cn = construction_graph.get_cn(node_id)
        assert len(cn.mapping_options) == 1
        mapping_option = cn.mapping_options[0]
        if isinstance(mapping_option, NetworkMappingOption):
            if mapping_option.mapping_type is NetworkMappingOptionType.PASS_THROUGH:

                # First get all the in and out edges
                in_edges = list(construction_graph.in_edges(node_id))
                out_edges = list(construction_graph.out_edges(node_id))

                # In Points
                in_points = [in_edge[0] for in_edge in in_edges]
                out_points = [out_edge[1] for out_edge in out_edges]

                # Delete the node
                construction_graph.delete_node(node_id)

                # Create edges for the different cases
                # Case 1 - 1->1
                if len(in_points) == 1 and len(out_points) == 1:
                    construction_graph.add_edge(in_points[0], out_points[0])
                # Case 2 - n->1
                # Case 3 - 1->n
                elif (len(in_points) > 1 and len(out_points) == 1) or (
                    len(in_points) == 1 and len(out_points) > 1
                ):
                    for in_point in in_points:
                        for out_point in out_points:
                            construction_graph.add_edge(in_point, out_point)
                else:
                    raise Exception(
                        "Pass through network node elimination not implemented \
                        when n->n edge creation is necessary"
                    )


def connect_orphan_IO():
    print("Implement the orphan io generation system")


def get_flow_flow_candidates(
    module: Module, gen_strategy: GenStrategy
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
    fig_original = module.FIG
    fig_copy = (
        module.FIG.copy()
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
        print("Flow candidate")
        print(component)
        sub = fig_original.subgraph(component)
        # TODO - Decide what the mapping type should be. for now assume that we just a single
        # passthrough type scenario where we don't have to do much work
        is_passthrough = __check_if_passthrough(sub)
        if is_passthrough:
            mapping_type = NetworkMappingOptionType.PASS_THROUGH
        else:
            mapping_type = NetworkMappingOptionType.CHANNEL_NETWORK
        nprimitive = NetworkPrimitive(sub, gen_strategy)
        nprimitive.generate_netlist()
        mapping_option = NetworkMappingOption(nprimitive, mapping_type, sub)
        # Step 4. Create a Construction node for each of the disconnected pieces
        cn = ConstructionNode("flow_network_{}".format(i))
        cn.add_mapping_option(mapping_option)

        i += 1
        ret.append(cn)

    return ret


def size_netlist():
    # Size all the node's netlist components to based on the CONSTRAINTS set
    # by the postprocessor
    # TODO - Modify datastructure in library and other places
    netlist_user_constriants = module.get_user_constriants()

    construction_graph.fix_component_params(netlist_user_constriants)

    # Size all the Meter/Dilute/Divide nodes based on the value nodes
    # TODO - Talk to Ali about this for strategy
    construction_graph.size_components()


def __check_if_passthrough(sub) -> bool:
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
