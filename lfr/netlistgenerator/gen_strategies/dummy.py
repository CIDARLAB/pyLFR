from lfr.fig.fluidinteractiongraph import FluidInteractionGraph
from lfr.netlistgenerator.mappingoption import MappingOption
from lfr.netlistgenerator.gen_strategies.genstrategy import GenStrategy

# from lfr.netlistgenerator.constructiongraph import ConstructionGraph


class DummyStrategy(GenStrategy):
    def __init__(self, fig: FluidInteractionGraph) -> None:
        super().__init__(fig)

    def reduce_mapping_options(self) -> None:
        super().reduce_mapping_options()

    @staticmethod
    def get_flow_flow_mapping_option(subgraph_view) -> MappingOption:
        return None
