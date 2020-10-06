from pymint.mintcomponent import MINTComponent
from typing import List, Optional
from lfr.fig.interaction import InteractionType
from pymint.mintdevice import MINTDevice
from pymint.antlr.mintLexer import mintLexer
from pymint.antlr.mintParser import mintParser
from pymint.mintcompiler import MINTCompiler
from antlr4 import ParseTreeWalker, CommonTokenStream, FileStream
from os import path


class Primitive:
    def __init__(self, jsondict) -> None:
        self.__mint = jsondict['mint']
        self.__inputs = jsondict['inputs']
        self.__outputs = jsondict['outputs']
        self.__default_netlist_location = jsondict['default-netlist']
        # TODO - Parse the default netlist and generate the netlist to copy into the implement

    @property
    def mint(self):
        return self.__mint

    @property
    def inputs(self):
        return self.__inputs

    @property
    def outputs(self):
        return self.__outputs

    @property
    def default_netlist_location(self):
        return self.__default_netlist_location

    @property
    def default_netlist(self) -> Optional[MINTDevice]:

        if self.__default_netlist_location is None or self.__default_netlist_location == 'None':
            return None

        default_mint_file = path.abspath(self.__default_netlist_location)

        if not path.exists(default_mint_file):
            raise Exception("Default netlist file does not exist")

        path.exists(default_mint_file)

        finput = FileStream(default_mint_file)

        lexer = mintLexer(finput)

        stream = CommonTokenStream(lexer)

        parser = mintParser(stream)

        tree = parser.netlist()

        walker = ParseTreeWalker()

        listener = MINTCompiler()

        walker.walk(listener, tree)

        # Return the default library
        return listener.current_device


class MappingLibrary:

    def __init__(self, jsondict) -> None:
        self.__name = jsondict['name']
        self.__mix_operators = []
        self.__meter_operators = []
        self.__seive_operators = []
        self.__dilute_operators = []
        self.__divide_operators = []
        self.__technology_process_operators = []

        if 'operators' not in jsondict.keys():
            raise Exception("Operator definitions not found in mapping lib")

        for operator_type in jsondict['operators'].keys():
            operators_json = jsondict['operators'][operator_type]
            for operator in operators_json:
                primitive = Primitive(operator)
                if operator_type == 'MIX':
                    self.__mix_operators.append(primitive)
                elif operator_type == 'SEIVE':
                    self.__seive_operators.append(primitive)
                elif operator_type == 'METER':
                    self.__meter_operators.append(primitive)
                elif operator_type == 'DILUTE':
                    self.__dilute_operators.append(primitive)
                elif operator_type == 'DIVIDE':
                    self.__divide_operators.append(primitive)
                else:
                    self.__technology_process_operators.append(primitive)
                
    def get_operators(self, interaction_type: InteractionType) ->List[Primitive] :
        if interaction_type is InteractionType.MIX:
            return self.__mix_operators
        elif interaction_type is InteractionType.SIEVE:
            return self.__seive_operators
        elif interaction_type is InteractionType.DILUTE:
            return self.__dilute_operators
        elif interaction_type is InteractionType.METER:
            return self.__meter_operators
        elif interaction_type is InteractionType.DIVIDE:
            return self.__divide_operators
        else:
            return self.__technology_process_operators
        