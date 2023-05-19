# from lfr.netlistgenerator.constructiongraph import ConstructionGraph
from typing import List

import networkx as nx
from pymint import MINTDevice
from lfr.fig.fignode import FIGNode, IOType

from lfr.fig.fluidinteractiongraph import FluidInteractionGraph
from lfr.fig.interaction import Interaction, InteractionType
from lfr.netlistgenerator.constructiongraph.constructiongraph import ConstructionGraph
from lfr.netlistgenerator.constructiongraph.constructionnode import ConstructionNode
from lfr.netlistgenerator.dafdadapter import DAFDAdapter
from lfr.netlistgenerator.gen_strategies.genstrategy import GenStrategy


class DropXStrategy(GenStrategy):
    def __init__(self, fig: FluidInteractionGraph) -> None:
        super().__init__("dropx", fig)

    def validate_construction_graph_flow(
        self, construction_graph: ConstructionGraph
    ) -> bool:
        """
        Validate the construction graph against the rules of the dropx
        generation strategy strategy

        TODO - Future version of this should use a rule based grammar

        Current ruleset for the dropx strategy: can be found in the notes

        Args:
            construction_graph (ConstructionGraph): Construction graph to validate

        Returns:
            bool: True if the construction graph is valid
        """
        # TODO -
        # Step 1 - Perform a topological sort of the fignodes so that we
        # know how to traverse anc check the rules against each of the nodes
        # Step 2 - For each of these fig nodes call the individual rules (all 6/7 of them).
        # Step 3 - If response of any of those 7 is false then return false indicating that
        # its an invalid design. Skip rulecheck if explicitly mapped
        #
        sorted_fignodes = list(nx.topological_sort(self._fig))

        all_paths = []
        input_fignodes = [node.ID for node in self._fig.get_input_fignodes()]
        output_fignodes = [node.ID for node in self._fig.get_output_fignodes()]

        # Get all the paths for the input / output cominations
        nx.all_simple_paths(
            self._fig,
        )
        for fignode in sorted_fignodes:
            # TODO - Skip check if explicitly mapped. Rationale is that user knows best
            rule_1_success = self.__check_rule_1_validity(fignode, construction_graph)
            if rule_1_success is False:
                return False
            rule_2_success = self.__check_rule_2_validity(fignode, construction_graph)
            if rule_2_success is False:
                return False
            rule_3_success = self.__check_rule_3_validity(fignode, construction_graph)
            if rule_3_success is False:
                return False
            rule_4_success = self.__check_rule_4_validity(fignode, construction_graph)
            if rule_4_success is False:
                return False
            rule_5_success = self.__check_rule_5_validity(fignode, construction_graph)
            if rule_5_success is False:
                return False
            rule_6_success = self.__check_rule_6_validity(fignode, construction_graph)
            if rule_6_success is False:
                return False
            rule_7_success = self.__check_rule_7_validity(fignode, construction_graph)
            if rule_7_success is False:
                return False

        return True

    def __search_predecessors(self, fignode_id: str, search_type: InteractionType):
        """recursive function searches for the specified InteractionType in the
        predecessors of the specified fignode_id

        Args:
            fignode_id (str): Starting node to find the
            predecessors
            search_type (InteractionType): Interaction type to find in the predecessors

        Returns:
            Bool: If found, returns true. Else false
        """
        fignode = self._fig.get_fignode(fignode_id)

        if self.__check_if_type(fignode, search_type):
            return True

        else:
            for prednode_id in self._fig.predecessors(fignode_id):
                if self.__search_predecessors(prednode_id, search_type):
                    return True

        return False

    def __check_rule_1_validity(
        self, fignode: str, constructin_graph: ConstructionGraph
    ) -> bool:
        raise NotImplementedError()

    def __check_rule_2_validity(
        self, fignode: str, constructin_graph: ConstructionGraph
    ) -> bool:
        raise NotImplementedError()

    def __check_rule_3_validity(
        self, fignode: str, constructin_graph: ConstructionGraph
    ) -> bool:
        raise NotImplementedError()

    def __check_rule_4_validity(
        self, fignode: str, constructin_graph: ConstructionGraph
    ) -> bool:
        raise NotImplementedError()

    def __check_rule_5_validity(
        self, fignode: str, constructin_graph: ConstructionGraph
    ) -> bool:
        raise NotImplementedError()

    def __check_rule_6_validity(
        self, fignode: str, constructin_graph: ConstructionGraph
    ) -> bool:
        raise NotImplementedError()

    def __check_rule_7_validity(
        self, fignode: str, constructin_graph: ConstructionGraph
    ) -> bool:
        raise NotImplementedError()

    @staticmethod
    def __check_if_type(fignode: FIGNode, search_type: InteractionType):
        """helper function for __search_predecessors and __check_continuous. Check if
        the specified search_type matches to the fignode.type

        Args:
            fignode (FIGNode): fignode that contains InteractionType as type
            search_type ([type]): desired type to check

        Returns:
            Bool: if fignode.type matches to search_type, returns true. Else false
        """
        if isinstance(fignode, Interaction):
            if fignode.type is search_type:
                return True

        return False
