from __future__ import annotations

import copy
from typing import Dict, List, Optional, Union

from lfr.compiler.moduleio import ModuleIO
from lfr.fig.fignode import FIGNode, Flow, IONode, IOType
from lfr.fig.fluidinteractiongraph import FluidInteractionGraph
from lfr.fig.interaction import (
    FluidFluidInteraction,
    FluidIntegerInteraction,
    FluidNumberInteraction,
    FluidProcessInteraction,
    Interaction,
    InteractionType,
)
from lfr.postprocessor.constraints import DiyTerminalConstraint, PerformanceConstraint
from lfr.postprocessor.mapping import (
    FluidicOperatorMapping,
    NetworkMapping,
    NodeMappingTemplate,
    PumpMapping,
    StorageMapping,
)

# DIYcomponent sides → physical terminals (matches Fluigi/3DuF BlackBox)
DIY_SIDE_TO_TERMINAL = {
    "up": "1",
    "right": "2",
    "down": "3",
    "left": "4",
}
DIY_SIDES = ("up", "right", "down", "left")

# NOZZLE DROPLET GENERATOR local ports (rotation 0, primitives-server coords):
#   3-port junction on the left, 1-port outlet horn on the right:
#
#              1 (top of junction)
#     4 ------[ junction ]========== 2  (single-port horn)
#              3 (bottom of junction)
#
#   1 and 3 face each other → oil. 4 is the water channel of the 3-port
#   part. 2 is the droplet outlet.
#   JSON rotation 90 is 3DuF's vertical flow-focusing pose (clockwise):
#              aqueous (4, water into the junction)
#   oil_left (3) --[ nozzle ]-- oil_right (1)
#              droplets (2, horn down)
#   TREE-PLACE then stacks mixers above the nozzle and the chamber below.
#   A 180° JSON flip (90→270) puts the 3DuF oil holes on the opposite end
#   from the routed channels.
DROPLET_GENERATOR_PORT_TO_TERMINAL = {
    "aqueous": "4",
    "oil_left": "3",
    "oil_right": "1",
    "droplets": "2",
}
DROPLET_GENERATOR_INPUT_PORTS = ("oil_left", "oil_right", "aqueous")
DROPLET_GENERATOR_OUTPUT_PORTS = ("droplets",)
DROPLET_GENERATOR_PORTS = DROPLET_GENERATOR_INPUT_PORTS + DROPLET_GENERATOR_OUTPUT_PORTS


class Module:
    def __init__(self, name):
        self.name = name
        self._imported_modules: List[Module] = []
        self._io: List[ModuleIO] = []
        self.FIG: FluidInteractionGraph = FluidInteractionGraph()
        self.fluids = {}
        self._mappings: List[NodeMappingTemplate] = []

    @property
    def mappings(self) -> List[NodeMappingTemplate]:
        return self._mappings

    @property
    def io(self) -> List[ModuleIO]:
        return self._io

    @property
    def imported_modules(self) -> List[Module]:
        return self._imported_modules

    def add_new_import(self, module: Module) -> None:
        self._imported_modules.append(module)

    def get_explicit_mappings(self) -> List[NodeMappingTemplate]:
        return self.mappings

    def add_io(self, io: ModuleIO):
        self._io.append(io)
        for i in range(len(io.vector_ref)):
            if isinstance(io.vector_ref[i], IONode) is False:
                raise TypeError(
                    "Cannot add IO that is not of type, found {}".format(
                        io.vector_ref[i]
                    )
                )
            self.FIG.add_fignode(io.vector_ref[i])

    def get_io(self, name: str) -> ModuleIO:
        for module_io in self._io:
            if name == module_io.id:
                return module_io

        raise Exception("ModuleIO:{0} not found !".format(name))

    def get_all_io(self) -> List[ModuleIO]:
        return self._io

    def add_fluid(self, fluid: Flow):
        self.fluids[fluid.ID] = fluid
        self.FIG.add_fignode(fluid)

    def get_fluid(self, name: str) -> Optional[FIGNode]:
        return self.FIG.get_fignode(name)

    def add_fluid_connection(self, item1id: str, item2id: str) -> None:
        source = self.FIG.get_fignode(item1id)
        target = self.FIG.get_fignode(item2id)
        self.FIG.connect_fignodes(source, target)

    def add_fluid_custom_interaction(
        self, item: Flow, operator: str, interaction_type: InteractionType
    ) -> Interaction:
        # TODO - Figure out why the interaction_type is not being used here
        # Check if the item exists
        finteraction = FluidProcessInteraction(item, operator)
        self.FIG.add_interaction(finteraction)
        return finteraction

    def add_finteraction_custom_interaction(
        self,
        item: Interaction,
        operator: str,
        interaction_type: InteractionType,
    ) -> Interaction:
        # Check if the item exists
        # TODO: create finteraction factory method and FluidInteraction
        # finteraction = FluidInteraction(fluid1=item, interactiontype=interaction_type,
        # custominteraction= operator)
        finteraction = FluidProcessInteraction(item, operator)
        self.FIG.add_interaction(finteraction)
        return finteraction

    # def add_fluid_custominteraction(
    #     self, fluid1: Flow, fluid2: Flow, interaction: str
    # ) -> Interaction:
    #     finteraction = FluidFluidCustomInteraction(fluid1, fluid2, interaction)
    #     self.FIG.add_interaction(finteraction)
    #     return finteraction

    def add_fluid_fluid_interaction(
        self, fluid1: Flow, fluid2: Flow, interaction_type: InteractionType
    ) -> Interaction:
        fluid_interaction = FluidFluidInteraction(fluid1, fluid2, interaction_type)
        self.FIG.add_interaction(fluid_interaction)

        return fluid_interaction

    def add_fluid_finteraction_interaction(
        self,
        fluid1: Flow,
        finteraction: Interaction,
        interaction_type: InteractionType,
    ) -> Interaction:
        # TODO: Create new factory method for creating this kind of fluid interaction
        new_fluid_interaction = FluidFluidInteraction(
            fluid1, finteraction, interaction_type
        )

        self.FIG.add_interaction(new_fluid_interaction)

        return new_fluid_interaction

    def add_finteraction_finteraction_interaction(
        self,
        f_interaction1: Interaction,
        f_interaction2: Interaction,
        interaction_type: InteractionType,
    ) -> Interaction:
        # TODO - Revisit this to fix the fluid data mappings

        new_fluid_interaction = FluidFluidInteraction(
            f_interaction1, f_interaction2, interaction_type
        )

        self.FIG.add_interaction(new_fluid_interaction)

        return new_fluid_interaction

    def add_interaction_output(self, output: Flow, interaction: Interaction):
        self.FIG.connect_fignodes(output, interaction)

    def add_fluid_numeric_interaction(
        self,
        fluid1: Flow,
        number: Union[int, float],
        interaction_type: InteractionType,
    ) -> Interaction:
        """Add a fluid numeric interaction to the module

        Args:
            fluid1 (Flow): Fluid to interact with
            number (Union[int, float]): Number to interact with
            interaction_type (InteractionType): Type of interaction

        Raises:
            NotImplementedError: Currently not supporting variables and their lookups
            ValueError: If the interaction type is not supported

        Returns:
            Interaction: The interaction that was added
        """

        finteraction: Union[FluidIntegerInteraction, FluidNumberInteraction]

        if interaction_type is InteractionType.METER:
            finteraction = FluidNumberInteraction(fluid1, number, interaction_type)
        elif interaction_type is InteractionType.DILUTE:
            if isinstance(number, float):
                finteraction = FluidNumberInteraction(fluid1, number, interaction_type)
            elif isinstance(number, int):
                raise ValueError("Dilute interaction only supports float values")
            else:
                # If its a variable get the corresponding value for it
                # from the variable store
                raise NotImplementedError()
        elif interaction_type is InteractionType.DIVIDE:
            if isinstance(number, int):
                finteraction = FluidIntegerInteraction(fluid1, number, interaction_type)
            elif isinstance(number, float):
                raise ValueError("Divide interaction only supports integer values")
            else:
                # If its a variable get the corresponding value for it
                # from the variable store
                raise NotImplementedError()
        else:
            raise ValueError(f"Unsupported Numeric Operator: {interaction_type}")

        self.FIG.add_interaction(finteraction)

        return finteraction

    def __str__(self):
        ret = "Name : " + self.name + "\n"
        for module_io in self._io:
            ret += module_io.__str__()
            ret += "\n"
        return ret

    def instantiate_module(
        self,
        type_id: str,
        var_name: str,
        io_mapping: Dict[str, str],
        instance_params: Optional[Dict[str, float]] = None,
    ) -> None:
        # Step 1 - Find the corresponding module from the imports
        module_to_import = None
        for module_check in self.imported_modules:
            if module_check.name == type_id:
                module_to_import = module_check

        # Step 2 - Create a copy of the fig
        if module_to_import is None:
            raise ReferenceError("module_to_import is set to none")

        fig_copy: FluidInteractionGraph = copy.deepcopy(module_to_import.FIG)

        # Step 3 - Convert all the flow IO nodes where mappings exist
        # to flow nodes
        for there_node_key in io_mapping.keys():
            fignode = fig_copy.get_fignode(there_node_key)
            # Skip if its a control type one
            if isinstance(fignode, IONode) is True:
                if fignode.type is IOType.CONTROL:  # type: ignore
                    continue
            else:
                raise TypeError("Node not of type IO Node")

            # Convert this node into a flow node
            # Replace
            new_fignode = Flow(fignode.ID)
            fig_copy.switch_fignode(fignode, new_fignode)

        # Step 4 - Relabel all the nodes with the prefix defined by
        # var_name
        fig_node_rename_map = {}
        annotation_rename_map = {}
        for node in list(fig_copy.nodes):
            fig_node_rename_map[node] = self.__generate_instance_node_name(
                node, var_name
            )

        # Step 4.1 - Relabel all the annotations with the prefix defined by var_name
        for annotation in list(fig_copy.annotations):
            annotation_rename_map[annotation.id] = self.__generate_instance_node_name(
                annotation.id, var_name
            )

        fig_copy.rename_nodes(fig_node_rename_map)
        fig_copy.rename_annotations(fig_node_rename_map, annotation_rename_map)

        # Step 5 - Stitch together tall the io newly formed io nodes into
        # current fig
        self.FIG.add_fig(fig_copy)

        # Step 6 - connect all the io nodes
        for there_id, here_id in io_mapping.items():
            # target_fig = self.FIG.get_fignode(rename_map[value])
            # source_fig = self.FIG.get_fignode(key)
            there_check_node = module_to_import.FIG.get_fignode(there_id)
            there_node = self.FIG.get_fignode(fig_node_rename_map[there_id])
            here_node = self.FIG.get_fignode(here_id)
            if (
                isinstance(there_check_node, IONode)
                and there_check_node.type is IOType.FLOW_INPUT
            ):
                source_node = here_node
                target_node = there_node
            elif (
                isinstance(there_check_node, IONode)
                and there_check_node.type is IOType.FLOW_OUTPUT
            ):
                source_node = there_node
                target_node = here_node
            else:
                source_node = here_node
                target_node = there_node
            assert source_node is not None
            assert target_node is not None
            self.FIG.connect_fignodes(source_node, target_node)

        # TODO - Step 7 - Make copies of all the mappingtemplates for the final FIG.
        # Since we only utilize mappings based on the assicated fig node it should be
        # possible to find the corresponding fignodes by ID's
        for mappingtemplate in module_to_import.mappings:
            # TODO - Switch this to shallow copy implementation if the scheme needs to
            # follow python specs correctly
            mappingtemplate_copy = copy.deepcopy(mappingtemplate)
            # TODO - Switch out each of the instances here
            for mapping_instance in mappingtemplate_copy.instances:
                if isinstance(
                    mapping_instance,
                    (FluidicOperatorMapping, StorageMapping, PumpMapping),
                ):
                    # Swap the basic node from original to the instance
                    there_node_id = mapping_instance.node.ID
                    here_node = self.FIG.get_fignode(fig_node_rename_map[there_node_id])
                    mapping_instance.node = here_node
                elif isinstance(mapping_instance, NetworkMapping):
                    # TODO - Swap the nodes in the inputs and the outputs
                    # Swap the inputs
                    nodes_to_switch = mapping_instance.input_nodes
                    mapping_instance.input_nodes = self.__switch_fignodes_list(
                        fig_node_rename_map, nodes_to_switch
                    )

                    nodes_to_switch = mapping_instance.output_nodes
                    mapping_instance.output_nodes = self.__switch_fignodes_list(
                        fig_node_rename_map, nodes_to_switch
                    )

            # Override size / keepout constraints for this instance
            # (e.g. DIYcomponent #(length=10000, width=8000, componentSpacing=3000) box(...))
            if instance_params:
                from lfr.postprocessor.constraints import PerformanceConstraint

                kept = [
                    c
                    for c in mappingtemplate_copy.constraints
                    if getattr(c, "key", None) not in instance_params
                ]
                for key, value in instance_params.items():
                    perf = PerformanceConstraint()
                    perf.add_target_value(str(key), float(value))
                    kept.append(perf)
                mappingtemplate_copy._constraints = kept

            self.mappings.append(mappingtemplate_copy)

    def _infer_diy_side_role(self, here_node: FIGNode) -> str:
        """Infer whether a bound net feeds the DIY box (input) or leaves it (output)."""
        if isinstance(here_node, IONode):
            if here_node.type is IOType.FLOW_OUTPUT:
                return "output"
            if here_node.type is IOType.FLOW_INPUT:
                return "input"
        # Intermediate flow: already driven → into the box; else box drives it.
        try:
            preds = list(self.FIG.predecessors(here_node.ID))
        except Exception:
            preds = []
        if preds:
            return "input"
        return "output"

    def instantiate_diy_component(
        self,
        var_name: str,
        side_bindings: Dict[str, Optional[str]],
        imported_module: "Module",
        instance_params: Optional[Dict[str, float]] = None,
    ) -> None:
        """Instantiate DIYcomponent with up/right/down/left (None = unused)."""
        inputs = []  # (terminal, here_node)
        outputs = []
        for side in DIY_SIDES:
            here_id = side_bindings.get(side)
            if here_id is None:
                continue
            if side not in DIY_SIDE_TO_TERMINAL:
                raise ValueError(f"Unknown DIYcomponent side: {side}")
            here_node = self.FIG.get_fignode(here_id)
            if here_node is None:
                raise ValueError(
                    f"DIYcomponent side .{side} bound to unknown net `{here_id}`"
                )
            role = self._infer_diy_side_role(here_node)
            term = DIY_SIDE_TO_TERMINAL[side]
            if role == "input":
                inputs.append((term, here_node))
            else:
                outputs.append((term, here_node))

        if not inputs or not outputs:
            raise ValueError(
                "DIYcomponent requires at least one connected input-side net and "
                "one output-side net (use None for unused sides)"
            )

        seed = inputs[0][1]
        proc = self.add_fluid_custom_interaction(
            seed, "~", InteractionType.TECHNOLOGY_PROCESS
        )
        proc.operator = "~"
        # Extra inputs into the same process (no MIX stage)
        for _term, node in inputs[1:]:
            self.FIG.connect_fignodes(node, proc)
        for _term, node in outputs:
            self.FIG.connect_fignodes(proc, node)

        input_map = {node.ID: term for term, node in inputs}
        output_map = {node.ID: term for term, node in outputs}

        # Attach explicit DIYCOMPONENT mapping (+ size overrides) to this process
        if imported_module.mappings:
            for mappingtemplate in imported_module.mappings:
                mappingtemplate_copy = copy.deepcopy(mappingtemplate)
                for mapping_instance in mappingtemplate_copy.instances:
                    if isinstance(mapping_instance, FluidicOperatorMapping):
                        mapping_instance.node = proc
                        mapping_instance.operator = "~"
                kept = list(mappingtemplate_copy.constraints)
                if instance_params:
                    kept = [
                        c
                        for c in kept
                        if getattr(c, "key", None) not in instance_params
                    ]
                    for key, value in instance_params.items():
                        perf = PerformanceConstraint()
                        perf.add_target_value(str(key), float(value))
                        kept.append(perf)
                kept.append(DiyTerminalConstraint(input_map, output_map))
                mappingtemplate_copy._constraints = kept
                if mappingtemplate_copy.technology_string is None:
                    mappingtemplate_copy.technology_string = "DIYCOMPONENT"
                self.mappings.append(mappingtemplate_copy)
        else:
            mt = NodeMappingTemplate()
            mt.technology_string = "DIYCOMPONENT"
            opmap = FluidicOperatorMapping()
            opmap.node = proc
            opmap.operator = "~"
            mt.instances.append(opmap)
            constraints = [DiyTerminalConstraint(input_map, output_map)]
            if instance_params:
                for key, value in instance_params.items():
                    perf = PerformanceConstraint()
                    perf.add_target_value(str(key), float(value))
                    constraints.append(perf)
            mt._constraints = constraints
            self.mappings.append(mt)

    def ensure_standalone_diy_component_terminals(self) -> None:
        """Wire all four DIYcomponent sides when the library seed is synthesized alone.

        The seed assign is ``down = ~up``. That leaves ``right`` / ``left``
        orphaned, so netlist generation used to emit floating PORTs. Parent
        instances already go through ``instantiate_diy_component``.
        """
        io_ids = {io.id for io in self.io}
        if not set(DIY_SIDES).issubset(io_ids):
            return

        diy_maps = [
            m
            for m in self.mappings
            if m.technology_string
            and "DIYCOMPONENT" in str(m.technology_string).upper().replace(" ", "")
        ]
        if not diy_maps:
            return

        proc = None
        target_map = None
        for mapping in diy_maps:
            for constraint in mapping.constraints or []:
                if isinstance(constraint, DiyTerminalConstraint):
                    return
            for inst in mapping.instances:
                if isinstance(inst, FluidicOperatorMapping) and inst.node is not None:
                    proc = inst.node
                    target_map = mapping
                    break
            if proc is not None:
                break
        if proc is None or target_map is None:
            return

        input_sides = ("up", "right")
        output_sides = ("down", "left")
        input_map: Dict[str, str] = {}
        output_map: Dict[str, str] = {}
        for side in input_sides:
            node = self.FIG.get_fignode(side)
            if node is None:
                return
            if self.FIG.out_degree(side) == 0:
                self.FIG.connect_fignodes(node, proc)
            input_map[node.ID] = DIY_SIDE_TO_TERMINAL[side]
        for side in output_sides:
            node = self.FIG.get_fignode(side)
            if node is None:
                return
            if self.FIG.in_degree(side) == 0:
                self.FIG.connect_fignodes(proc, node)
            output_map[node.ID] = DIY_SIDE_TO_TERMINAL[side]

        target_map._constraints = list(target_map.constraints or [])
        target_map._constraints.append(DiyTerminalConstraint(input_map, output_map))

    def ensure_standalone_droplet_generator_terminals(self) -> None:
        """Wire oil_left/oil_right onto a #MAP NOZZLE seed assign.

        Library ``droplet_generator`` bodies use ``assign droplets = ~aqueous``
        so #MAP can attach. That leaves oil IO orphaned and lets
        ``dropletgenerator.mint`` inject two extra oil PORTs. Parent instances
        already go through ``instantiate_droplet_generator``; this closes the
        same gap when the module is synthesized standalone.
        """
        io_ids = {io.id for io in self.io}
        if not set(DROPLET_GENERATOR_PORTS).issubset(io_ids):
            return

        nozzle_maps = [
            m
            for m in self.mappings
            if m.technology_string
            and "NOZZLE DROPLET GENERATOR"
            in str(m.technology_string).upper().replace("_", " ")
        ]
        if not nozzle_maps:
            return

        proc = None
        target_map = None
        for mapping in nozzle_maps:
            for constraint in mapping.constraints or []:
                if isinstance(constraint, DiyTerminalConstraint):
                    return  # already fully bound (import path)
            for inst in mapping.instances:
                if isinstance(inst, FluidicOperatorMapping) and inst.node is not None:
                    proc = inst.node
                    target_map = mapping
                    break
            if proc is not None:
                break
        if proc is None or target_map is None:
            return

        input_map: Dict[str, str] = {}
        output_map: Dict[str, str] = {}
        for port in DROPLET_GENERATOR_INPUT_PORTS:
            node = self.FIG.get_fignode(port)
            if node is None:
                return
            if port != "aqueous" and self.FIG.out_degree(port) == 0:
                self.FIG.connect_fignodes(node, proc)
            input_map[node.ID] = DROPLET_GENERATOR_PORT_TO_TERMINAL[port]
        for port in DROPLET_GENERATOR_OUTPUT_PORTS:
            node = self.FIG.get_fignode(port)
            if node is None:
                return
            output_map[node.ID] = DROPLET_GENERATOR_PORT_TO_TERMINAL[port]

        target_map._constraints = list(target_map.constraints or [])
        target_map._constraints.append(DiyTerminalConstraint(input_map, output_map))

    def ensure_metering_nozzle_terminals(self) -> None:
        """Bind aqueous→4 / droplets→2 for a 2-port #MAP NOZZLE metering case.

        ``map_droplet.lfr`` uses ``assign droplets = aqueous % 100`` with only
        aqueous/droplets IO. Without a DiyTerminalConstraint the METER library
        options fall back to ports 1/3, which are the oil faces under rot 90.
        """
        io_ids = {io.id for io in self.io}
        if "aqueous" not in io_ids or "droplets" not in io_ids:
            return
        # Full 4-port bodies are handled by ensure_standalone_droplet_generator.
        if set(DROPLET_GENERATOR_PORTS).issubset(io_ids):
            return

        nozzle_maps = [
            m
            for m in self.mappings
            if m.technology_string
            and "NOZZLE DROPLET GENERATOR"
            in str(m.technology_string).upper().replace("_", " ")
        ]
        if not nozzle_maps:
            return

        proc = None
        target_map = None
        for mapping in nozzle_maps:
            for constraint in mapping.constraints or []:
                if isinstance(constraint, DiyTerminalConstraint):
                    return
            for inst in mapping.instances:
                if isinstance(inst, FluidicOperatorMapping) and inst.node is not None:
                    proc = inst.node
                    target_map = mapping
                    break
            if proc is not None:
                break
        if proc is None or target_map is None:
            return

        aqueous = self.FIG.get_fignode("aqueous")
        droplets = self.FIG.get_fignode("droplets")
        if aqueous is None or droplets is None:
            return
        input_map = {aqueous.ID: DROPLET_GENERATOR_PORT_TO_TERMINAL["aqueous"]}
        output_map = {droplets.ID: DROPLET_GENERATOR_PORT_TO_TERMINAL["droplets"]}
        target_map._constraints = list(target_map.constraints or [])
        target_map._constraints.append(DiyTerminalConstraint(input_map, output_map))

    def instantiate_droplet_generator(
        self,
        var_name: str,
        io_mapping: Dict[str, str],
        imported_module: "Module",
        instance_params: Optional[Dict[str, float]] = None,
    ) -> None:
        """Bind oil_left / oil_right / aqueous / droplets onto one 4-port nozzle."""
        missing = [p for p in DROPLET_GENERATOR_PORTS if p not in io_mapping]
        if missing:
            raise ValueError(
                "droplet_generator `{}` requires oil_left, oil_right, aqueous, "
                "droplets; missing: {}".format(var_name, ", ".join(missing))
            )

        inputs = []
        for port in DROPLET_GENERATOR_INPUT_PORTS:
            here_node = self.FIG.get_fignode(io_mapping[port])
            if here_node is None:
                raise ValueError(
                    "droplet_generator port `{}` bound to unknown net `{}`".format(
                        port, io_mapping[port]
                    )
                )
            inputs.append((DROPLET_GENERATOR_PORT_TO_TERMINAL[port], here_node))

        outputs = []
        for port in DROPLET_GENERATOR_OUTPUT_PORTS:
            here_node = self.FIG.get_fignode(io_mapping[port])
            if here_node is None:
                raise ValueError(
                    "droplet_generator port `{}` bound to unknown net `{}`".format(
                        port, io_mapping[port]
                    )
                )
            outputs.append((DROPLET_GENERATOR_PORT_TO_TERMINAL[port], here_node))

        seed = inputs[0][1]
        proc = self.add_fluid_custom_interaction(
            seed, "~", InteractionType.TECHNOLOGY_PROCESS
        )
        proc.operator = "~"
        for _term, node in inputs[1:]:
            self.FIG.connect_fignodes(node, proc)
        for _term, node in outputs:
            self.FIG.connect_fignodes(proc, node)

        input_map = {node.ID: term for term, node in inputs}
        output_map = {node.ID: term for term, node in outputs}

        if imported_module.mappings:
            for mappingtemplate in imported_module.mappings:
                mappingtemplate_copy = copy.deepcopy(mappingtemplate)
                for mapping_instance in mappingtemplate_copy.instances:
                    if isinstance(mapping_instance, FluidicOperatorMapping):
                        mapping_instance.node = proc
                        mapping_instance.operator = "~"
                kept = list(mappingtemplate_copy.constraints)
                if instance_params:
                    kept = [
                        c
                        for c in kept
                        if getattr(c, "key", None) not in instance_params
                    ]
                    for key, value in instance_params.items():
                        perf = PerformanceConstraint()
                        perf.add_target_value(str(key), float(value))
                        kept.append(perf)
                kept.append(DiyTerminalConstraint(input_map, output_map))
                mappingtemplate_copy._constraints = kept
                if mappingtemplate_copy.technology_string is None:
                    mappingtemplate_copy.technology_string = "NOZZLE DROPLET GENERATOR"
                self.mappings.append(mappingtemplate_copy)
        else:
            mt = NodeMappingTemplate()
            mt.technology_string = "NOZZLE DROPLET GENERATOR"
            opmap = FluidicOperatorMapping()
            opmap.node = proc
            opmap.operator = "~"
            mt.instances.append(opmap)
            constraints = [DiyTerminalConstraint(input_map, output_map)]
            if instance_params:
                for key, value in instance_params.items():
                    perf = PerformanceConstraint()
                    perf.add_target_value(str(key), float(value))
                    constraints.append(perf)
            mt._constraints = constraints
            self.mappings.append(mt)

    def __switch_fignodes_list(self, rename_map, nodes_to_switch):
        there_node_ids = [n.id for n in nodes_to_switch]
        here_nodes = [
            self.FIG.get_fignode(rename_map[there_node_id])
            for there_node_id in there_node_ids
        ]
        return here_nodes

    @staticmethod
    def __generate_instance_node_name(node: str, var_name: str) -> str:
        return "{0}_{1}".format(var_name, node)
