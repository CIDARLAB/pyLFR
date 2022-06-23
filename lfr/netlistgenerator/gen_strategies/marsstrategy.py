from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from pymint.mintlayer import MINTLayerType

from lfr.fig.fluidinteractiongraph import FluidInteractionGraph
from lfr.netlistgenerator.constructiongraph.constructionnode import \
    ConstructionNode
from lfr.netlistgenerator.dafdadapter import DAFDAdapter
from lfr.netlistgenerator.gen_strategies.genstrategy import GenStrategy

if TYPE_CHECKING:
    from lfr.netlistgenerator.constructiongraph.constructiongraph import (
        ConstructionGraph,
    )

from typing import List

from parchmint import Target
from pymint.mintdevice import MINTDevice
from pymint.mintnode import MINTNode

from lfr.netlistgenerator.connectingoption import ConnectingOption


class MarsStrategy(GenStrategy):
    def __init__(self, fig: FluidInteractionGraph) -> None:
        self._fig: FluidInteractionGraph = fig
        self._fig_netlist_map: Dict[str, str] = dict()

    def reduce_mapping_options(self) -> None:
        # Dummy strategy
        # for fignode_id in self._fig.nodes:
        #     fignode = self._fig.get_fignode(fignode_id)

        #     if ConstructionNode(fignode_id).is_explictly_mapped:
        #         pass
        #     else:
        #         if isinstance(fignode, Interaction):
        #             cn = self._construction_graph.get_fignode_cn(fignode)

        #             del cn.mapping_options[1 : len(cn.mapping_options)]

        # for cn in self._construction_graph.construction_nodes:
        #     # print(len(cn.mapping_options))
        #     # clean this
        #     # Remove the extra mappings
        #     print(
        #         "Reducing mapping options for Construction node: {} from {} to {}".format(
        #             cn.id, len(cn.mapping_options), 1
        #         ),
        #     )
        #     if len(cn.mapping_options) > 1:
        #         for option in cn.mapping_options:
        #             print("     -{}".format(option.primitive.mint))
        #     del cn.mapping_options[1 : len(cn.mapping_options)]
        #     # print("... -> {}".format(len(cn.mapping_options)))

        # print("Printing all final mapping options:")
        # for cn in self._construction_graph.construction_nodes:
        #     print("Construction node: {}".format(cn.id))
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
            node = MINTNode("node_{}".format(str(node)), mint_layer)
            ret.device.add_component(node.component)
            # TODO - Add method to store NODES
            self._store_fig_netlist_name(str(node), node.component.ID)

        i = 1
        for node in fig_subgraph_view.nodes:
            # Create the channel between these nodes
            channel_name = "c_{}".format(i)
            i += 1
            params = dict()
            params["channelWidth"] = 400
            source = Target("node_{}".format(node))
            sinks = []

            # Add all the outgoing edges
            for edge in fig_subgraph_view.out_edges(node):
                tar = edge[1]
                if tar not in fig_subgraph_view.nodes:
                    # We skip because this might be a weird edge that we were not supposed
                    # to have in this network
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

    def generate_carrier_connectingoptions(
        self, subgraph_view
    ) -> List[ConnectingOption]:
        return []

    def generate_loading_connectingoptions(
        self, subgraph_view
    ) -> List[ConnectingOption]:
        return []

    def size_netlist(self, device: MINTDevice) -> None:
        """
        Sizes the device based on either lookup tables, inverse design algorithms, etc.
        """
        # dafd_adapter = DAFDAdapter(device)
        # # Default size for PORT is 2000 um
        # for component in device.components:
        #     constraints = self._construction_graph.get_component_cn(
        #         component
        #     ).constraints
        #     if component.entity == "NOZZLE DROPLET GENERATOR":
        #         # dafd_adapter.size_droplet_generator(component, constraints)
        #         print("Skipping calling DAFD since its crashing everything right now")
        #     elif component.entity == "PORT":
        #         component.params.set_param("portRadius", 2000)
        pass
