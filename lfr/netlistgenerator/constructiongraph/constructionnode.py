from lfr.netlistgenerator.primitive import Primitive
from lfr.postprocessor.constraints import Constraint
from lfr.netlistgenerator.connectingoption import ConnectingOption
from lfr.netlistgenerator.mappingoption import MappingOption
from typing import List, Optional, Set
import networkx as nx


class ConstructionNode:
    def __init__(
        self,
        node_id: str,
        primitive: Optional[Primitive] = None,
        subgraph_view: Optional[nx.DiGraph] = None,
    ) -> None:
        self._id = node_id
        self._explict_mapping_flag = False
        self._fig_subgraph: Optional[nx.DiGraph] = subgraph_view
        self._primitive: Optional[Primitive] = primitive

        # Connection options that we want to load here
        self._input_options: List[ConnectingOption] = []
        self._output_options: List[ConnectingOption] = []
        self._loading_options: List[ConnectingOption] = []
        self._carrier_options: List[ConnectingOption] = []

        # Mapping Constraints
        # These will be all the imported constraints
        self._constraints: List[Constraint] = []

    @property
    def primitive(self):
        return self._primitive

    @primitive.setter
    def primitive(self, primitive: Primitive) -> None:
        self._primitive = primitive

    @property
    def fig_subgraph(self):
        return self._fig_subgraph

    @fig_subgraph.setter
    def fig_subgraph(self, subgraph: nx.DiGraph) -> None:
        self._fig_subgraph = subgraph

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
    def fig_cover(self) -> Set[str]:
        """Returns the cover of the figure subgraph

        Returns:
            Set[str]: Cover of the figure subgraph
        """
        return set(self.fig_subgraph.nodes)

    def use_explicit_mapping(self, mapping: MappingOption) -> None:
        """Uses the explicit mapping option passed as the parameter

        Args:
            mapping (MappingOption): MappingOption that needs to set
                here explicitly
        """
        # Set the flag for explicit mapping
        self._explict_mapping_flag = True
        # Delete all the existing mapping options
        self._primitive = mapping.primitive
        # Now that we have overwritten all the netlist options here
        # we basically cherry pick the one little bit that we want to attach here
        self.load_connection_options()

    def load_connection_options(self) -> None:
        """Loads the corresponding different connecting options into
        the construction node
        """
        # Load the input options
        if self.primitive is None:
            raise Exception("Primitive not set for construction node")

        self._input_options = self.primitive.export_inputs(self.fig_subgraph)
        self._output_options = self.primitive.export_outputs(self.fig_subgraph)

        options = self.primitive.export_loadings(self.fig_subgraph)
        if options is None:
            options = []

        self._loading_options = options

        options = self.primitive.export_carriers(self.fig_subgraph)
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

    def has_border_overlap(self, other_node: "ConstructionNode") -> bool:
        """Checks if the border of the current node overlaps with the border"""

        # Step 1 - Get the intersection of the two covers, If the intersection is empty
        # then we do not have a border overlap
        # Step 2 - If any of thos are in the border of the subgraph (i.e. the incoming
        # or outgoing edges are 0)
        # then we have a border overlap

        intersection_cover = self.fig_cover.intersection(other_node.fig_cover)
        if len(intersection_cover) == 0:
            return False
        else:
            # Check if any of the intersection cover is in the border of the subgraph
            for node in intersection_cover:
                if (
                    self.fig_subgraph.in_degree(node) == 0
                    or self.fig_subgraph.out_degree(node) == 0
                ):
                    return True
            return False

    def __str__(self) -> str:
        return "Construction Node: {}".format(self.ID)
