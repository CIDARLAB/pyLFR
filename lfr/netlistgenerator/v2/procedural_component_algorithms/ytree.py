from typing import List, Optional

from pymint import MINTComponent, MINTLayer

from lfr.netlistgenerator.namegenerator import NameGenerator
from lfr.netlistgenerator.primitive import ProceduralPrimitive
from lfr.netlistgenerator.v2.connectingoption import ConnectingOption


class YTREE(ProceduralPrimitive):
    def __init__(self) -> None:
        super().__init__(
            mint="YTREE",
            match_string="",
            is_storage=False,
            has_storage_control=False,
            functional_input_params=None,
            output_params=None,
            user_defined_params=None,
            default_netlist=None,
        )

    def export_inputs(self, subgraph) -> List[ConnectingOption]:
        input_nodes = []
        for node in subgraph.nodes:
            in_dim = len(list(subgraph.in_edges(node)))
            if in_dim == 0:
                input_nodes.append(node)

        # TODO create the connecting options based on in dim and out dim
        if len(input_nodes) == 1:
            # This is the normal numbering of the connecting options
            return [ConnectingOption(None, ["1"])]
        else:
            # This is the reverse numbering of the connecting options
            return [
                ConnectingOption(None, [str(i)]) for i in range(2, len(input_nodes) + 2)
            ]

    def export_outputs(self, subgraph) -> List[ConnectingOption]:
        output_nodes = []
        for node in subgraph.nodes:
            out_dim = len(list(subgraph.out_edges(node)))
            if out_dim == 0:
                output_nodes.append(node)

        # TODO create the connecting options based on in dim and out dim
        if len(output_nodes) == 1:
            # This is the reverse numbering of the connecting options
            return [ConnectingOption(None, ["1"])]
        else:
            # This is the normal numbering of the connecting options
            return [
                ConnectingOption(None, [str(i)])
                for i in range(2, len(output_nodes) + 2)
            ]

    def export_loadings(self, subgraph) -> Optional[List[ConnectingOption]]:
        return None

    def export_carriers(self, subgraph) -> Optional[List[ConnectingOption]]:
        return None

    def get_procedural_component(
        self, name_gen: NameGenerator, layer: MINTLayer, subgraph
    ) -> MINTComponent:
        name = name_gen.generate_name(self.mint)
        params = {}
        # Calculate param values based on the subgraph
        params["flowChannelWidth"] = 5
        params["spacing"] = 5

        # Get number of inputs or outputs
        # for node in subgraph.nodes:

        params["leafs"] = 5
        params["width"] = 5
        params["height"] = 5
        params["stageLength"] = 5
        mc = MINTComponent(name, self.mint, params, [layer])
        return mc

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
