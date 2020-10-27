from typing import overload
from lfr.netlistgenerator.v2.mappingoption import MappingOption
from lfr.netlistgenerator.v2.constructiongraph import ConstructionGraph


class GenStrategy:

    def __init__(self, construction_graph: ConstructionGraph) -> None:
        self._construction_graph: ConstructionGraph = construction_graph

    @overload
    def reduce_mapping_options(self) -> None:
        pass
