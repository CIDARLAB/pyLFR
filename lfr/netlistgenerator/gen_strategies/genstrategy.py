from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from pymint.mintlayer import MINTLayerType

from lfr.fig.fluidinteractiongraph import FluidInteractionGraph

if TYPE_CHECKING:
    from lfr.netlistgenerator.constructiongraph import ConstructionGraph

from lfr.netlistgenerator.connectingoption import ConnectingOption
from typing import List

from pymint.mintdevice import MINTDevice
from pymint.mintnode import MINTNode
from parchmint import Target


class GenStrategy:
    def __init__(self, fig: FluidInteractionGraph) -> None:
        self._fig: FluidInteractionGraph = fig
        self._fig_netlist_map: Dict[str, str] = {}

    def reduce_mapping_options(self) -> None:
        # Dummy strategy
        # for cn in self._construction_graph.construction_nodes:
        #     # print(len(cn.mapping_options))
        #     # clean this
        #     # Remove the extra mappings
        #     print(
        #         "Reducing mapping options for Construction node: {} from {} to {}"
        #         .format(cn.ID, len(cn.mapping_options), 1),
        #     )
        #     if len(cn.mapping_options) > 1:
        #         for option in cn.mapping_options:
        #             print("     -{}".format(option.primitive.mint))
        #     del cn.mapping_options[1 : len(cn.mapping_options)]
        #     # print("... -> {}".format(len(cn.mapping_options)))

        # print("Printing all final mapping options:")
        # for cn in self._construction_graph.construction_nodes:
        #     print("Construction node: {}".format(cn.ID))
        #     print("Options: ")

        #     for mapping_option in cn.mapping_options:
        #         print(mapping_option.primitive.mint)
        pass

    def generate_flow_network(self, fig_subgraph_view) -> MINTDevice:
        # TODO - For now just assume that the networks basically are a bunch
        # of nodes with nets/channels connecting them
        ret = MINTDevice("flow_network_temp")
        mint_layer = ret.create_mint_layer("0", "0", 0, MINTLayerType.FLOW)
        for node in fig_subgraph_view.nodes:
            n = MINTNode("node_{}".format(node), mint_layer)
            ret.device.add_component(n.component)
            self._store_fig_netlist_name(node, n.component.ID)

        i = 1
        for node in fig_subgraph_view.nodes:
            # Create the channel between these nodes
            channel_name = "c_{}".format(i)
            i += 1
            params = {}
            params["channelWidth"] = 400
            source = Target("node_{}".format(node))
            sinks = []

            # Add all the outgoing edges
            for edge in fig_subgraph_view.out_edges(node):
                tar = edge[1]
                if tar not in fig_subgraph_view.nodes:
                    # We skip because this might be a weird edge that we
                    # were not supposed to have in this network
                    continue

                sinks.append(Target("node_{}".format(tar)))

            ret.create_mint_connection(
                channel_name, "CHANNEL", params, source, sinks, "0"
            )

        return ret

    def _store_fig_netlist_name(self, fig_id: str, netlist_id: str) -> None:
        self._fig_netlist_map[fig_id] = netlist_id

    def _get_fig_netlist_name(self, fig_id: str) -> str:
        return self._fig_netlist_map[fig_id]

    def generate_input_connectingoptions(self, subgraph_view) -> List[ConnectingOption]:
        subgraph_inputs = []
        for node in list(subgraph_view.nodes):
            if len(subgraph_view.in_edges(node)) == 0:
                subgraph_inputs.append(
                    ConnectingOption(self._get_fig_netlist_name(node))
                )

        return subgraph_inputs

    def generate_output_connectingoptions(
        self, subgraph_view
    ) -> List[ConnectingOption]:
        subgraph_outputs = []
        for node in list(subgraph_view.nodes):
            if len(subgraph_view.out_edges(node)) == 0:
                subgraph_outputs.append(
                    ConnectingOption(self._get_fig_netlist_name(node))
                )

        return subgraph_outputs

    @staticmethod
    def generate_carrier_connectingoptions(subgraph_view) -> List[ConnectingOption]:
        return []

    @staticmethod
    def generate_loading_connectingoptions(subgraph_view) -> List[ConnectingOption]:
        return []

    def size_netlist(self, device: MINTDevice) -> None:
        raise NotImplementedError()

    def prune_variants(self, variants: List[ConstructionGraph]) -> None:
        for variant in variants:
            if variant.is_fig_fully_covered() is not True:
                print("Removing variant (Construction Graph): {}".format(variant.ID))
                variants.remove(variant)
