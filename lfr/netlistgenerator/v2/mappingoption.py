
from enum import Enum
from lfr.fig.fluidinteractiongraph import FluidInteractionGraph
from typing import List, Optional
from lfr.fig.interaction import InteractionType
from lfr.netlistgenerator.mappinglibrary import MappingLibrary, Primitive
from networkx import nx


class MappingOption():

    def __init__(self, primitive: Primitive = None, subgraph_view=None) -> None:

        self._primitive: Optional[Primitive] = primitive

        self.fig_subgraph: nx.DiGraph = subgraph_view

        # Figure out what computation needs to get done with this
        self._interaction_type: Optional[InteractionType] = None

    @property
    def interaction_type(self):
        return self._interaction_type

    @property
    def primitive(self):
        return self._primitive

    def add_subgraph(self, subgraph_view) -> None:
        self.fig_subgraph = subgraph_view

    # TODO - We need to change this later
    @staticmethod
    def from_explicit_mapping(explicit_mapping: object, mapping_library: MappingLibrary):
        primitive = mapping_library.get_primitive(explicit_mapping.technology)
        # TODO - Figure out how to get the subgraph from the explicit mapping
        sub_graph = explicit_mapping.get_subgraph()
        ret = MappingOption(primitive, sub_graph)
        return ret


class TechnologyMappingType(Enum):
    NO_MAPPING = 0
    OPERATOR_MAPPING = 1
    ASSIGN_MAPPING = 2
    STORAGE_MAPPING = 3


class ExplicitMappingOption(MappingOption):

    def __init__(self, mapping_type: TechnologyMappingType, operator: str = '', technology: str = None) -> None:
        # TODO - Generate this from the Explicit Mapping
        if technology is None or technology == '':
            raise Exception("Cannot instantiate explicit mapping if without primitive reference.")
        self._mapping_type = mapping_type
        self._primitive_mint = technology
        self._mapping_operator = operator
        self._startlist: List[str] = []
        self._endlist: List[str] = []

    @property
    def operator(self) -> str:
        return self._mapping_operator

    @property
    def startlist(self):
        return self._startlist

    @startlist.setter
    def startlist(self, list: List[str]) -> None:
        self._startlist = list

    @property
    def endlist(self):
        return self._endlist

    @endlist.setter
    def endlist(self, list: List[str]) -> None:
        self._endlist = list

    @property
    def technology(self):
        return self._primitive_mint

    def set_find_keys(self, start_list: List[str], end_list: List[str], prefix: str) -> None:
        # TODO - Figure out what start / end match variables strings need to included here
        pass

    def load_primitive_from_library(self, library: MappingLibrary) -> None:
        primitive = library.get_primitive(self._primitive_mint)
        self._primitive = primitive

    def find_subgraph(self, fig: FluidInteractionGraph) -> None:
        # TODO - Figure out how to find the subgraph specific to this
        pass
