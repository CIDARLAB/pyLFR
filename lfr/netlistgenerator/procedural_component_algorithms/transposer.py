from typing import List

from lfr.netlistgenerator.connectingoption import ConnectingOption
from lfr.netlistgenerator.primitive import ProceduralPrimitive


class TRANSPOSER(ProceduralPrimitive):
    def __init__(self) -> None:
        super().__init__(
            mint="TRANSPOSER",
            is_storage=False,
            has_storage_control=False,
            default_netlist=None,
        )

    def generate_input_connectingoptions(self, subgraph_view) -> List[ConnectingOption]:
        """Generates a list of connection options that represent where the inputs can
        be connected to the primitive

        Args:
            subgraph_view (networkx.Graph.subgraph): A subgraph view of the Fluid Interaction Graph

        Raises:
            NotImplementedError: Raised when its not implemented

        Returns:
            List[ConnectingOption]: List of options where we can attach connections
        """
        raise NotImplementedError()

    def generate_output_connectingoptions(
        self, subgraph_view
    ) -> List[ConnectingOption]:
        """Generates a list of connection options that represent where the outputs can
        be connected to the primitive

        Args:
            subgraph_view (networkx.Graph.subgraph): A subgraph view of the Fluid Interaction Graph


        Raises:
            NotImplementedError: Raised when its not implemented

        Returns:
            List[ConnectingOption]: List of options where we can attach connections
        """
        raise NotImplementedError()

    def generate_carrier_connectingoptions(
        self, subgraph_view
    ) -> List[ConnectingOption]:
        """Generates a list of connection options that represent where the carrier inputs can
        be connected to the primitive

        Args:
            subgraph_view (networkx.Graph.subgraph): A subgraph view of the Fluid Interaction Graph

        Raises:
            NotImplementedError: Raised when its not implemented

        Returns:
            List[ConnectingOption]: List of options where we can attach connections
        """
        raise NotImplementedError()

    def generate_loading_connectingoptions(
        self, subgraph_view
    ) -> List[ConnectingOption]:
        """Generates a list of connection options that represent where the loading inputs can
        be connected to the primitive

        Args:
            subgraph_view (networkx.Graph.subgraph): A subgraph view of the Fluid Interaction Graph

        Raises:
            NotImplementedError: Raised when its not implemented

        Returns:
            List[ConnectingOption]: List of options where we can attach connections
        """
        raise NotImplementedError()
