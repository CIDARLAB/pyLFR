from typing import Dict, List, Optional

from lfr.antlrgen.lfr.lfrXParser import lfrXParser
from lfr.fig.fignode import FIGNode
from lfr.fig.interaction import FluidProcessInteraction, Interaction
from lfr.moduleinstanceListener import ModuleInstanceListener
from lfr.postprocessor.constraints import MaterialConstraint, PerformanceConstraint
from lfr.postprocessor.mapping import (
    FluidicOperatorMapping,
    NetworkMapping,
    NodeMappingInstance,
    NodeMappingTemplate,
    PumpMapping,
    StorageMapping,
)


class PostProcessListener(ModuleInstanceListener):
    def __init__(self) -> None:
        super().__init__()
        self._prev_node_list: List[str] = []
        self._after_node_list: List[str] = []
        self._current_mappings: Dict[str, NodeMappingTemplate] = {}

    def enterPerformancedirective(self, ctx: lfrXParser.PerformancedirectiveContext):
        super().enterPerformancedirective(ctx)
        # TODO - Make a list of all the nodes previous
        # TODO - Check is this needs to be utilized in the future
        # fig = self.currentModule.FIG

        # Update the previous list of nodes
        self.__make_prev_fig_nodes_list()

        # Quoted target: mapping operator ("+", "~", …), CHANNEL, or CTRLCHANNEL.
        operator = getattr(ctx, "targetText", None)
        if not operator:
            mop = ctx.mappingoperator()
            operator = mop.getText() if mop is not None else ""
        op_upper = str(operator).upper().replace("_", "")
        if op_upper == "CHANNEL":
            operator = "CHANNEL"
        elif op_upper in {"CTRLCHANNEL", "CONTROLCHANNEL"}:
            operator = "CTRLCHANNEL"

        # Create an entry for the operator if it isn't present already,
        # we will use this map to store all the performance directives
        # for the
        if operator not in self._current_mappings.keys():
            mapping = NodeMappingTemplate()
            # mapping.operator = operator
            self._current_mappings[operator] = mapping

        for constraint in ctx.constraint():  # type: ignore
            param_name = constraint.ID().getText()
            conditional_operator = constraint.operator.text
            value = float(constraint.number().getText())
            if constraint.unit() is not None:
                unit = constraint.unit().getText()
            else:
                unit = None

            perf_constraint = PerformanceConstraint()
            if operator == "CHANNEL":
                perf_constraint.scope = "connection"
                perf_constraint.layer = "flow"
            elif operator == "CTRLCHANNEL":
                perf_constraint.scope = "connection"
                perf_constraint.layer = "control"
            if unit is not None:
                perf_constraint.unit = unit

            if conditional_operator == "=":
                perf_constraint.add_target_value(param_name, value)
            elif conditional_operator == "<=":
                perf_constraint.add_target_value(param_name, value)
                perf_constraint.add_max_value(param_name, value)
            elif conditional_operator == ">=":
                perf_constraint.add_target_value(param_name, value)
                perf_constraint.add_min_value(param_name, value)
            elif conditional_operator == ">":
                perf_constraint.add_min_value(param_name, value)
            elif conditional_operator == "<":
                perf_constraint.add_max_value(param_name, value)
            else:
                raise Exception(
                    "Incorrect conditional operator found in the constraint"
                )

            self._current_mappings[operator].constraints.append(perf_constraint)

    def exitMaterialmappingdirective(
        self, ctx: lfrXParser.MaterialmappingdirectiveContext
    ):
        super().exitMaterialmappingdirective(ctx)
        if self.currentModule is None:
            raise ValueError("No module found while processing #MATERIAL")

        identifier_token = ctx.ID(0)
        if identifier_token is None:
            raise ValueError("No identifier found for #MATERIAL")
        identifier = identifier_token.getText()
        if ctx.materialtype is None:
            raise ValueError("No material type found for #MATERIAL")
        material_type = ctx.materialtype.text
        if material_type is None:
            raise ValueError("material type token is None")

        node = self.currentModule.get_fluid(identifier)
        if node is None:
            raise ValueError(
                "Could not find identifier '{}' used in #MATERIAL".format(identifier)
            )

        mapping = NodeMappingTemplate()
        mapping_instance = NodeMappingInstance()
        mapping_instance.node = node
        mapping.instances.append(mapping_instance)

        material_constraint = MaterialConstraint()
        material_constraint.set_material(identifier, material_type)
        mapping.constraints.append(material_constraint)
        self.currentModule.mappings.append(mapping)

    def exitTechnologymappingdirective(
        self, ctx: lfrXParser.TechnologymappingdirectiveContext
    ):
        super().exitTechnologymappingdirective(ctx)

        mint_string = " ".join([i.getText() for i in ctx.ID()])

        if ctx.assignmode is not None:
            if ctx.assignmode.text == "assign":
                self._current_mappings["assign"] = self._mapping_with_technology(
                    mint_string, self._current_mappings.get("assign")
                )
            elif ctx.assignmode.text == "storage":
                self._current_mappings["storage"] = self._mapping_with_technology(
                    mint_string, self._current_mappings.get("storage")
                )
            else:
                raise Exception(
                    "Unknown #MAP mode {0!r}. Mode keywords are "
                    "'assign' and 'storage'. Unary process steps "
                    "(mixer, pump-like, incubator) use an operator "
                    "such as #MAP \"MIXER\" \"~\".".format(
                        ctx.assignmode.text
                    )
                )
        else:
            # Create explicit mapping for the operator. Keep any #CONSTRAIN
            # values already attached to this operator so MAP/CONSTRAIN order
            # does not drop mixer geometry (numberOfBends, channelWidth, …).
            operator = ctx.mappingoperator().getText()
            self._current_mappings[operator] = self._mapping_with_technology(
                mint_string, self._current_mappings.get(operator)
            )

    @staticmethod
    def _mapping_with_technology(
        mint_string: str, existing: Optional[NodeMappingTemplate] = None
    ) -> NodeMappingTemplate:
        mapping = NodeMappingTemplate()
        mapping.technology_string = mint_string
        if existing is not None:
            mapping._constraints.extend(existing.constraints)
            mapping.instances.extend(existing.instances)
        return mapping

    def enterStoragestat(self, ctx: lfrXParser.StoragestatContext):
        # Keep a track of all the fig nodes
        self.__make_prev_fig_nodes_list()
        return super().enterStoragestat(ctx)

    def exitStoragestat(self, ctx: lfrXParser.StoragestatContext):
        # Find the nodes and assign the mapping to the
        # storage node
        nodes_of_interest = self.__find_new_fig_nodes()
        if "storage" in self._current_mappings.keys():
            mapping = self._current_mappings["storage"]
            for node in nodes_of_interest:
                mapping_instance = StorageMapping()
                mapping_instance.node = node
                mapping.instances.append(mapping_instance)
            # Operator #MAP is flushed on the next assignstat. A storage-only
            # module (chamber + distribute, no assign) never hits that path,
            # so register the template here.
            if (
                self.currentModule is not None
                and mapping not in self.currentModule.mappings
            ):
                self.currentModule.mappings.append(mapping)
        return super().exitStoragestat(ctx)

    def enterPumpvarstat(self, ctx: lfrXParser.PumpvarstatContext):
        self.__make_prev_fig_nodes_list()
        return super().enterPumpvarstat(ctx)

    def exitPumpvarstat(self, ctx: lfrXParser.PumpvarstatContext):
        # Find the nodes and assign the mapping to the
        # storage node
        nodes_of_interest = self.__find_new_fig_nodes()
        if "pump" in self._current_mappings.keys():
            mapping = self._current_mappings["pump"]
            for node in nodes_of_interest:
                mapping_instance = PumpMapping()
                mapping_instance.node = node
                mapping.instances.append(mapping_instance)
        return super().exitPumpvarstat(ctx)

    def enterAssignstat(self, ctx: lfrXParser.AssignstatContext):
        self.__make_prev_fig_nodes_list()
        return super().enterAssignstat(ctx)

    def exitAssignstat(self, ctx: lfrXParser.AssignstatContext):
        super().exitAssignstat(ctx)
        nodes_of_interest = self.__find_new_fig_nodes()

        # TODO - Check if there is an assign mapping, then add the mapping
        # to the fig (get the inputs and output nodes from the LHS and RHS)
        if "assign" in self._current_mappings.keys():
            # Get the LHS and RHS nodes here
            lhs: List[FIGNode] = self._lhs_store
            rhs: List[FIGNode] = self._rhs_store

            # Check if there is an `assign` mapping
            if "assign" in self._current_mappings.keys():
                mapping = self._current_mappings["assign"]
                # Now add the LHS and RHS nodes into the mapping
                network_mapping_instance = NetworkMapping()
                for node in rhs:
                    network_mapping_instance.input_nodes.append(node)
                for node in lhs:
                    network_mapping_instance.output_nodes.append(node)

                mapping.instances.append(network_mapping_instance)

        # TODO - Go through the `nodes_of_interest` and then check to see
        # if any of the nodes have the corresponding mappings in the cache
        if len(nodes_of_interest) > 0:
            for node in nodes_of_interest:
                print(node.__class__)
                if isinstance(node, (FluidProcessInteraction, Interaction)):
                    print(node.operator)
                    # Look for mapping with the corresponding operator
                    if node.operator in self._current_mappings.keys():
                        mapping = self._current_mappings[node.operator]
                        mapping_instance = FluidicOperatorMapping()
                        mapping_instance.operator = node.operator
                        mapping_instance.node = node
                        mapping.instances.append(mapping_instance)

        # Scheme B: #CONSTRAIN "CHANNEL" / "CTRLCHANNEL" stamp connections of
        # this assign, not the mapped mixer/pump body (same param names stay split).
        for channel_key in ("CHANNEL", "CTRLCHANNEL"):
            channel_mapping = self._current_mappings.get(channel_key)
            if channel_mapping is None or not channel_mapping.constraints:
                continue
            attached = False
            for node in nodes_of_interest:
                if isinstance(node, (FluidProcessInteraction, Interaction)):
                    mapping_instance = FluidicOperatorMapping()
                    mapping_instance.operator = node.operator
                    mapping_instance.node = node
                    channel_mapping.instances.append(mapping_instance)
                    attached = True
            if not attached:
                network_mapping_instance = NetworkMapping()
                for node in self._rhs_store or []:
                    network_mapping_instance.input_nodes.append(node)
                for node in self._lhs_store or []:
                    network_mapping_instance.output_nodes.append(node)
                if (
                    network_mapping_instance.input_nodes
                    or network_mapping_instance.output_nodes
                ):
                    channel_mapping.instances.append(network_mapping_instance)

        self.__clear_mappings()

    def __make_prev_fig_nodes_list(self):
        if self.currentModule is None:
            raise ValueError("No module found")
        fig = self.currentModule.FIG
        self._prev_node_list = []
        self._after_node_list = []
        for node in fig.nodes:
            self._prev_node_list.append(node)

    def __find_new_fig_nodes(self) -> List[FIGNode]:
        if self.currentModule is None:
            raise ValueError("No module found")
        fig = self.currentModule.FIG
        for node in fig.nodes:
            self._after_node_list.append(node)

        nodes_of_interest = [
            n for n in self._after_node_list if n not in self._prev_node_list
        ]

        return [fig.get_fignode(n) for n in nodes_of_interest]

    def __clear_mappings(self) -> None:
        if self.currentModule is None:
            raise ValueError("No module found")
        self.currentModule.mappings.extend(self._current_mappings.values())
        self._current_mappings.clear()
