
from enum import Enum
from lfr.netlistgenerator.mappinglibrary import MappingLibrary
from typing import Dict, List, Optional
from lfr.netlistgenerator.v2.mappingoption import ExplicitMappingOption, TechnologyMappingType
from lfr.antlrgen.lfrXParser import lfrXParser
from lfr.antlrgen.lfrXListener import lfrXListener
from lfr.compiler.module import Module


class ConstriantBoundType(Enum):
    EQUALS = 0
    LESS_THAN = 1
    GREATER_THAN = 2
    LESS_THAN_EQUALS = 3
    GREATER_THAN_EQUALS = 4


class PostProcessingListener(lfrXListener):

    def __init__(self, module: Module, mapping_library: MappingLibrary) -> None:
        self._current_module = module
        # self._mapping_mode = TechnologyMappingMODE.NO_MAPPING
        # self._mapping_operator = ''
        # self._current_mapping_technology = ''
        self._current_mappings = []
        # Store all the mappings for each of the modules
        self._all_mappings: Dict[str, List[ExplicitMappingOption]] = dict()
        self._fig_node_module_prefix: str = ""
        self._current_module_name: str = ""
        self._is_mapping_active: bool = False
        pass

    def enterModule(self, ctx: lfrXParser.ModuleContext):
        self._current_module_name = ctx.moduledefinition().ID().getText()
        self._all_mappings[self._current_module_name] = []

    def exitModule(self, ctx: lfrXParser.ModuleContext):
        for mapping_option in self._current_mappings:
            self._all_mappings[self._current_module_name].append(mapping_option)

    def enterTechnologymappingdirective(self, ctx: lfrXParser.TechnologymappingdirectiveContext):
        if ctx.mappingoperator() is None:
            print('Need to map for an assign/storage statement and not an operator')
            if ctx.assignmode == 'assign':
                mapping_mode = TechnologyMappingType.ASSIGN_MAPPING
            elif ctx.assignmode == 'storage':
                mapping_mode = TechnologyMappingType.STORAGE_MAPPING
        else:
            mapping_mode = TechnologyMappingType.OPERATOR_MAPPING
            mapping_operator = ctx.mappingoperator().getText()

        mapping_technology = ' '.join([id.getText() for id in ctx.ID()])
        mapping_option = ExplicitMappingOption(mapping_mode, mapping_operator, mapping_technology)
        self._current_mappings.append(mapping_option)

    def enterAssignstat(self, ctx: lfrXParser.AssignstatContext):
        self._is_mapping_active = True
        # for mapping_option in self._current_mappings:
        #     pass

    def exitAssignstat(self, ctx: lfrXParser.AssignstatContext):
        self._is_mapping_active = False
        # Clean up by adding all the mapping options
        for mapping_option in self._current_mappings:
            self._all_mappings[self._current_module_name].append(mapping_option)

    def exitExpressionterm(self, ctx: lfrXParser.ExpressiontermContext):
        # Check to see if there is a unary operator associated with
        # the expression term
        if ctx.unary_operator() is not None:
            operator = ctx.unary_operator().getText()
            mapping_option = self.__get_current_mapping(operator)

            # If there is no mapping, lets forget about it
            if mapping_option is None:
                return

            variablename = ctx.variables().vectorvar().ID().getText()
            mapping_option.startlist.append(variablename)
            # This is easy, just check to see what the variable is and associate it
            # TODO - Check if everything is working correctly here

    def exitExpression(self, ctx: lfrXParser.ExpressionContext):
        # TODO - Check to see if there is a binary operator mapping necessary
        # Loop through the expression terms and then just do the thing
        operand_list = []
        operators =[operator.getText() for operator in ctx.binary_operator()]
        for i in range(len(operators)):
            operator = operators[i]
            mapping_option = self.__get_current_mapping(operator)

            # If there is no mapping, skip
            if mapping_option is None:
                return

            for expression_term in ctx.expressionterm():
                if expression_term.variables() is not None:
                    if expression_term.variables().vectorvar() is not None:
                        varname = expression_term.variables().vectorvar().ID().getText()
                        operand_list.append(varname)
                    elif expression_term.variables().concatenation() is not None:
                        for var in expression_term.variables().concatenation().vectorvar():
                            operand_list.append(var.ID().getText())
            
        pass

    def __get_current_mapping(self, operator: str) -> Optional[ExplicitMappingOption]:
        """Returns the corresponding mapping option in the
        the current set of options with the right operator.

        Args:
            operator (str): Operator to match against

        Returns:
            Optional[ExplicitMappingOption]: MappingOption
            correstponding to the operator. Returns None if
            it can't find it
        """
        for mapping_option in self._current_mappings:
            if mapping_option.operator == operator:
                return mapping_option
        return None
