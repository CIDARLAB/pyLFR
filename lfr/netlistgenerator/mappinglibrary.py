from lfr import parameters
from lfr.netlistgenerator.namegenerator import NameGenerator
from typing import List, Optional

from pymint.mintcomponent import MINTComponent
from lfr.fig.interaction import InteractionType
from pymint.mintdevice import MINTDevice
from pymint.antlr.mintLexer import mintLexer
from pymint.antlr.mintParser import mintParser
from pymint.mintcompiler import MINTCompiler
from antlr4 import ParseTreeWalker, CommonTokenStream, FileStream
from os import path
from enum import Enum


class PrimitiveType(Enum):
    COMPONENT = 0
    NETLIST = 1
    PROCEDURAL = 2


class ConnectingOption:
    def __init__(
        self,
        component_name: str = None,
        component_port: List[int] = [],
    ) -> None:
        self._component_name: str = component_name
        self._component_port: List[int] = component_port

    @property
    def component_name(self) -> Optional[str]:
        return self._component_name

    @property
    def component_port(self) -> List[int]:
        return self._component_port


class Primitive:
    def __init__(
        self,
        mint: str = None,
        component_type: PrimitiveType = PrimitiveType.COMPONENT,
        match_string: str = None,
        is_storage: bool = False,
        has_storage_control: bool = False,
        inputs: List[ConnectingOption] = [],
        outputs: List[ConnectingOption] = [],
        loadings: List[ConnectingOption] = [],
        carriers: List[ConnectingOption] = [],
        default_netlist: str = None,
        functional_input_params: List[str] = [],
        output_params: List[str] = []
    ) -> None:

        self._component_type: PrimitiveType = component_type
        self._match_string: str = match_string
        self._mint: str = mint
        self._is_storage: bool = is_storage
        self._has_storage_control: bool = has_storage_control
        self._inputs: List[ConnectingOption] = inputs
        self._outputs: List[ConnectingOption] = outputs
        self._loadings: List[ConnectingOption] = loadings
        self._carriers: List[ConnectingOption] = carriers
        self._default_netlist: str = default_netlist

        self._functional_input_params = functional_input_params
        self._output_params = output_params

        # self._mint = jsondict['mint']
        # self._inputs = jsondict['inputs']
        # self._outputs = jsondict['outputs']
        # self._match_string = jsondict['match']
        # self._is_storage = jsondict['is-storage']
        # self._has_storage_control = jsondict['']
        # self._default_netlist_location = jsondict['default-netlist']
        # TODO - Parse the default netlist and generate the netlist to copy into the implement

    @property
    def type(self) -> PrimitiveType:
        return self._component_type

    @property
    def mint(self) -> str:
        return self._mint

    @property
    def inputs(self) -> List[ConnectingOption]:
        return self._inputs

    @property
    def outputs(self) -> List[ConnectingOption]:
        return self._outputs

    @property
    def loadings(self) -> List[ConnectingOption]:
        return self._loadings

    @property
    def carriers(self) -> List[ConnectingOption]:
        return self._carriers

    @property
    def default_netlist_location(self):
        return self._default_netlist_location

    @property
    def inverse_design_query_params(self):
        return self._functional_input_params

    @property
    def output_params(self):
        return self._output_params

    def get_default_component(self, name_gen: NameGenerator) -> MINTComponent:
        if self.type is not PrimitiveType.COMPONENT:
            raise Exception("Cannot execute this method for this kind of a primitive")
        name = name_gen.generate_name(self.mint)
        mc = MINTComponent(name, self.mint, dict())
        return mc

    def get_default_netlist(self, name_gen: NameGenerator) -> MINTDevice:
        if self.type is not PrimitiveType.NETLIST:
            raise Exception("Cannot execute this method for this kind of a  primitive")

        default_mint_file = parameters.LIB_DIR.joinpath(self._default_netlist).resolve()

        if not path.exists(default_mint_file):
            raise Exception("Default netlist file does not exist")

        finput = FileStream(default_mint_file)

        lexer = mintLexer(finput)

        stream = CommonTokenStream(lexer)

        parser = mintParser(stream)

        tree = parser.netlist()

        walker = ParseTreeWalker()

        listener = MINTCompiler()

        walker.walk(listener, tree)

        device = listener.current_device
        # Rename the netlist
        name_gen.rename_netlist(device)

        # Return the default netlist
        return device


class MappingLibrary:
    def __init__(self, name) -> None:
        self.__name = name
        self.__mix_operators = []
        self.__meter_operators = []
        self.__seive_operators = []
        self.__dilute_operators = []
        self.__divide_operators = []
        self.__technology_process_operators = []
        self.__io_primitives = []

    def add_io_entry(self, primitive: Primitive) -> None:
        self.__io_primitives.append(primitive)

    def add_operator_entry(self, primitve: Primitive, interaction_type: InteractionType) -> None:
        if interaction_type is InteractionType.MIX:
            self.__mix_operators.append(primitve)
        elif interaction_type is InteractionType.SIEVE:
            self.__seive_operators.append(primitve)
        elif interaction_type is InteractionType.DILUTE:
            self.__dilute_operators.append(primitve)
        elif interaction_type is InteractionType.METER:
            self.__meter_operators.append(primitve)
        elif interaction_type is InteractionType.DIVIDE:
            self.__divide_operators.append(primitve)
        else:
            self.__technology_process_operators.append(primitve)

    def get_operators(self, interaction_type: InteractionType) -> List[Primitive]:
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
