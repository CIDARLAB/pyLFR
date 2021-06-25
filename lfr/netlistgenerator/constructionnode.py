from lfr.postprocessor.constraints import Constraint
from lfr.netlistgenerator.connectingoption import ConnectingOption
from lfr.netlistgenerator.mappingoption import MappingOption
from typing import List


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
        """Returns the list of loading options for the mapption option candidate

        Returns:
            List[ConnectingOption]: List of loading options
        """
        return self._loading_options

    @property
    def carrier_options(self) -> List[ConnectingOption]:
        """Returns the list of carrier options set for the construction node

        Returns:
            List[ConnectingOption]: List of carrier options
        """
        return self._carrier_options

    @property
    def ID(self) -> str:
        """Returns the id of the construction node

        Returns:
            str: ID of the construction node
        """
        return self._id

    @property
    def mapping_options(self) -> List[MappingOption]:
        """Returns the list connecting options on the
        construction node

        Returns:
            List[MappingOption]: Mapping options available for the construction node
        """
        return self._mapping_options

    @mapping_options.setter
    def mapping_options(self, options: List[MappingOption]):
        """Sets the mapping options

        Args:
            options (List[MappingOption]): MappingOptions
        """
        self._mapping_options = options

    def use_explicit_mapping(self, mapping: MappingOption) -> None:
        """Uses the explicit mapping option passed as the parameter

        Args:
            mapping (MappingOption): MappingOption that needs to set
                here explicitly
        """
        # Set the flag for explicit mapping
        self._explict_mapping_flag = True
        # Delete all the existing mapping options
        self._mapping_options.clear()
        # Now that we have overwritten all the netlist options here
        # we basically cherry pick the one little bit that we want to attach here
        self._mapping_options.append(mapping)
        self.load_connection_options()

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
        """Loads the corresponding different connecting options into
        the construction node
        """
        # TODO - Figure out what do do if its a combinatorial design
        if len(self._mapping_options) != 1:
            raise Exception(
                "More than one mapping options present for construction node, cannot"
                " load connecting options"
            )
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

    def merge_construction_node(self, construction_node: "ConstructionNode") -> None:
        """Merges the construction node passed as an arugment into the this
        construction node.

        This will let us handle the scenario where we might want to merge
        construction nodes that have undercoverage and help support the future
        combinatorial generation options


        Args:
            construction_node (ConstructionNode): [description]
        """
        raise NotImplementedError(
            "Implement this when we are trying to make combinatorial operations work"
        )

    def __str__(self) -> str:
        return "Construction Node: {}".format(self.ID)
