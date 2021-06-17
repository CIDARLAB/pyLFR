import copy
from typing import List

from lfr.netlistgenerator.primitive import ProceduralPrimitive
from lfr.netlistgenerator.v2.connectingoption import ConnectingOption
from lfr.netlistgenerator.v2.mappingoption import MappingOption
from lfr.postprocessor.constraints import Constraint


class ConstructionNode:
    def __init__(self, node_id: str) -> None:
        self._id = node_id
        self._mapping_options: List[MappingOption] = []
        self._explict_mapping_flag = False

        # Connection options that we want to load here
        self._input_options: List[ConnectingOption] = []
        self._output_options: List[ConnectingOption] = []
        self._loading_options: List[ConnectingOption] = []
        self._carrier_options: List[ConnectingOption] = []

        # Mapping Constraints
        # These will be all the imported constraints
        self._constraints: List[Constraint] = []

    @property
    def is_explictly_mapped(self) -> bool:
        return self._explict_mapping_flag

    @property
    def constraints(self) -> List[Constraint]:
        return self._constraints

    @constraints.setter
    def constraints(self, vals: List[Constraint]) -> None:
        self._constraints = vals

    @property
    def input_options(self) -> List[ConnectingOption]:
        # return self.mapping_options.[0].primitive.input_options....
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

    def use_explicit_mapping(self, mapping: MappingOption) -> None:
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
            print(
                "Warning, cannot update construction graph node {}, since explicit"
                " mapping is present"
            )
        else:
            self._mapping_options.append(mapping_option)

    def load_connection_options(self) -> None:
        # TODO - Figure out what do do if its a combinatorial design
        assert len(self._mapping_options) == 1
        primitive_ref = self._mapping_options[0].primitive

        self._input_options = primitive_ref.export_inputs(
            self._mapping_options[0].fig_subgraph
        )
        self._output_options = primitive_ref.export_outputs(
            self._mapping_options[0].fig_subgraph
        )

        options = primitive_ref.export_loadings(self._mapping_options[0].fig_subgraph)
        if options is None:
            options = []

        self._loading_options = options

        options = primitive_ref.export_carriers(self._mapping_options[0].fig_subgraph)
        if options is None:
            options = []

        self._carrier_options = options

    def __str__(self) -> str:
        return "Construction Node: {}".format(self.id)
