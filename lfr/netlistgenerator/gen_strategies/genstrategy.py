from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from pymint.mintlayer import MINTLayerType

from lfr.fig.fluidinteractiongraph import FluidInteractionGraph

if TYPE_CHECKING:
    from lfr.netlistgenerator.constructiongraph import ConstructionGraph

from typing import List

from parchmint import Target
from pymint.mintdevice import MINTDevice
from pymint.mintnode import MINTNode

from lfr.netlistgenerator.connectingoption import ConnectingOption


class GenStrategy:
    def __init__(self, name: str, fig: FluidInteractionGraph) -> None:
        self._name: str = name
        self._fig: FluidInteractionGraph = fig

    def validate_construction_graph_flow(
        self, construction_graph: ConstructionGraph
    ) -> bool:
        """
        Validate the construction graph against a set of rules

        TODO - Future version of this should use a rule based grammar
        like Eugene but for topologically sorted FIGs where we
        figure out where the outputs of a certain flow network
        can be connected to the inputs of another flow network
        (Needs to be put in theorem form).

        Args:
            construction_graph (ConstructionGraph): Construction graph to validate

        Returns:
            bool: True if the construction graph is valid
        """
        raise NotImplementedError()

    def reduce_mapping_options(self) -> None:
        """
        Reduce the mapping options for the construction graph

        TODO - In the future go through the options by looking at Rama
        like apps that can be used for pruning technologies based on
        the physics parameters.

        Raises:
            NotImplementedError: If the method is not implemented
        """
        raise NotImplementedError()

    def generate_flow_network(self) -> None:
        """Generate the flow flow network mappings

        TODO - Use this to sort through the correct kinds of network primitives
        to use for the flow-flow networks
        """
        raise NotImplementedError()

    def generate_input_connectingoptions(self):
        """Unsure if this is necessary in the future with the new architecture

        Raises:
            NotImplementedError: Raises if the method is not implemented
        """
        raise NotImplementedError()

    def generate_output_connectingoptions(self):
        """Unsure if this is necessary in the future with the new architecture

        Raises:
            NotImplementedError: Raises if the method is not implemented
        """
        raise NotImplementedError()

    @staticmethod
    def generate_carrier_connectingoptions():
        """
        Generate the connecting options for the carrier networks.

        TODO - In the future version, go through the connectivity of the flow network,
        compute what options would need to be pipelined and then optimize the carrier
        network to have the least number of carrier inputs and wastes.
        """
        return []

    @staticmethod
    def generate_loading_connectingoptions():
        """
        Generate the connecting options for the loading networks.

        TODO - In the future version, go through the connectivity of the flow network,
        compute what options would need to be pipelined and then optimize the loading
        network to have the least number of carrier inputs and wastes.

        Args:
            subgraph_view (_type_): _description_

        Returns:
            List[ConnectingOption]: _description_
        """
        raise NotImplementedError()

    def size_netlist(self, device: MINTDevice) -> None:
        raise NotImplementedError()

    def prune_variants(self, variants: List[ConstructionGraph]) -> None:
        for variant in variants:
            if variant.is_fig_fully_covered() is not True:
                print(f"Removing variant (Construction Graph): {variant.ID}")
                variants.remove(variant)
