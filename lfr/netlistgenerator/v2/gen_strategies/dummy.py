
from lfr.netlistgenerator.v2.mappingoption import MappingOption
from lfr.netlistgenerator.v2.gen_strategies.genstrategy import GenStrategy
from lfr.netlistgenerator.v2.constructiongraph import ConstructionGraph


class DummyStrategy(GenStrategy):

    def __init__(self, construction_graph: ConstructionGraph) -> None:
        super().__init__(construction_graph)

    def reduce_mapping_options(self) -> None:
        # TODO - Implement Generalized Ali Strategy 1

        # Dummy strategy
        for cn in self._construction_graph.construction_nodes:
            print(len(cn.mapping_options))
            # Remove the extra mappings
            del cn.mapping_options[1:len(cn.mapping_options)]
            print(len(cn.mapping_options))
            pass

    def get_flow_flow_mapping_option(self, subgraph_view) -> MappingOption:
        return None
