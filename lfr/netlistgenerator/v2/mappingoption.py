
from typing import Optional
from lfr.netlistgenerator.explicitmapping import ExplicitMapping
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

    @staticmethod
    def from_explicit_mapping(explicit_mapping: ExplicitMapping, mapping_library: MappingLibrary):
        primitive = mapping_library.get_primitive(explicit_mapping.technology)
        # TODO - Figure out how to get the subgraph from the explicit mapping
        sub_graph = explicit_mapping.get_subgraph()
        ret = MappingOption(primitive, sub_graph)
        return ret


class ExplicitMappingOption(MappingOption):

    def __init__(self, mapping: ExplicitMapping) -> None:
        # TODO - Generate this from the Explicit Mapping
        pass
