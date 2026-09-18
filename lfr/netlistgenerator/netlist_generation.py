import math
from typing import Dict, List, Optional, Set, Tuple

import networkx as nx
from parchmint import Component, Params, Target
from parchmint.connection import Connection
from pymint.mintdevice import MINTDevice

from lfr import parameters as lfr_parameters
from lfr.netlistgenerator.connectingoption import ConnectingOption
from lfr.netlistgenerator.constructiongraph.constructiongraph import ConstructionGraph
from lfr.netlistgenerator.mappinglibrary import MappingLibrary
from lfr.netlistgenerator.namegenerator import NameGenerator
from lfr.netlistgenerator.primitive import PrimitiveType, ProceduralPrimitive
from lfr.postprocessor.constraints import DiyTerminalConstraint, MaterialConstraint


def generate_device(
    construction_graph: ConstructionGraph,
    scaffhold_device: MINTDevice,
    name_generator: NameGenerator,
    mapping_library: MappingLibrary,
) -> Dict[str, List[str]]:
    # TODO - Generate the device
    # Step 1 - go though each of the construction nodes and genrate the corresponding
    # components
    # Step 2 - generate the connections between the outputs to input on the connected
    # construction nodes
    # Step 3 - TODO - Generate the control network

    cn_component_mapping: Dict[str, List[str]] = {}

    node_ids = nx.dfs_preorder_nodes(construction_graph)
    print("Nodes to Traverse:", node_ids)

    # Go through the ordered nodes and start creating the components
    for node_id in node_ids:
        cn = construction_graph.get_construction_node(node_id)

        # raise and error if the construction node has no primitive
        if cn.primitive is None:
            raise ValueError(f"Construction Node: {node_id} has no primitive")

        # Generate the netlist based on the primitive type
        if cn.primitive.type is PrimitiveType.COMPONENT:
            # Generate the component
            component = cn.primitive.get_default_component(
                name_generator, scaffhold_device.device.layers[0]
            )

            # Add to the scaffhold device
            scaffhold_device.device.add_component(component)
            _apply_constraints_to_components(cn.constraints, [component])

            # Add to the component mapping
            cn_component_mapping[node_id] = [component.ID]

        elif cn.primitive.type is PrimitiveType.NETLIST:
            # Explicit 4-port nozzle (oil_left/oil_right/aqueous/droplets): emit
            # the primitive only. The default dropletgenerator.mint netlist would
            # add extra synthesized oil PORTs that duplicate the parent finputs.
            if _diy_constraint(cn) is not None:
                name = name_generator.generate_name(cn.primitive.mint)
                layer = scaffhold_device.device.layers[0]
                component = Component(
                    name=name,
                    ID=name,
                    entity=cn.primitive.mint,
                    params=Params({}),
                    layers=[layer],
                )
                scaffhold_device.device.add_component(component)
                _apply_constraints_to_components(cn.constraints, [component])
                cn_component_mapping[node_id] = [component.ID]
                continue
            netlist = cn.primitive.get_default_netlist(cn.ID, name_generator)
            _apply_constraints_to_components(cn.constraints, list(netlist.components))

            # Merge the netlist into the scaffhold device
            scaffhold_device.device.merge_netlist(netlist)

            # Add to the component mapping
            cn_component_mapping[node_id] = [
                component.ID for component in netlist.components
            ]

        elif cn.primitive.type is PrimitiveType.PROCEDURAL:
            layer = scaffhold_device.device.layers[0]
            proc = cn.primitive
            if not isinstance(proc, ProceduralPrimitive):
                raise TypeError(
                    f"Expected ProceduralPrimitive for {node_id}, got {type(proc)}"
                )
            component = proc.get_procedural_component(
                name_generator, layer, cn.fig_subgraph
            )
            _apply_constraints_to_components(cn.constraints, [component])
            scaffhold_device.device.add_component(component)
            cn_component_mapping[node_id] = [component.ID]

    # Go through the edges and connect the components using the inputs and outputs of
    # the primitives
    for source_cn_id, target_cn_id in construction_graph.edges:

        source_cn = construction_graph.get_construction_node(source_cn_id)
        target_cn = construction_graph.get_construction_node(target_cn_id)

        fig = getattr(construction_graph, "_fig", None)

        # DIYcomponent: pick side terminals from DiyTerminalConstraint when present
        source_option = _diy_connecting_option(
            source_cn, target_cn, as_input=False
        )
        target_option = _diy_connecting_option(
            target_cn, source_cn, as_input=True
        )
        if source_option is None:
            source_option = _chamber_connecting_option(source_cn, as_input=False)
        if target_option is None:
            target_option = _chamber_connecting_option(target_cn, as_input=True)
        if source_option is None:
            source_option = _pick_connecting_option(
                source_cn, target_cn, as_input=False, fig=fig
            )
        if target_option is None:
            target_option = _pick_connecting_option(
                target_cn, source_cn, as_input=True, fig=fig
            )
        if source_option is None or target_option is None:
            print(
                f"Warning: no connecting option for {source_cn_id} -> {target_cn_id}"
            )
            continue

        #Source option exists here
        #print(source_option.component_port)

        # Generate the target from the source option
        source_targets = get_targets(
            source_option, source_cn_id, name_generator, cn_component_mapping
        )

        target_targets = get_targets(
            target_option, target_cn_id, name_generator, cn_component_mapping
        )

        #print(source_targets)
        #print(target_targets)
        # If there is 1 source and 1 target, then connect the components
        if len(source_targets) == 1 and len(target_targets) == 1:
            create_device_connection(
                source_targets.pop(),
                target_targets.pop(),
                name_generator,
                scaffhold_device,
                mapping_library,
            )

        elif len(source_targets) == len(target_targets):
            raise NotImplementedError("Bus targets not implemented")
        elif len(source_targets) == 1 and len(target_targets) > 1:
            raise NotImplementedError("Multiple targets not implemented")
        elif len(source_targets) > 1 and len(target_targets) == 1:
            raise NotImplementedError("Multiple sources not implemented")

    return cn_component_mapping


def _cn_fig_ids(cn) -> Set[str]:
    try:
        return {_fig_id_from_node(n) for n in cn.fig_subgraph.nodes}
    except Exception:
        return set()


def _option_fig_ids(option: ConnectingOption) -> List[str]:
    return [str(n) for n in (getattr(option, "fig_nodes", None) or [])]


def _pick_connecting_option(cn, neighbor_cn, as_input: bool, fig=None):
    """Pick a connecting option for an edge, matching tagged YTREE/TREE/MUX leaves.

    Construction-graph generation used to ``copy().pop()`` the last option on
    every edge, so a 16-leaf YTREE always emitted ``ytree_1 17``. A tagged
    option is consumed only when its FIG node is actually covered by the
    neighbor (the PORT for that leaf). Adjacent mixers must not steal leaves;
    they fall through to trunk port 1.
    """
    options = cn.input_options if as_input else cn.output_options
    mint = str(getattr(getattr(cn, "primitive", None), "mint", "") or "").upper()
    is_tree = mint in {"YTREE", "TREE", "MUX"}
    if not options:
        return ConnectingOption(None, ["1"]) if is_tree else None
    neighbor_ids = _cn_fig_ids(neighbor_cn)
    for i, opt in enumerate(options):
        if any(nid in neighbor_ids for nid in _option_fig_ids(opt)):
            return options.pop(i)
    if is_tree and any(_option_fig_ids(o) for o in options):
        return ConnectingOption(None, ["1"])
    return options[-1]


def _chamber_connecting_option(cn, as_input: bool):
    """REACTION CHAMBER: top (1) in, bottom (3) out — vertical through-chamber."""
    primitive = getattr(cn, "primitive", None)
    mint = getattr(primitive, "mint", None)
    if mint != "REACTION CHAMBER":
        return None
    options = cn.input_options if as_input else cn.output_options
    preferred = "1" if as_input else "3"
    for opt in options:
        if preferred in (opt.component_port or []):
            return opt
    return None


def _diy_constraint(cn) -> Optional[DiyTerminalConstraint]:
    for constraint in getattr(cn, "constraints", []) or []:
        if isinstance(constraint, DiyTerminalConstraint):
            return constraint
    return None


def _diy_connecting_option(diy_cn, neighbor_cn, as_input: bool):
    """Resolve DIY side terminal for an edge via neighbor FIG node IDs."""
    diy = _diy_constraint(diy_cn)
    if diy is None:
        return None
    try:
        neighbor_ids = {_fig_id_from_node(n) for n in neighbor_cn.fig_subgraph.nodes}
    except Exception:
        return None
    mapping = diy.input_map if as_input else diy.output_map
    for fig_id, terminal in mapping.items():
        if fig_id in neighbor_ids:
            return ConnectingOption(None, [terminal])
    return None


# 3DuF / MINT camelCase keys that LFR would otherwise lowercase.
_CANONICAL_PARAM_KEYS = {
    "componentspacing": "componentSpacing",
    "rotation": "rotation",
    "channelwidth": "channelWidth",
    "edgebend": "edgeBend",
    "edgebend1": "edgeBend1",
    "edgebend2": "edgeBend2",
    "bendspacing": "bendSpacing",
    "bendlength": "bendLength",
    "numberofbends": "numberOfBends",
    "minchannellength": "minChannelLength",
}


def _canonical_param_key(key: str) -> str:
    mapped = _CANONICAL_PARAM_KEYS.get(key.lower())
    if mapped:
        return mapped
    return key.lower()


def _apply_constraints_to_components(constraints, components) -> None:
    """Apply LFR directive constraints as component params metadata."""
    if not constraints or not components:
        return

    for component in components:
        params = component.params.data
        for constraint in constraints:
            if isinstance(constraint, DiyTerminalConstraint):
                continue
            if isinstance(constraint, MaterialConstraint):
                material_type = constraint.material_type
                if material_type is not None:
                    params["material"] = material_type
                continue

            key = constraint.key
            if key == "":
                continue
            key_norm = _canonical_param_key(key)
            target = constraint.get_target_value()
            min_value = constraint.get_min_value()
            max_value = constraint.get_max_value()
            unit = constraint.unit

            if target is not None:
                params[key_norm] = target
            if min_value is not None:
                params[f"{key_norm}Min"] = min_value
            if max_value is not None:
                params[f"{key_norm}Max"] = max_value
            if unit is not None:
                params[f"{key_norm}Unit"] = unit


def _fig_id_from_node(n) -> str:
    """Return FIG node ID (string) from a node in fig_subgraph (object or str)."""
    return getattr(n, "ID", str(n))


def generate_control_network(
    module,
    variant: ConstructionGraph,
    cn_component_mapping: Dict[str, List[str]],
    scaffhold_device: MINTDevice,
) -> None:
    """Add CONTROL layer, valves on flow connections, and Cport components from FIG state_tables.

    Control-layer ports are named Cport_0, Cport_1, ... to distinguish from flow layer.
    ``#MAP "MUX" "assign"`` has no state table; Super_MUX-style CONTROL PORTs
    are attached afterwards via ``attach_mux_control_ports``.
    """
    from parchmint.device import ValveType
    from pymint.mintlayer import MINTLayerType

    fig = module.FIG
    if fig.state_tables:
        _generate_state_table_control(
            module,
            variant,
            cn_component_mapping,
            scaffhold_device,
            ValveType,
            MINTLayerType,
        )
    attach_mux_control_ports(scaffhold_device)


def _mux_control_already_wired(device, mux_id: str, first: int, n_ctrl: int) -> bool:
    wanted = {str(first + i) for i in range(n_ctrl)}
    for connection in device.connections:
        layer = getattr(connection, "layer", None)
        layer_type = str(getattr(layer, "layer_type", "") or "").upper()
        layer_id = str(getattr(layer, "ID", "") or "")
        if "CONTROL" not in layer_type and layer_id != "1":
            continue
        ends = []
        if connection.source:
            ends.append(connection.source)
        ends.extend(connection.sinks or [])
        for end in ends:
            if str(end.component) == mux_id and str(end.port) in wanted:
                return True
    return False


def _unique_device_id(existing: Set[str], name: str) -> str:
    if name not in existing:
        return name
    idx = 2
    while f"{name}_{idx}" in existing:
        idx += 1
    return f"{name}_{idx}"


def attach_mux_control_ports(scaffhold_device: MINTDevice) -> None:
    """Wire CONTROL PORTs onto MUX body terminals like handwritten Super_MUX.

    A 1-to-N MUX has ``2 * ceil(log2(N))`` control terminals starting at
    label ``2 + N``. Super_MUX connects them as:
      odd  (1-based) control: PORT side 4 -> mux port
      even (1-based) control: PORT side 2 -> mux port
    """
    from pymint.mintlayer import MINTLayerType

    muxes = [
        component
        for component in scaffhold_device.device.components
        if str(component.entity).upper() == "MUX"
    ]
    if not muxes:
        return

    control_layer_id = "1"
    try:
        scaffhold_device.device.get_layer(control_layer_id)
    except KeyError:
        scaffhold_device.create_mint_layer(
            control_layer_id, "control", 0, MINTLayerType.CONTROL
        )

    existing = {component.ID for component in scaffhold_device.device.components}
    existing_conns = {
        connection.ID for connection in scaffhold_device.device.connections
    }
    prefix_ids = len(muxes) > 1

    for mux in muxes:
        params = mux.params.data
        n_in = int(round(float(params.get("in") or 1)))
        n_out = int(round(float(params.get("out") or 1)))
        leafs = max(n_in, n_out, 1)
        if leafs < 2:
            continue
        n_ctrl = 2 * int(math.ceil(math.log2(leafs)))
        first = 2 + leafs
        if _mux_control_already_wired(scaffhold_device.device, mux.ID, first, n_ctrl):
            continue
        channel_width = float(
            params.get("controlChannelWidth")
            or lfr_parameters.DEFAULT_CONTROL_CHANNEL_WIDTH_UM
        )
        for i in range(n_ctrl):
            base_port = f"cp{i + 1}"
            cport_name = f"{mux.ID}_{base_port}" if prefix_ids else base_port
            cport_name = _unique_device_id(existing, cport_name)
            scaffhold_device.create_mint_component(
                name=cport_name,
                technology="PORT",
                params={
                    "portRadius": 1000,
                    "componentSpacing": lfr_parameters.DEFAULT_COMPONENT_SPACING_UM,
                },
                layer_ids=[control_layer_id],
            )
            existing.add(cport_name)
            mux_port = str(first + i)
            port_side = "4" if (i % 2 == 0) else "2"
            base_channel = f"cc{i + 1}"
            channel_name = f"{mux.ID}_{base_channel}" if prefix_ids else base_channel
            channel_name = _unique_device_id(existing_conns, channel_name)
            src_target = Target(component_id=cport_name, port=port_side)
            sink_target = Target(component_id=mux.ID, port=mux_port)
            scaffhold_device.create_mint_connection(
                name=channel_name,
                technology="CHANNEL",
                params={"channelWidth": channel_width},
                source=src_target,
                sinks=[sink_target],
                layer_id=control_layer_id,
            )
            existing_conns.add(channel_name)

    n_cports = sum(
        1
        for component in scaffhold_device.device.components
        if component.entity == "PORT"
        and (
            str(component.ID).startswith("Cport_")
            or str(component.ID).startswith("cp")
            or "_cp" in str(component.ID)
        )
    )
    if n_cports > 0:
        scaffhold_device.device.params.set_param("controlPortCount", n_cports)


def _generate_state_table_control(
    module,
    variant: ConstructionGraph,
    cn_component_mapping: Dict[str, List[str]],
    scaffhold_device: MINTDevice,
    ValveType,
    MINTLayerType,
) -> None:
    fig = module.FIG

    # Build fig_node_id -> set(device component IDs)
    fig_to_components: Dict[str, set] = {}
    for cn in variant.construction_nodes:
        try:
            sub = cn.fig_subgraph
        except Exception:
            continue
        fig_ids = set(_fig_id_from_node(n) for n in sub.nodes)
        comps = set(cn_component_mapping.get(cn.ID, []))
        for fid in fig_ids:
            fig_to_components.setdefault(fid, set()).update(comps)

    # Collect all control mappings from state tables
    control_entries: List[Tuple[Tuple[str, str], str, str]] = []
    for st in fig.state_tables:
        control_entries.extend(st.get_control_mapping())

    if not control_entries:
        return

    # Resolve FIG node ID to component set (use _removed_to_surviving alias after simplification)
    def resolve_fig_id(fig_id: str) -> Set[str]:
        out = set(fig_to_components.get(fig_id, set()))
        if not out and getattr(fig, "_removed_to_surviving", None):
            aliased = fig._removed_to_surviving.get(fig_id)
            if aliased:
                out = set(fig_to_components.get(aliased, set()))
        return out

    # Ensure CONTROL layer exists (id "1", name "control")
    control_layer_id = "1"
    try:
        scaffhold_device.device.get_layer(control_layer_id)
    except KeyError:
        scaffhold_device.create_mint_layer(
            control_layer_id, "control", 0, MINTLayerType.CONTROL
        )

    # Logical control bit width from distribute state-table headers (e.g. 3-bit mux select).
    # Physical MINT/JSON uses one Cport per gated flow arm (one-hot valves) after tree expansion.
    logical_bits = 0
    seen_headers: Set[str] = set()
    for st in fig.state_tables:
        for h in getattr(st, "headers", []) or []:
            if h not in seen_headers:
                seen_headers.add(h)
                logical_bits += 1

    created_cports = 0
    for idx, ((fig_src, fig_tgt), _st_valve_id, _ctrl_id) in enumerate(control_entries):
        src_comps = resolve_fig_id(fig_src)
        tgt_comps = resolve_fig_id(fig_tgt)
        conn = None
        for c in scaffhold_device.device.connections:
            if c.layer is None or c.layer.ID != "0":
                continue
            src_ok = c.source and c.source.component in src_comps
            snk = c.sinks[0] if c.sinks else None
            tgt_ok = snk and snk.component in tgt_comps
            if src_ok and tgt_ok:
                conn = c
                break
        if conn is None:
            continue

        # Each distribute block names its first valve valve_0. Number globally
        # so two gated edges become valve_0 and valve_1, not one shared valve.
        valve_id = "valve_{}".format(idx)

        # Add control-layer port first (so we can connect Ctrlchannel from it to valve)
        cport_name = "Cport_{}".format(idx)
        if not any(c.ID == cport_name for c in scaffhold_device.device.components):
            scaffhold_device.create_mint_component(
                name=cport_name,
                technology="PORT",
                params={"position": [-1, -1]},
                layer_ids=[control_layer_id],
            )
            created_cports += 1

        # Add valve on this flow connection (on control layer).
        # VALVE3D uses valveRadius (not planar VALVE width/length). Explicit
        # componentSpacing avoids a missing-param fallback being injected
        # for every component when serializing to *_fromLFR.mint / JSON.
        if not any(v.ID == valve_id for v in scaffhold_device.device.valves):
            scaffhold_device.create_valve(
                name=valve_id,
                technology="VALVE3D",
                params={
                    "position": [-1, -1],
                    "controlPort": cport_name,
                    "componentSpacing": lfr_parameters.DEFAULT_COMPONENT_SPACING_UM,
                    "valveRadius": lfr_parameters.DEFAULT_VALVE3D_RADIUS_UM,
                    "gap": lfr_parameters.DEFAULT_VALVE3D_GAP_UM,
                    "width": lfr_parameters.DEFAULT_VALVE3D_WIDTH_UM,
                    "length": lfr_parameters.DEFAULT_VALVE3D_LENGTH_UM,
                    "height": 250,
                },
                layer_ids=[control_layer_id],
                connection=conn,
                valve_type=ValveType.NORMALLY_OPEN,
            )

        scaffhold_device.device.set_valve_control_port(valve_id, cport_name)

        # Control-layer channel from Cport to valve (Ctrlchannel to distinguish from flow CHANNELs)
        ctrl_channel_name = "Ctrlchannel_{}".format(idx)
        if not any(c.ID == ctrl_channel_name for c in scaffhold_device.device.connections):
            src_target = Target(component_id=cport_name, port="1")
            sink_target = Target(component_id=valve_id, port="1")
            scaffhold_device.create_mint_connection(
                name=ctrl_channel_name,
                technology=lfr_parameters.DEFAULT_CONNECTION_ENTITY,
                params={
                    "position": [-1, -1],
                    "crossSection": lfr_parameters.DEFAULT_CONNECTION_CROSS_SECTION,
                    "channelWidth": lfr_parameters.DEFAULT_CONTROL_CHANNEL_WIDTH_UM,
                    "length": lfr_parameters.MIN_CONNECTED_COMPONENT_DISTANCE_UM,
                    "minChannelLength": lfr_parameters.MIN_CONNECTED_COMPONENT_DISTANCE_UM,
                },
                source=src_target,
                sinks=[sink_target],
                layer_id=control_layer_id,
            )

    # Device-detail truth: physical Cport count after mux/distribute expansion.
    # synthesize / compile_lfr consumers should use controlPortCount, not LFR bit width alone.
    n_cports = sum(
        1
        for c in scaffhold_device.device.components
        if c.entity == "PORT" and str(c.ID).startswith("Cport_")
    )
    if n_cports == 0:
        n_cports = created_cports
    scaffhold_device.device.params.set_param("controlPortCount", n_cports)
    if logical_bits > 0:
        scaffhold_device.device.params.set_param("logicalControlBits", logical_bits)
    if logical_bits > 0 and n_cports > logical_bits:
        scaffhold_device.device.params.set_param(
            "controlExpansion", "distribute_one_hot"
        )


def create_device_connection(
    source_target: Target,
    target_target: Target,
    name_generator: NameGenerator,
    scaffhold_device: MINTDevice,
    mapping_library: MappingLibrary,
) -> None:
    # TODO - Create the connection based on parameters from the connecting option
    # Step 1 - Get the connection from the mapping library
    # TODO: Create new method stubs to get the right connection primitives from the
    # mapping library (this would need extra criteria that that will need evaulation
    # in the future (RAMA Extension))
    primitive = mapping_library.get_default_connection_entry()
    # Step 2 - Create the connection in the device.
    # Keep instance names as channel_N even when the entity is ROUNDED CHANNEL.
    connection_name = name_generator.generate_name("CHANNEL")
    connection = Connection(
        name=connection_name,
        ID=connection_name,
        entity=primitive.mint,
        source=source_target,
        sinks=[target_target],
        params=Params(
            {
                "crossSection": lfr_parameters.DEFAULT_CONNECTION_CROSS_SECTION,
                "length": lfr_parameters.MIN_CONNECTED_COMPONENT_DISTANCE_UM,
                "minChannelLength": lfr_parameters.MIN_CONNECTED_COMPONENT_DISTANCE_UM,
            }
        ),
        layer=scaffhold_device.device.layers[
            0
        ],  # TODO - This will be replaced in the future when we introduce layer sharding
    )
    scaffhold_device.device.add_connection(connection)


def get_targets(
    option: ConnectingOption,
    connection_node_id: str,
    name_generator: NameGenerator,
    cn_name_map,
) -> List[Target]:
    ret: List[Target] = []

    if option.component_name is None:
        # TODO: Clarify the logic for doing this later on and put it in the docstring
        component_names = cn_name_map[connection_node_id]
    else:
        # TODO: Clarify the logic for doing this later on and put it in the docstring
        old_name = option.component_name
        component_name = name_generator.get_cn_name(connection_node_id, old_name)
        component_names = [component_name]
    for component_name in component_names:
        for port_name in option.component_port:
            # Check and make sure that the component name is valid
            if component_name is None:
                raise ValueError(
                    "Could not generate connection target for construction node"
                    f" {connection_node_id} since Port name is None"
                )
            target = Target(component_name, port_name)
            ret.append(target)

    return ret
