
from typing import overload
from lfr.netlistgenerator.v2.constructiongraph import ConstructionGraph
from lfr.netlistgenerator.v2.gen_strategies.genstrategy import GenStrategy


class MARSStrategy(GenStrategy):

    def __init__(self, construction_graph: ConstructionGraph) -> None:
        super().__init__(construction_graph)

    def reduce_mapping_options(self) -> None:
        # TODO - Implement Generalized Ali Strategy 1

        # Dummy strategy
        for cn in [v for k, v in self._construction_nodes.items()]:
            print(len(cn.mapping_options))
            # Remove the extra mappings
            del cn.mapping_options[1:len(cn.mapping_options)]
            print(len(cn.mapping_options))
            pass
