from lfr.netlistgenerator.primitive import NetworkPrimitive, Primitive, PrimitiveType
from lfr.netlistgenerator.v2.connectingoption import ConnectingOption
from lfr.netlistgenerator.mappinglibrary import MappingLibrary
from lfr.netlistgenerator.v2.networkmappingoption import NetworkMappingOption, NetworkMappingOptionType
from lfr.netlistgenerator.v2.gen_strategies.genstrategy import GenStrategy
from lfr.fig.fignode import Flow, IOType, ValueNode
from typing import List
from pymint.mintdevice import MINTDevice
from lfr.netlistgenerator.namegenerator import NameGenerator
from lfr.netlistgenerator.v2.gen_strategies.dummy import DummyStrategy
from lfr.netlistgenerator.v2.constructionnode import ConstructionNode
from lfr.netlistgenerator.v2.constructiongraph import ConstructionGraph
from lfr.fig.interaction import FluidIntegerInteraction, FluidNumberInteraction, InteractionType
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

    library = MappingLibrary("dropX")

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
        None
    )

    library.add_io_entry(port)

    # PICO INJECTOR

    pico_injector_inputs = []

    pico_injector_inputs.append(ConnectingOption(None, [1]))
    pico_injector_inputs.append(ConnectingOption(None, [2]))

    pico_injector_outputs = []

    pico_injector_outputs.append(ConnectingOption(None, [3]))

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

    electrophoresis_merger_inputs.append(ConnectingOption(None, [1]))
    electrophoresis_merger_inputs.append(ConnectingOption(None, [2]))

    electrophoresis_merger_outputs = []

    electrophoresis_merger_outputs.append(ConnectingOption(None, [3]))

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

    droplet_generator_inputs.append(ConnectingOption("default_component", [1]))

    droplet_generator_outputs = []

    droplet_generator_outputs.append(ConnectingOption("default_component", [3]))

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
        ]
    )

    library.add_operator_entry(droplet_generator, InteractionType.METER)

    droplet_merger_junction_inputs = []

    droplet_merger_junction_inputs.append(ConnectingOption(None, [1]))
    droplet_merger_junction_inputs.append(ConnectingOption(None, [2]))

    droplet_merger_junction_outputs = []

    droplet_merger_junction_outputs.append(ConnectingOption(None, [3]))

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

    droplet_merger_channel_inputs.append(ConnectingOption(None, [1]))

    droplet_merger_channel_outputs = []

    droplet_merger_channel_outputs.append(ConnectingOption(None, [2]))

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

    # DROPLET SPLITTER

    droplet_splitter_inputs = []

    droplet_splitter_inputs.append(ConnectingOption(None, [1]))

    droplet_splitter_outputs = []

    droplet_splitter_outputs.append(ConnectingOption(None, [2]))
    droplet_splitter_outputs.append(ConnectingOption(None, [3]))

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

    droplet_capacitance_sensor_inputs.append(ConnectingOption(None, [1]))

    droplet_capacitance_sensor_outputs = []

    droplet_capacitance_sensor_outputs.append(ConnectingOption(None, [2]))

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

    library.add_operator_entry(droplet_capacitance_sensor, InteractionType.TECHNOLOGY_PROCESS)

    # DROPLET FLUORESCENCE SENSOR

    droplet_fluorescence_sensor_inputs = []

    droplet_fluorescence_sensor_inputs.append(ConnectingOption(None, [1]))

    droplet_fluorescence_sensor_outputs = []

    droplet_fluorescence_sensor_outputs.append(ConnectingOption(None, [2]))

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

    library.add_operator_entry(droplet_fluorescence_sensor, InteractionType.TECHNOLOGY_PROCESS)

    # DROPLET LUMINESCENCE SENSOR
    droplet_luminescence_sensor_inputs = []

    droplet_luminescence_sensor_inputs.append(ConnectingOption(None, [1]))

    droplet_luminescence_sensor_outputs = []

    droplet_luminescence_sensor_outputs.append(ConnectingOption(None, [2]))

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

    library.add_operator_entry(droplet_luminescence_sensor, InteractionType.TECHNOLOGY_PROCESS)

    # DROPLET SPACER

    droplet_spacer_inputs = []

    droplet_spacer_inputs.append(ConnectingOption("default_component", [1]))

    droplet_spacer_outputs = []

    droplet_spacer_outputs.append(ConnectingOption("default_component", [2]))

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

    return library


def generate(module: Module, library: MappingLibrary) -> MINTDevice:

    construction_graph = ConstructionGraph()

    name_generator = NameGenerator()

    cur_device = MINTDevice(module.name)

    dummy_strategy = DummyStrategy(construction_graph)

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
            if isinstance(interaction, FluidNumberInteraction) or isinstance(interaction, FluidIntegerInteraction):
                # Basically add the value node id into the subgraph view also
                node_ids = [module.FIG.get_fignode(edge[0]).id for edge in module.FIG.in_edges(interaction.id) if isinstance(module.FIG.get_fignode(edge[0]), ValueNode)]
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
    cn_nodes = get_flow_flow_candidates(module, dummy_strategy)
    for cn in cn_nodes:
        construction_graph.add_construction_node(cn)

    # Apply all the explicit mappings in the module to the nodes, overwriting
    # the options from the library to match against
    # TODO - Modify Explicit Mapping Data structure

    # Find all the explicit mappings and override them in the construction graph
    mappings = module.get_explicit_mappings()
    construction_graph.override_mappings(mappings)

    # Whittle Down the mapping options here to only include the requried single candidates
    # TODO - Check what library is being used and use the required library here
    dummy_strategy.reduce_mapping_options()

    # TODO - Consider what needs to get done for a combinatorial design space
    # ----------------
    # Generate edges in the construction graph, these edges will guide the generation/
    # reduction of path and pipelineing that needs to get done for mars devices
    construction_graph.generate_edges(module.FIG)

    # Now since all the mapping options are finalized Extract the netlist necessary
    construction_graph.construct_components(name_generator, cur_device)

    construction_graph.construct_connections(name_generator, cur_device)

    # Finally join all the netlist pieces attached to the construction nodes
    # and the input/output/load/carrier flows
    # MINIMIZE - carrier / load flows - this might require us to generate
    # multiple netlist options and pick the best
    construction_graph.generate_flow_cn_edges(module)

    construction_graph.generate_control_cn_edges(module)

    # Generate all the unaccounted carriers and waste output lines necessary
    # for this to function
    connect_orphan_IO()

    return cur_device


def connect_orphan_IO():
    print("Implement the orphan io generation system")


def get_flow_flow_candidates(module: Module, gen_strategy: GenStrategy) -> List[ConstructionNode]:
    # TODO - go through all the edges and see which ones are between flow-flow graphs
    # If these connectsions are between flow-flow nodes then we need to figure out
    # which ones are part of the same network/connected graphs with only flow nodes
    # The networks with only the flow nodes will need to be covered as a part of.
    # these construction nodes.

    ret = []

    # TODO-
    # Step 1. Do a shallow copy of the graph
    # Step 2. Remove all the fignodes that are not Flow
    # Step 3. Now get the all the disconnected pieces of the graph
    # Step 4. Create a Construction node for each of the disconnected pieces
    # Return all the constructions nodes

    # Step 1. Do a shallow copy of the graph
    fig_original = module.FIG
    fig_copy = module.FIG.copy()  # Note this does not copy anything besides the nx.DiGraph at the moment

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
        assert(len(sub.nodes) == 1)
        mapping_type = NetworkMappingOptionType.PASS_THROUGH
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
