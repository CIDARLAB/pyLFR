from typing import List, Optional

from parchmint import Component, Layer, Params

from lfr.netlistgenerator.connectingoption import ConnectingOption
from lfr.netlistgenerator.namegenerator import NameGenerator
from lfr.netlistgenerator.primitive import ProceduralPrimitive
from lfr.netlistgenerator.procedural_component_algorithms.ytree import (
    _boundary_nodes,
    _tree_options,
)


class MUX(ProceduralPrimitive):
    """3DuF MUX primitive for ``#MAP "MUX" "assign"``.

    Trunk/leaf numbering matches YTREE: port 1 is the trunk, leaves are
    2 .. leafs+1. Control terminals start at 2+leafs; netlist generation
    attaches Super_MUX-style CONTROL PORTs after the flow netlist is built.
    """

    def __init__(self) -> None:
        super().__init__(
            mint="MUX",
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
        n_in = 0
        n_out = 0
        for node in subgraph.nodes:
            if len(list(subgraph.in_edges(node))) == 0:
                n_in += 1
            if len(list(subgraph.out_edges(node))) == 0:
                n_out += 1
        n_in = max(n_in, 1)
        n_out = max(n_out, 1)
        params = {
            "in": float(n_in),
            "out": float(n_out),
            "leafs": float(max(n_in, n_out)),
            "flowChannelWidth": 600.0,
            "controlChannelWidth": 600.0,
            "leafSpace": 4000.0,
            "width": 1800.0,
            "valveWidthY": 1000.0,
            "length": 1000.0,
            "stageSpace": 6000.0,
            "height": 250.0,
            "componentSpacing": 2000.0,
        }
        return Component(
            ID=name, name=name, entity=self.mint, params=Params(params), layers=[layer]
        )
