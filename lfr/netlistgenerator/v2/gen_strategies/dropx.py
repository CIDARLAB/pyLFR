from lfr.fig.fluidinteractiongraph import FluidInteractionGraph
from lfr.netlistgenerator.v2.constructiongraph import ConstructionGraph
from lfr.netlistgenerator.v2.gen_strategies.genstrategy import GenStrategy
import networkx as nx


class DropXStrategy(GenStrategy):
    def __init__(
        self, construction_graph: ConstructionGraph, fig: FluidInteractionGraph
    ) -> None:
        super().__init__(construction_graph, fig)

    def reduce_mapping_options(self) -> None:
        # TODO - Implement Generalized Ali Strategy 1
        # Rule 1 - The first level of % should be mapping to a Droplet Generator (TODO - Talk to ali about this or a T junction generator)
        # Rule 2 – Any +-, distribute nodes before % should be in continuous flow (figure out components for this)
        # Rule 3 – Any Remetering (%) should require a droplet breakdown and regeneration (Ask Ali)
        # Rule 4 – Distribute network post Metering stage should be mapped to different kinds of separator / selection/ storage networks
        # Rule 5 – If plus is shown between node that has % in pred and non % in pred, then its pico injection
        # Rule 6 – if plus is sown between two nodes that has % in pred, then its droplet merging
        # Rule 7 – TBD Rule for droplet splitting
        figs_in_order = list(nx.topological_sort(self._fig))
        print(figs_in_order)
        # Finally just reduce the total number of mapping options if greater than 1
        super().reduce_mapping_options()
