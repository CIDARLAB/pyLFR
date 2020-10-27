from lfr.netlistgenerator.v2.connectingoption import ConnectingOption
from typing import List, overload
from pymint.mintdevice import MINTDevice
from pymint.mintnode import MINTNode
from pymint.minttarget import MINTTarget
from lfr.netlistgenerator.v2.constructiongraph import ConstructionGraph


class GenStrategy:

    def __init__(self, construction_graph: ConstructionGraph) -> None:
        self._construction_graph: ConstructionGraph = construction_graph

    @overload
    def reduce_mapping_options(self) -> None:
        pass

    @overload
    def generate_flow_network(self, fig_subgraph_view) -> MINTDevice:
        # TODO - For now just assume that the networks basically are a bunch
        # of nodes with nets/channels connecting them
        ret = MINTDevice("flow_network_temp")
        for node in fig_subgraph_view.nodes:
            n = MINTNode("node_{}".format(node))
            ret.add_component(n)

        i = 1
        for node in fig_subgraph_view.nodes:
            # Create the channel between these nodes
            channel_name = "c_{}".format(i)
            i += 1
            params = dict()
            params["channelWidth"] = 400
            source = MINTTarget("node_{}".format(node))
            sinks = []

            # Add all the outgoing edges
            for edge in node.out_edges:
                tar = edge[1]
                if tar not in fig_subgraph_view.nodes:
                    # We skip because this might be a weird edge that we were not supposed
                    # to have in this network
                    continue

                sinks.append(MINTTarget("node_{}".format(tar)))

            ret.addConnection(channel_name, "CHANNEL",  params, source, sinks)

        return ret

    def generate_input_connectingoptions(self, subgraph_view) -> List[ConnectingOption]:
        subgraph_inputs = []
        for node in list(subgraph_view.nodes):
            if len(subgraph_view.in_edges(node)):
                subgraph_inputs.append(node)

        return subgraph_inputs

    def generate_output_connectingoptions(self, subgraph_view) -> List[ConnectingOption]:
        subgraph_outputs = []
        for node in list(subgraph_view.nodes):
            if len(subgraph_view.out_edges(node)):
                subgraph_outputs.append(node)
        return subgraph_outputs

    @overload
    def generate_carrier_connectingoptions(self, subgraph_view) -> List[ConnectingOption]:
        pass

    @overload
    def generate_loading_connectingoptions(self, subgraph_view) -> List[ConnectingOption]:
        pass
