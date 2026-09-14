import re
from typing import List, Optional

from parchmint import Component, Layer, Params

from lfr.netlistgenerator.connectingoption import ConnectingOption
from lfr.netlistgenerator.namegenerator import NameGenerator
from lfr.netlistgenerator.primitive import ProceduralPrimitive


def _fig_id(node) -> str:
    return str(getattr(node, "ID", node))


def _natural_key(node):
    parts = re.split(r"(\d+)", _fig_id(node))
    return tuple(int(p) if p.isdigit() else p for p in parts)


def _boundary_nodes(subgraph, *, sinks: bool) -> list:
    if subgraph is None:
        return []
    nodes = []
    for node in subgraph.nodes:
        deg = (
            len(list(subgraph.out_edges(node)))
            if sinks
            else len(list(subgraph.in_edges(node)))
        )
        if deg == 0:
            nodes.append(node)
    nodes.sort(key=_natural_key)
    return nodes


def _tree_options(nodes) -> List[ConnectingOption]:
    """3DuF YTREE: port 1 is the trunk; leaves are 2 .. n+1."""
    if not nodes:
        return []
    if len(nodes) == 1:
        n = nodes[0]
        return [ConnectingOption(None, ["1"], fig_nodes=[_fig_id(n)])]
    return [
        ConnectingOption(None, [str(i + 2)], fig_nodes=[_fig_id(n)])
        for i, n in enumerate(nodes)
    ]


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
        return _tree_options(_boundary_nodes(subgraph, sinks=False))

    def export_outputs(self, subgraph) -> List[ConnectingOption]:
        return _tree_options(_boundary_nodes(subgraph, sinks=True))

    def export_loadings(self, subgraph) -> Optional[List[ConnectingOption]]:
        return None

    def export_carriers(self, subgraph) -> Optional[List[ConnectingOption]]:
        return None

    def get_procedural_component(
        self, name_gen: NameGenerator, layer: Layer, subgraph
    ) -> Component:
        name = name_gen.generate_name(self.mint)
        params = {}
        # Calculate param values based on the subgraph
        params["flowChannelWidth"] = 5
        params["spacing"] = 5

        n_in = 0
        n_out = 0
        for node in subgraph.nodes:
            if len(list(subgraph.in_edges(node))) == 0:
                n_in += 1
            if len(list(subgraph.out_edges(node))) == 0:
                n_out += 1
        n_in = max(n_in, 1)
        n_out = max(n_out, 1)
        # 3DuF YTREE: port 1 is the trunk, 2..leafs+1 are leaves.
        params["in"] = float(n_in)
        params["out"] = float(n_out)
        params["leafs"] = float(max(n_in, n_out))
        params["width"] = 5
        params["height"] = 5
        params["stageLength"] = 5
        mc = Component(
            ID=name, name=name, entity=self.mint, params=Params(params), layers=[layer]
        )
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
