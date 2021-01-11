from lfr.fig.interaction import FluidProcessInteraction, Interaction
from lfr.postprocessor.mapping import (
    FluidicOperatorMapping,
    NetworkMapping,
    NodeMappingTemplate,
    PumpMapping,
    StorageMapping,
)
from lfr.postprocessor.constraints import Constraint
from lfr.antlrgen.lfrXParser import lfrXParser
from lfr.fig.fignode import FIGNode
from typing import Dict, List
from lfr.moduleinstanceListener import ModuleInstanceListener


class PostProcessListener(ModuleInstanceListener):
    def __init__(self) -> None:
        super().__init__()
        self._prev_node_list: List[str] = []
        self._after_node_list: List[str] = []
        self._current_mappings: Dict[str, NodeMappingTemplate] = dict()

    def enterPerformancedirective(self, ctx: lfrXParser.PerformancedirectiveContext):
        super().enterPerformancedirective(ctx)
        # TODO - Make a list of all the nodes previous
        fig = self.currentModule.FIG

        # Update the previous list of nodes
        self.__make_prev_fig_nodes_list()

        # TODO - Generate all the constraints into a list
        operator = ctx.mappingoperator().getText()

        # Create an entry for the operator if it isn't present already,
        # we will use this map to store all the performance directives
        # for the
        if operator not in self._current_mappings.keys():
            mapping = NodeMappingTemplate()
            # mapping.operator = operator
            self._current_mappings[operator] = mapping

        for constraint in ctx.constraint():
            param_name = constraint.ID().getText()
            conditional_operator = constraint.operator.text
            value = float(constraint.number().getText())
            if constraint.unit() is not None:
                unit = constraint.unit().getText()
            else:
                unit = None

            perf_constraint = Constraint()
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

    def exitTechnologymappingdirective(
        self, ctx: lfrXParser.TechnologymappingdirectiveContext
    ):
        super().exitTechnologymappingdirective(ctx)

        mint_string = " ".join([i.getText() for i in ctx.ID()])

        if ctx.assignmode is not None:
            if ctx.assignmode.text == "assign":
                # Create explicit mapping for network node
                mapping = NodeMappingTemplate()
                mapping.technology_string = mint_string
                self._current_mappings["assign"] = mapping
            elif ctx.assignmode.text == "storage":
                # Create explicit mapping for storage node
                mapping = NodeMappingTemplate()
                mapping.technology_string = mint_string
                self._current_mappings["storage"] = mapping
            else:
                raise Exception("Unknown mapping mode found")
        else:
            # Create explicit mapping for the operator
            operator = ctx.mappingoperator().getText()
            mapping = NodeMappingTemplate()
            mapping.technology_string = mint_string
            # mapping.operator = operator
            self._current_mappings[operator] = mapping

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
            lhs = self._lhs_store
            rhs = self._rhs_store

            # Check if there is an `assign` mapping
            if "assign" in self._current_mappings.keys():
                mapping = self._current_mappings["assign"]
                # Now add the LHS and RHS nodes into the mapping
                mapping_instance = NetworkMapping()
                for node in rhs:
                    mapping_instance.input_nodes.append(node)
                for node in lhs:
                    mapping_instance.output_nodes.append(node)

                mapping.instances.append(mapping_instance)

        # TODO - Go through the `nodes_of_interest` and then check to see
        # if any of the nodes have the corresponding mappings in the cache
        if len(nodes_of_interest) > 0:
            for node in nodes_of_interest:
                print(node.__class__)
                if isinstance(node, FluidProcessInteraction) or isinstance(
                    node, Interaction
                ):
                    print(node.operator)
                    # Look for mapping with the corresponding operator
                    if node.operator in self._current_mappings.keys():
                        mapping = self._current_mappings[node.operator]
                        mapping_instance = FluidicOperatorMapping()
                        mapping_instance.operator = node.operator
                        mapping_instance.node = node
                        mapping.instances.append(mapping_instance)

        self.__clear_mappings()

    def __make_prev_fig_nodes_list(self):
        fig = self.currentModule.FIG
        self._prev_node_list = []
        self._after_node_list = []
        for node in fig.nodes:
            self._prev_node_list.append(node)

    def __find_new_fig_nodes(self) -> List[FIGNode]:
        fig = self.currentModule.FIG
        for node in fig.nodes:
            self._after_node_list.append(node)

        nodes_of_interest = [
            n for n in self._after_node_list if n not in self._prev_node_list
        ]

        return [fig.get_fignode(n) for n in nodes_of_interest]

    def __clear_mappings(self) -> None:
        self.currentModule.mappings.extend(self._current_mappings.values())
        self._current_mappings.clear()
