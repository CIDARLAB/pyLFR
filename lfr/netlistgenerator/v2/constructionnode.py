from lfr.netlistgenerator.v2.connectingoption import ConnectingOption
from lfr.netlistgenerator.v2.mappingoption import ExplicitMappingOption, MappingOption
from typing import List
import copy


class ConstructionNode():

    def __init__(self, node_id: str) -> None:
        self._id = node_id
        self._mapping_options: List[MappingOption] = []
        self._explict_mapping_flag = False

        # Connection options that we want to load here
        self._input_options: List[ConnectingOption] = []
        self._output_options: List[ConnectingOption] = []
        self._loading_options: List[ConnectingOption] = []
        self._carrier_options: List[ConnectingOption] = []

    @property
    def input_options(self) -> List[ConnectingOption]:
        return self._input_options

    @property
    def output_options(self) -> List[ConnectingOption]:
        return self._output_options

    @property
    def loading_options(self) -> List[ConnectingOption]:
        return self._loading_options

    @property
    def carrier_options(self) -> List[ConnectingOption]:
        return self._carrier_options

    @property
    def id(self) -> str:
        return self._id

    @property
    def mapping_options(self) -> List[MappingOption]:
        return self._mapping_options

    @mapping_options.setter
    def mapping_options(self, options: List[MappingOption]):
        self._mapping_options = options

    def use_explicit_mapping(self, mapping: ExplicitMappingOption) -> None:
        # Set the flag for explicit mapping
        self._explict_mapping_flag = True
        # Delete all the existing mapping options
        self._mapping_options.clear()
        # Now that we have overwritten all the netlist options here
        # we basically cherry pick the one little bit that we want to attach here
        self._mapping_options.append(mapping)

    def add_mapping_option(self, mapping_option: MappingOption) -> None:
        if self._explict_mapping_flag is True:
            # TODO - Add user flag for overwriting explicit mappings
            print("Warning, cannot update construction graph node {}, since explicit mapping is present")
        else:
            self._mapping_options.append(mapping_option)

    def load_connection_options(self) -> None:
        # TODO - Figure out what do do if its a combinatorial design
        assert(len(self._mapping_options) == 1)
        primitive_ref = self._mapping_options[0].primitive
        if primitive_ref.inputs is not None:
            self._input_options = [copy.copy(c) for c in primitive_ref.inputs]
        if primitive_ref.outputs is not None:
            self._output_options = [copy.copy(c) for c in primitive_ref.outputs]
        if primitive_ref.loadings is not None:
            self._loading_options = [copy.copy(c) for c in primitive_ref.loadings]
        if primitive_ref.carriers is not None:
            self._carrier_options = [copy.copy(c) for c in primitive_ref.carriers]
