from lfr.netlistgenerator.v2.dafdadapter import DAFDAdapter
from lfr.fig.fluidinteractiongraph import FluidInteractionGraph
from lfr.netlistgenerator.v2.constructiongraph import ConstructionGraph
from lfr.netlistgenerator.v2.gen_strategies.genstrategy import GenStrategy
import networkx as nx
from pymint import MINTDevice


class DropXStrategy(GenStrategy):
    def __init__(
        self, construction_graph: ConstructionGraph, fig: FluidInteractionGraph
    ) -> None:
        super().__init__(construction_graph, fig)

    def reduce_mapping_options(self) -> None:
        # Generate a topological order for the FIG to make sure athat we know the order of things
        figs_in_order = list(nx.topological_sort(self._fig))
        print(figs_in_order)
        # Generate the mapping between fignodes and construction nodes
        fig_cn_map = dict()
        # TODO - Implement Generalized Ali Strategy 1
        # Rule 1 - The first level of % should be mapping to a Droplet Generator (TODO - Talk to ali about this or a T junction generator)
        # Rule 2 – Any +-, distribute nodes before % should be in continuous flow (figure out components for this)
        # TODO - Go through each of the FIG nodes, if the fig node has

        # Rule 3 – Any Remetering (%) should require a droplet breakdown and regeneration (Ask Ali)
        # Rule 4 – Distribute network post Metering stage should be mapped to different kinds of separator / selection/ storage networks
        # Rule 5 – If plus is shown between node that has % in pred and non % in pred, then its pico injection
        # Rule 6 – if plus is sown between two nodes that has % in pred, then its droplet merging
        # Rule 7 – TBD Rule for droplet splitting
        # Finally just reduce the total number of mapping options if greater than 1
        super().reduce_mapping_options()

    def size_netlist(self, device: MINTDevice) -> None:
        """
        Sizes the device based on either lookup tables, inverse design algorithms, etc.
        """
        dafd_adapter = DAFDAdapter(device)
        # Default size for PORT is 2000 um
        for component in device.components:
            constraints = self._construction_graph.get_component_cn(
                component
            ).constraints
            if component.entity == "NOZZLE DROPLET GENERATOR":
                # dafd_adapter.size_droplet_generator(component, constraints)
                print("Skipping calling DAFD since its crashing everything right now")
            elif component.entity == "PORT":
                component.params.set_param("portRadius", 2000)
