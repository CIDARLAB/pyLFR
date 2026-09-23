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
            # Always emit the mint entity alone. Default netlists such as
            # dropletgenerator.mint also synthesize oil PORTs/CHANNELs that
            # duplicate parent finputs and make get_targets expand one CN into
            # many components (Multiple sources/targets). DIY / nozzle terminal
            # maps wire the real module PORTs onto this single body.
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

        # Construction-graph edges follow node-list order, which can oppose FIG
        # flow (e.g. later unary MIXER listed before an earlier one). FIG role
        # already picked the in/out terminals; emit the CHANNEL in FIG order.
        source_role = _fig_flow_role(source_cn, target_cn, fig)
        if source_role == "input":
            from_option, from_cn_id = target_option, target_cn_id
            to_option, to_cn_id = source_option, source_cn_id
            from_cn, to_cn = target_cn, source_cn
        else:
            from_option, from_cn_id = source_option, source_cn_id
            to_option, to_cn_id = target_option, target_cn_id
            from_cn, to_cn = source_cn, target_cn

        source_targets = get_targets(
            from_option, from_cn_id, name_generator, cn_component_mapping
        )
        target_targets = get_targets(
            to_option, to_cn_id, name_generator, cn_component_mapping
        )

        if len(source_targets) == 1 and len(target_targets) == 1:
            create_device_connection(
                source_targets.pop(),
                target_targets.pop(),
                name_generator,
                scaffhold_device,
                mapping_library,
                connection_constraints=_flow_connection_constraints_for_edge(
                    from_cn, to_cn
                ),
            )

        elif len(source_targets) == len(target_targets):
            raise NotImplementedError("Bus targets not implemented")
        elif len(source_targets) == 1 and len(target_targets) > 1:
            raise NotImplementedError("Multiple targets not implemented")
        elif len(source_targets) > 1 and len(target_targets) == 1:
            raise NotImplementedError("Multiple sources not implemented")

    _strip_channel_type_keys_from_components(scaffhold_device.device)
    return cn_component_mapping


def _cn_fig_ids(cn) -> Set[str]:
    ids: Set[str] = set()
    try:
        ids |= {_fig_id_from_node(n) for n in cn.fig_subgraph.nodes}
    except Exception:
        pass
    declared = getattr(cn, "_declared_fig_ids", None) or getattr(cn, "fig_cover", None)
    if declared:
        try:
            ids |= {_fig_id_from_node(n) for n in declared}
        except Exception:
            pass
    return ids


def _option_fig_ids(option: ConnectingOption) -> List[str]:
    return [str(n) for n in (getattr(option, "fig_nodes", None) or [])]


def _fig_has_edge(fig, source_id: str, target_id: str) -> bool:
    if fig is None:
        return False
    try:
        return bool(fig.has_edge(source_id, target_id))
    except Exception:
        return False


def _fig_successors(fig, node_id: str) -> List[str]:
    if fig is None:
        return []
    try:
        return [str(n) for n in fig.successors(node_id)]
    except Exception:
        return []


def _fig_reaches_through_uncovered(
    fig,
    start_ids: Set[str],
    goal_ids: Set[str],
    blocked: Set[str],
) -> bool:
    """True when start can reach goal walking only through uncovered FIG nodes."""
    if not start_ids or not goal_ids or fig is None:
        return False
    seen = set(start_ids)
    queue = list(start_ids)
    while queue:
        node_id = queue.pop(0)
        for nxt in _fig_successors(fig, node_id):
            if nxt in goal_ids:
                return True
            if nxt in seen or nxt in blocked:
                continue
            seen.add(nxt)
            queue.append(nxt)
    return False


def _fig_flow_role(cn, neighbor_cn, fig) -> Optional[str]:
    """Return ``input`` / ``output`` from FIG, ignoring construction-edge direction.

    Construction-graph edges are added in node-list order, so a PUMP/MIXER can
    end up as the source of both PORT edges. FIG still has ``in → device → out``;
    use that to put inlets on terminal 1 and outlets on terminal 2.
    """
    if fig is None:
        return None
    cn_ids = _cn_fig_ids(cn)
    nb_ids = _cn_fig_ids(neighbor_cn)
    if not cn_ids or not nb_ids:
        return None
    feeds_cn = any(
        _fig_has_edge(fig, b, a) for a in cn_ids for b in nb_ids
    )
    fed_by_cn = any(
        _fig_has_edge(fig, a, b) for a in cn_ids for b in nb_ids
    )
    if feeds_cn and not fed_by_cn:
        return "input"
    if fed_by_cn and not feeds_cn:
        return "output"
    # Intermediate FLOW nets (stage1 between two MIXERs) are uncovered.
    # Walk only outside the two covers so we do not tunnel through another CN.
    other = set(cn_ids)
    if _fig_reaches_through_uncovered(fig, nb_ids, cn_ids, other):
        return "input"
    other = set(nb_ids)
    if _fig_reaches_through_uncovered(fig, cn_ids, nb_ids, other):
        return "output"
    if feeds_cn:
        return "input"
    if fed_by_cn:
        return "output"
    return None


def _pick_connecting_option(cn, neighbor_cn, as_input: bool, fig=None):
    """Pick a connecting option for an edge, matching tagged YTREE/TREE/MUX leaves.

    Construction-graph generation used to ``copy().pop()`` the last option on
    every edge, so a 16-leaf YTREE always emitted ``ytree_1 17``. A tagged
    option is consumed only when its FIG node is actually covered by the
    neighbor (the PORT for that leaf). Adjacent mixers must not steal leaves;
    they fall through to trunk port 1.

    Through-flow primitives (MIXER, PUMP, …) ignore construction-edge direction
    and use FIG in→out so both PORTs do not collapse onto the outlet terminal.
    """
    mint = str(getattr(getattr(cn, "primitive", None), "mint", "") or "").upper()
    is_tree = mint in {"YTREE", "TREE", "MUX"}
    if not is_tree:
        role = _fig_flow_role(cn, neighbor_cn, fig)
        if role == "input":
            as_input = True
        elif role == "output":
            as_input = False
    primary = cn.input_options if as_input else cn.output_options
    secondary = cn.output_options if as_input else cn.input_options
    neighbor_ids = _cn_fig_ids(neighbor_cn)
    for pool in (primary, secondary) if is_tree else (primary,):
        if not pool:
            continue
        for i, opt in enumerate(pool):
            if any(nid in neighbor_ids for nid in _option_fig_ids(opt)):
                return pool.pop(i)
    if is_tree:
        # Trunk / extra sink on the uncovered mid net, not a tagged leaf.
        return ConnectingOption(None, ["1"])
    if not primary:
        return None
    # Return a copy so multi-inlet MIXER edges can reuse terminal "1".
    ports = list(getattr(primary[-1], "component_port", None) or [])
    return ConnectingOption(None, ports)


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
    """Resolve DIY / nozzle terminal for an edge via neighbor FIG node IDs.

    Construction-graph edge direction is not FIG in/out: a 4-to-1 inlet
    PORT and a droplet oil PORT may sit on the source side of the edge.
    Search the requested map first, then the other map.
    """
    diy = _diy_constraint(diy_cn)
    if diy is None:
        return None
    neighbor_ids = _cn_fig_ids(neighbor_cn)
    try:
        neighbor_ids |= {_fig_id_from_node(n) for n in neighbor_cn.fig_subgraph.nodes}
    except Exception:
        pass
    maps = (
        (diy.input_map, diy.output_map)
        if as_input
        else (diy.output_map, diy.input_map)
    )
    for mapping in maps:
        for fig_id, terminal in mapping.items():
            if fig_id in neighbor_ids:
                return ConnectingOption(None, [terminal])
    return None


# 3DuF / MINT camelCase keys that LFR would otherwise lowercase.
_CANONICAL_PARAM_KEYS = {
    "componentspacing": "componentSpacing",
    "connectionspacing": "connectionSpacing",
    "rotation": "rotation",
    "channelwidth": "channelWidth",
    "flowchannelwidth": "flowChannelWidth",
    "controlchannelwidth": "controlChannelWidth",
    "edgebend": "edgeBend",
    "edgebend1": "edgeBend1",
    "edgebend2": "edgeBend2",
    "bendspacing": "bendSpacing",
    "bendlength": "bendLength",
    "numberofbends": "numberOfBends",
    "minchannellength": "minChannelLength",
    "leafspace": "leafSpace",
    "leafpitch": "leafSpace",
    "stagespace": "stageSpace",
    "valvewidthx": "valveWidthX",
    "valvewidthy": "valveWidthY",
    "portradius": "portRadius",
    "orificesize": "orificeSize",
    "orificelength": "orificeLength",
    "oilinputwidth": "oilInputWidth",
    "waterinputwidth": "waterInputWidth",
    "outputwidth": "outputWidth",
    "outputlength": "outputLength",
    "width": "width",
    "length": "length",
    "spacing": "spacing",
    "roundedchannel": "RoundedChannel",
}


def _canonical_param_key(key: str) -> str:
    mapped = _CANONICAL_PARAM_KEYS.get(key.lower())
    if mapped:
        return mapped
    return key.lower()


def _is_connection_constraint(constraint) -> bool:
    return str(getattr(constraint, "scope", "") or "").lower() == "connection"


def _connection_layer(constraint) -> str:
    return str(getattr(constraint, "layer", "") or "flow").lower()


def _is_flow_connection_constraint(constraint) -> bool:
    if not _is_connection_constraint(constraint):
        return False
    return _connection_layer(constraint) not in {"control", "ctrl", "1"}


def _is_control_connection_constraint(constraint) -> bool:
    if not _is_connection_constraint(constraint):
        return False
    return _connection_layer(constraint) in {"control", "ctrl", "1"}


def _connection_constraints_from_cns(*cns) -> List:
    out = []
    for cn in cns:
        for constraint in getattr(cn, "constraints", []) or []:
            if _is_flow_connection_constraint(constraint):
                out.append(constraint)
    return out


def _flow_connection_constraints_for_edge(from_cn, to_cn) -> List:
    """CHANNEL #CONSTRAIN applies only to the assign that owns this edge.

    Do not union both endpoints: a prior assign's ``RoundedChannel=0`` on the
    upstream mixer must not leak onto the next assign's FLOW pipes (which may
    only set ``channelWidth`` and should otherwise keep defaults).

    Ownership:
    - inlet / cascade (→ mixer): the sink CN is the assign that created the edge
    - outlet (mixer → PORT): the source CN owns the edge; PORT has no CHANNEL map
    """
    to_constraints = _connection_constraints_from_cns(to_cn)
    if to_constraints:
        return to_constraints
    return _connection_constraints_from_cns(from_cn)


def _control_connection_constraints_from_cns(*cns) -> List:
    out = []
    for cn in cns:
        for constraint in getattr(cn, "constraints", []) or []:
            if _is_control_connection_constraint(constraint):
                out.append(constraint)
    return out


def _channel_width_from_constraints(constraints) -> Optional[float]:
    for constraint in constraints or []:
        if _canonical_param_key(constraint.key) != "channelWidth":
            continue
        raw = constraint.get_target_value()
        if raw is None:
            continue
        try:
            value = float(raw)
        except (TypeError, ValueError):
            continue
        if value > 0:
            return value
    return None


def _apply_constraints_to_params(constraints, params: dict, skip_keys=None) -> None:
    """Write LFR #CONSTRAIN key=value pairs into a params dict."""
    if not constraints or params is None:
        return
    skip = {str(k).lower() for k in (skip_keys or ())}
    skip.update({"roundedchannel"})
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
        if key_norm.lower() in skip:
            continue
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


def _apply_constraints_to_components(constraints, components) -> None:
    """Apply LFR directive constraints as component params metadata."""
    if not constraints or not components:
        return
    component_constraints = [
        constraint
        for constraint in constraints
        if not _is_connection_constraint(constraint)
    ]
    if not component_constraints:
        return

    for component in components:
        _apply_constraints_to_params(component_constraints, component.params.data)


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
    are attached afterwards via ``attach_mux_control_ports``. ``#MAP "PUMP" "~"``
    likewise gets one CONTROL PORT per internal valve via
    ``attach_pump_control_ports``.
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
    ctrl_constraints = _control_connection_constraints_from_cns(
        *getattr(variant, "construction_nodes", [])
    )
    attach_mux_control_ports(scaffhold_device, ctrl_constraints)
    attach_pump_control_ports(scaffhold_device, ctrl_constraints)


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


def attach_mux_control_ports(
    scaffhold_device: MINTDevice, control_constraints=None
) -> None:
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
        channel_width = _channel_width_from_constraints(control_constraints)
        if channel_width is None:
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
            mux_ctrl_params = {"channelWidth": channel_width}
            _apply_constraints_to_params(control_constraints, mux_ctrl_params)
            scaffhold_device.create_mint_connection(
                name=channel_name,
                technology="CHANNEL",
                params=mux_ctrl_params,
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


_PUMP_CONTROL_TERMINALS = ("3", "4", "5")


def _pump_control_already_wired(device, pump_id: str) -> bool:
    wanted = set(_PUMP_CONTROL_TERMINALS)
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
            if str(end.component) == pump_id and str(end.port) in wanted:
                return True
    return False


def attach_pump_control_ports(
    scaffhold_device: MINTDevice, control_constraints=None
) -> None:
    """Wire one CONTROL PORT per peristaltic valve (3DuF PUMP pads 3, 4, 5).

    Same idea as ``attach_mux_control_ports``: LFR does not name those pads.
    ``#MAP "PUMP" "~"`` plus ``assign y = ~x`` only describes FLOW; compile
    then hangs ``cp1…cp3`` on the CONTROL layer.
    ``#CONSTRAIN "CTRLCHANNEL" channelWidth = 200`` stamps those pipes.
    """
    from pymint.mintlayer import MINTLayerType

    pumps = [
        component
        for component in scaffhold_device.device.components
        if str(component.entity).upper().replace(" ", "") in {"PUMP", "PUMP3D"}
    ]
    if not pumps:
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
    prefix_ids = len(pumps) > 1 or any(
        str(component.entity).upper() == "MUX"
        for component in scaffhold_device.device.components
    )

    for pump in pumps:
        if _pump_control_already_wired(scaffhold_device.device, pump.ID):
            continue
        params = pump.params.data
        channel_width = _channel_width_from_constraints(control_constraints)
        if channel_width is None:
            channel_width = _pump_control_channel_width(params)
        for i, pump_port in enumerate(_PUMP_CONTROL_TERMINALS):
            base_port = f"cp{i + 1}"
            cport_name = f"{pump.ID}_{base_port}" if prefix_ids else base_port
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
            base_channel = f"cc{i + 1}"
            channel_name = f"{pump.ID}_{base_channel}" if prefix_ids else base_channel
            channel_name = _unique_device_id(existing_conns, channel_name)
            src_target = Target(component_id=cport_name, port="1")
            sink_target = Target(component_id=pump.ID, port=pump_port)
            pump_ctrl_params = {"channelWidth": channel_width}
            _apply_constraints_to_params(control_constraints, pump_ctrl_params)
            scaffhold_device.create_mint_connection(
                name=channel_name,
                technology="CHANNEL",
                params=pump_ctrl_params,
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
        if not out:
            # Storage / IO ids often match component IDs directly.
            for component in scaffhold_device.device.components:
                if str(component.ID) == str(fig_id) or str(component.name) == str(fig_id):
                    out.add(component.ID)
        return out

    def _fig_node_id(node) -> str:
        if isinstance(node, str):
            return node
        for attr in ("ID", "id", "name"):
            value = getattr(node, attr, None)
            if value is not None:
                return str(value)
        return str(node)

    def expand_flow_net(fig_id: str) -> Set[str]:
        """Resolve a FIG id, or the CN covers of its graph neighbors.

        Uncovered FLOW nets (e.g. ``droplets``) never appear in a construction
        node cover. Their distribute valves still sit on the unique pipe between
        the neighboring primitives (nozzle → chamber).
        """
        out = resolve_fig_id(fig_id)
        if out:
            return out
        if fig_id not in fig:
            return out
        try:
            neighbors = list(fig.predecessors(fig_id)) + list(fig.successors(fig_id))
        except Exception:
            neighbors = []
        for nb in neighbors:
            nid = _fig_node_id(nb)
            out |= resolve_fig_id(nid)
            out |= set(fig_to_components.get(nid, set()))
        return out

    def connection_matches(connection, src_comps: Set[str], tgt_comps: Set[str]) -> bool:
        if connection.layer is None or connection.layer.ID != "0":
            return False
        snk = connection.sinks[0] if connection.sinks else None
        if connection.source is None or snk is None:
            return False
        forward = (
            connection.source.component in src_comps and snk.component in tgt_comps
        )
        reverse = (
            connection.source.component in tgt_comps and snk.component in src_comps
        )
        return bool(forward or reverse)

    def _connection_other_entity(connection, known: Set[str]) -> str:
        snk = connection.sinks[0] if connection.sinks else None
        if connection.source is None or snk is None:
            return ""
        other = (
            snk.component
            if connection.source.component in known
            else connection.source.component
        )
        try:
            return str(scaffhold_device.device.get_component(other).entity or "").upper()
        except Exception:
            return ""

    def infer_connection(
        src_comps: Set[str],
        tgt_comps: Set[str],
        fig_src: str = "",
        fig_tgt: str = "",
    ):
        """When an uncovered FLOW net has no CN cover, infer the gated pipe.

        ``distribute`` edges often name a net like ``droplets`` that never
        becomes a construction-node cover. Prefer the unique FLOW channel
        touching the resolved end; if several touch a storage, pick by the
        other end's entity (NOZZLE vs PORT).
        """
        flow = [
            c
            for c in scaffhold_device.device.connections
            if c.layer is not None and c.layer.ID == "0"
        ]
        if src_comps and tgt_comps:
            hits = [c for c in flow if connection_matches(c, src_comps, tgt_comps)]
            if len(hits) == 1:
                return hits[0]
            if len(hits) > 1:
                # Expanded FLOW nets include both endpoints; keep the pipe
                # whose ends sit in src and tgt without collapsing to a loop.
                strict = []
                for c in hits:
                    snk = c.sinks[0] if c.sinks else None
                    if c.source is None or snk is None:
                        continue
                    ends = {c.source.component, snk.component}
                    if ends & src_comps and ends & tgt_comps and len(ends) == 2:
                        strict.append(c)
                if len(strict) == 1:
                    return strict[0]
        if tgt_comps and not src_comps:
            hits = []
            for c in flow:
                snk = c.sinks[0] if c.sinks else None
                if c.source is None or snk is None:
                    continue
                ends = {c.source.component, snk.component}
                if ends & tgt_comps and len(ends - tgt_comps) == 1:
                    hits.append(c)
            if len(hits) == 1:
                return hits[0]
            if len(hits) > 1:
                src_l = str(fig_src).lower()
                tgt_l = str(fig_tgt).lower()

                def score(connection) -> int:
                    ent = _connection_other_entity(connection, tgt_comps)
                    if "NOZZLE" in ent or "DROPLET" in ent:
                        return 0 if "outlet" not in tgt_l else 3
                    if ent == "PORT":
                        return 0 if "outlet" in tgt_l or "outlet" in src_l else 2
                    return 1

                hits.sort(key=score)
                return hits[0]
        if src_comps and not tgt_comps:
            hits = []
            for c in flow:
                snk = c.sinks[0] if c.sinks else None
                if c.source is None or snk is None:
                    continue
                ends = {c.source.component, snk.component}
                if ends & src_comps and len(ends - src_comps) == 1:
                    hits.append(c)
            if len(hits) == 1:
                return hits[0]
        return None

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
        src_comps = expand_flow_net(fig_src)
        tgt_comps = expand_flow_net(fig_tgt)
        conn = None
        for c in scaffhold_device.device.connections:
            if connection_matches(c, src_comps, tgt_comps):
                conn = c
                break
        if conn is None:
            conn = infer_connection(src_comps, tgt_comps, fig_src, fig_tgt)
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


_CHANNEL_TYPE_PARAM_KEYS = ("RoundedChannel", "roundedChannel")


def _is_rounded_constraint_value(raw) -> bool:
    if isinstance(raw, bool):
        return raw
    try:
        return float(raw) >= 0.5
    except (TypeError, ValueError):
        return str(raw).strip().lower() in {"true", "yes", "1", "1.0"}


# 3DuF PUMP CONTROL pipes default to 300 µm (primitives-server).
# valveWidthY sizes the pad; it does not set the CONTROL channel unless
# the user also writes ``#CONSTRAIN "~" controlChannelWidth``.
_PUMP_CONTROL_CHANNEL_WIDTH_DEFAULT_UM = 300.0


def _pump_control_channel_width(params) -> float:
    """CONTROL nets into a PUMP: controlChannelWidth, else primitives default 300."""
    data = getattr(params, "data", None)
    if not isinstance(data, dict):
        data = params if isinstance(params, dict) else {}
    raw = data.get("controlChannelWidth")
    if raw is not None:
        try:
            value = float(raw)
        except (TypeError, ValueError):
            value = 0.0
        if value > 0:
            return value
    return _PUMP_CONTROL_CHANNEL_WIDTH_DEFAULT_UM


def _channel_type_from_constraints(constraints):
    """Honor ``#CONSTRAIN "CHANNEL" RoundedChannel = 0|1``.

    Grammar constraint values are numbers: 0 is square CHANNEL, 1 is rounded.
    Operator-level keys (``#CONSTRAIN "+" channelWidth``) stay on the mapped
    component and do not stamp incident connections.
    """
    for constraint in constraints or []:
        if _canonical_param_key(constraint.key) != "RoundedChannel":
            continue
        raw = constraint.get_target_value()
        if raw is None:
            continue
        if _is_rounded_constraint_value(raw):
            return "ROUNDED CHANNEL", 1
        return "CHANNEL", 0
    return None


def _strip_channel_type_keys_from_components(device) -> None:
    """Keep RoundedChannel on CHANNEL connections, not on MIXER / PUMP / …"""
    for component in device.components:
        entity = str(getattr(component, "entity", "") or "").upper()
        if "CHANNEL" in entity:
            continue
        data = getattr(getattr(component, "params", None), "data", None)
        if not data:
            continue
        for key in _CHANNEL_TYPE_PARAM_KEYS:
            data.pop(key, None)


def create_device_connection(
    source_target: Target,
    target_target: Target,
    name_generator: NameGenerator,
    scaffhold_device: MINTDevice,
    mapping_library: MappingLibrary,
    connection_constraints=None,
) -> None:
    # TODO - Create the connection based on parameters from the connecting option
    # Step 1 - Get the connection from the mapping library
    # TODO: Create new method stubs to get the right connection primitives from the
    # mapping library (this would need extra criteria that that will need evaulation
    # in the future (RAMA Extension))
    primitive = mapping_library.get_default_connection_entry()
    override = _channel_type_from_constraints(connection_constraints)
    if override is None:
        entity = primitive.mint
        cross_section = lfr_parameters.DEFAULT_CONNECTION_CROSS_SECTION
    else:
        entity, cross_section = override
    # Step 2 - Create the connection in the device.
    # Keep instance names as channel_N even when the entity is ROUNDED CHANNEL.
    connection_name = name_generator.generate_name("CHANNEL")
    conn_params = {
        "crossSection": cross_section,
        "length": lfr_parameters.MIN_CONNECTED_COMPONENT_DISTANCE_UM,
        "minChannelLength": lfr_parameters.MIN_CONNECTED_COMPONENT_DISTANCE_UM,
    }
    _apply_constraints_to_params(connection_constraints, conn_params)
    connection = Connection(
        name=connection_name,
        ID=connection_name,
        entity=entity,
        source=source_target,
        sinks=[target_target],
        params=Params(conn_params),
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
