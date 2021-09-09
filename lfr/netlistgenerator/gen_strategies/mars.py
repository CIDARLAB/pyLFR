from typing import overload
from lfr.fig.fluidinteractiongraph import FluidInteractionGraph
from lfr.netlistgenerator.gen_strategies.genstrategy import GenStrategy


class MARSStrategy(GenStrategy):
    def __init__(self, fig: FluidInteractionGraph) -> None:
        super().__init__(fig)

    def reduce_mapping_options(self) -> None:
        # TODO - Implement Generalized Ali Strategy 1

        # # Dummy strategy
        # for cn in [v for k, v in self._construction_nodes.items()]:
        #     print(len(cn.mapping_options))
        #     # Remove the extra mappings
        #     del cn.mapping_options[1 : len(cn.mapping_options)]
        #     print(len(cn.mapping_options))
        #     pass
        pass

    def size_netlist(self):
        super()
