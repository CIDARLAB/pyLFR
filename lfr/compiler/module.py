from __future__ import annotations
from typing import Dict, List, Optional
from lfr.netlistgenerator.explicitmapping import ExplicitMapping
from lfr.fig.fignode import FIGNode, IONode, Flow, IOType
from lfr.fig.fluidinteractiongraph import FluidInteractionGraph
from lfr.compiler.moduleio import ModuleIO
from lfr.fig.interaction import FluidFluidCustomInteraction, FluidFluidInteraction, FluidIntegerInteraction, FluidNumberInteraction, FluidProcessInteraction, Interaction, InteractionType
import copy


class Module(object):
    def __init__(self, name):
        self.name = name
        self._imported_modules: List[Module] = []
        self._io: List[ModuleIO] = []
        self.FIG = FluidInteractionGraph()
        self.fluids = dict()
        self.mappings: List[ExplicitMapping] = []

    @property
    def io(self) -> List[ModuleIO]:
        return self._io

    @property
    def imported_modules(self) -> List[Module]:
        return self._imported_modules

    def add_new_import(self, module: Module) -> None:
        self._imported_modules.append(module)

    def get_explicit_mappings(self) -> List[ExplicitMapping]:
        return self.mappings

    def add_io(self, io: ModuleIO):
        self._io.append(io)
        for i in range(len(io.vector_ref)):
            self.FIG.add_fignode(io.vector_ref[i])

    def get_io(self, name: str) -> ModuleIO:
        for module_io in self._io:
            if name == module_io.id:
                return module_io

        raise Exception("ModuleIO:{0} not found !".format(name))

    def get_all_io(self) -> List[ModuleIO]:
        return self._io

    def add_fluid(self, fluid: Flow):
        self.fluids[fluid.id] = fluid
        self.FIG.add_fignode(fluid)

    def get_fluid(self, name: str) -> Optional[FIGNode]:
        return self.FIG.get_fignode(name)

    def add_fluid_connection(self, item1id: str, item2id: str) -> None:
        source = self.FIG.get_fignode(item1id)
        target = self.FIG.get_fignode(item2id)
        self.FIG.connect_fignodes(source, target)

    def add_fluid_custom_interaction(self, item: Flow, operator: str, interaction_type: InteractionType) -> Interaction:
        # Check if the item exists
        finteraction = FluidProcessInteraction(item, operator)
        self.FIG.add_interaction(finteraction)
        return finteraction

    def add_finteraction_custom_interaction(self, item: Interaction, operator: str, interaction_type: InteractionType) -> Interaction:
        # Check if the item exists
        # TODO: create finteraction factory method and FluidInteraction
        # finteraction = FluidInteraction(fluid1=item, interactiontype=interaction_type, custominteraction= operator)
        finteraction = FluidProcessInteraction(item, operator)
        self.FIG.add_interaction(finteraction)
        return finteraction

    def add_fluid_custominteraction(self, fluid1: Flow, fluid2: Flow, interaction: str) -> Interaction:
        finteraction = FluidFluidCustomInteraction(
            fluid1, fluid2, interaction)
        self.FIG.add_interaction(finteraction)
        return finteraction

    def add_fluid_fluid_interaction(self, fluid1: Flow, fluid2: Flow, interaction_type: InteractionType) -> Interaction:

        fluid_interaction = FluidFluidInteraction(fluid1, fluid2, interaction_type)
        self.FIG.add_interaction(fluid_interaction)

        return fluid_interaction

    def add_fluid_finteraction_interaction(self, fluid1: Flow, finteraction: Interaction, interaction_type: InteractionType):
        # TODO: Create new factory method for creating this kind of fluid interaction
        new_fluid_interaction = FluidFluidInteraction(fluid1, finteraction, interaction_type)

        # self.FIG.add_fluid_finteraction_interaction(fluid1, finteraction, new_fluid_interaction)
        self.FIG.add_interaction(new_fluid_interaction)

        return new_fluid_interaction

    def add_finteraction_finteraction_interaction(self, f_interaction1: Interaction, f_interaction2: Interaction, interaction_type: InteractionType) -> Interaction:
        # TODO - Revisit this to fix the fluid data mappings

        new_fluid_interaction = FluidFluidInteraction(f_interaction1, f_interaction2, interaction_type)

        self.FIG.add_interaction(new_fluid_interaction)

        return new_fluid_interaction

    def add_interaction_output(self, output: Flow, interaction: Interaction):
        self.FIG.connect_fignodes(output, interaction)

    def add_fluid_numeric_interaction(self, fluid1: Flow, number: Optional[int, float], interaction_type: InteractionType) -> Interaction:
        # finteraction = FluidInteraction(fluid1=fluid1, interactiontype=interaction)
        finteraction = None

        if interaction_type is InteractionType.METER:
            finteraction = FluidNumberInteraction(fluid1, number, interaction_type)
        elif interaction_type is InteractionType.DILUTE:
            finteraction = FluidNumberInteraction(fluid1, number, interaction_type)
        elif interaction_type is InteractionType.DIVIDE:
            finteraction = FluidIntegerInteraction(fluid1, number, interaction_type)
        else:
            raise Exception("Unsupported Numeric Operator")

        self.FIG.add_interaction(finteraction)

        return finteraction

    def add_mapping(self, mapping: ExplicitMapping):
        self.mappings.append(mapping)

    def __str__(self):
        ret = "Name : " + self.name + "\n"
        for module_io in self._io:
            ret += module_io.__str__()
            ret += "\n"
        return ret

    def instantiate_module(self, type_id: str, var_name: str, io_mapping: Dict[str, str]) -> None:
        # Step 1 - Find the corresponding module from the imports
        module_to_import = None
        for module_check in self.imported_modules:
            if module_check.name == type_id:
                module_to_import = module_check

        # Step 2 - Create a copy of the fig
        fig_copy = copy.deepcopy(module_to_import.FIG)

        # Step 3 - Convert all the flow IO nodes where mappings exist
        # to flow nodes
        for there_node_key in io_mapping.keys():
            fignode = fig_copy.get_fignode(there_node_key)
            # Skip if its a control type one
            if fignode.type is IOType.CONTROL:
                continue
            # Convert this node into a flow node
            # Sanity check to see if its flow input/output
            assert(fignode.type is IOType.FLOW_INPUT or fignode.type is IOType.FLOW_OUTPUT)
            # Replace
            new_fignode = Flow(fignode.id)
            fig_copy.switch_fignode(fignode, new_fignode)

        # Step 4 - Relabel all the nodes with the prefix defined by
        # var_name
        rename_map = dict()
        for node in list(fig_copy.nodes):
            rename_map[node] = self.__generate_instance_node_name(node, var_name)

        fig_copy.rename_nodes(rename_map)

        # Step 5 - Stitch together tall the io newly formed io nodes into
        # current fig
        self.FIG.add_fig(fig_copy)

        # Step 6 - connect all the io nodes
        for there_id, here_id in io_mapping.items():
            # target_fig = self.FIG.get_fignode(rename_map[value])
            # source_fig = self.FIG.get_fignode(key)
            there_check_node = module_to_import.FIG.get_fignode(there_id)
            there_node = self.FIG.get_fignode(rename_map[there_id])
            here_node = self.FIG.get_fignode(here_id)
            if there_check_node.type is IOType.FLOW_INPUT:
                source_node = here_node
                target_node = there_node
            elif there_check_node.type is IOType.FLOW_OUTPUT:
                source_node = there_node
                target_node = here_node
            else:
                source_node = here_node
                target_node = there_node
            assert(source_node is not None)
            assert(target_node is not None)
            self.FIG.connect_fignodes(source_node, target_node)
        pass

    def __generate_instance_node_name(self, node: str, var_name: str) -> str:
        return "{0}_{1}".format(var_name, node)
