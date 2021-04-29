from typing import Optional
from lfr.fig.interaction import InteractionType
from lfr.netlistgenerator.mappinglibrary import Primitive
from networkx import nx


class MappingOption:
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
