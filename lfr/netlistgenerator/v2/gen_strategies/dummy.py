from lfr.fig.fluidinteractiongraph import FluidInteractionGraph
from lfr.netlistgenerator.v2.constructiongraph import ConstructionGraph
from lfr.netlistgenerator.v2.gen_strategies.genstrategy import GenStrategy
from lfr.netlistgenerator.v2.mappingoption import MappingOption


class DummyStrategy(GenStrategy):
    def __init__(
        self, construction_graph: ConstructionGraph, fig: FluidInteractionGraph
    ) -> None:
        super().__init__(construction_graph, fig)

    def reduce_mapping_options(self) -> None:
        super().reduce_mapping_options()

    @staticmethod
    def get_flow_flow_mapping_option(subgraph_view) -> MappingOption:
        return None
