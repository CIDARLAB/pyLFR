from lfr.netlistgenerator.v2 import mappingoption
from lfr.fig.fluidinteractiongraph import FluidInteractionGraph
from parchmint.device import Device
from lfr.compiler.module import Module
from lfr.netlistgenerator.namegenerator import NameGenerator
from lfr.netlistgenerator.mappinglibrary import PrimitiveType
from typing import Dict, List
from lfr.netlistgenerator.explicitmapping import ExplicitMapping, ExplicitMappingType
from lfr.netlistgenerator.v2.constructionnode import ConstructionNode
from networkx import nx
from pymint.mintdevice import MINTDevice


class ConstructionGraph(nx.DiGraph):

    def __init__(self, data=None, val=None, **attr) -> None:
        super(ConstructionGraph, self).__init__()
        self._construction_nodes = dict()

    @property
    def construction_nodes(self) -> List[ConstructionNode]:
        return self._construction_nodes

    def add_construction_node(self, node: ConstructionNode) -> None:
        self._construction_nodes[node.id] = node
        self.add_node(node.id)

    def override_mappings(self, mappings: List[ExplicitMapping]) -> None:
        for mapping in mappings:
            # First identify the type of the mapping
            if mapping.type is ExplicitMappingType.FLUID_INTERACTION:
                # TODO - Identify which construction nodes need to be overridden for this
                # TODO - Figure out if the mapping will be valid in terms of inputs and
                # outputs
                print("Implement mapping override for fluid interaction")
                pass
            elif mapping.type is ExplicitMappingType.STORAGE:
                # TODO - Identify which construction nodes need to be overrridden
                # TODO - Since the explicit mapping required for this might vary a bit
                # we need to figure out how multiple mappings can work with storage
                print("Implement mapping override for storage")
                pass
            elif mapping.type is ExplicitMappingType.NETWORK:
                # TODO - Identify which subgraph need to be replaced here
                print("Implement mapping override for network")
                pass

    def generate_components(self, name_generator: NameGenerator, device: MINTDevice) -> None:
        for cn in [v for k, v in self._construction_nodes.items()]:
            if len(cn.mapping_options) > 1:
                # TODO - update for combinatorial design space exploration
                raise Exception("Does not support Combinatorial design exploration")
            elif len(cn.mapping_options) == 1:
                mapping_option = cn.mapping_options[0]
                if mapping_option.primitive.type is PrimitiveType.COMPONENT:
                    # Create a new component here based on the primitive technology
                    # and the name generator
                    # Then merge with the larger device
                    # Save the copy of subgraph view of the netlist in the construction node
                    component_to_add = mapping_option.primitive.get_default_component(name_generator)
                    device.add_component(component_to_add)
                elif mapping_option.primitive.type is PrimitiveType.NETLIST:
                    netlist = mapping_option.primitive.get_default_netlist(name_generator)
                    device.merge_netlist(netlist)
            else:
                print("No mappings found to the current construction node {0}".format(cn))

    def generate_edges(self, fig: FluidInteractionGraph) -> None:
        # Look at the mapping options for each of the constructionnodes,
        # Figure out which other subgraphs are they connected to based on the original fig
        # connectivity make the constructionnode based on which other cn subgraphs they are
        # connected to

        # Step 1 - create a map for each fig element and see what all cn's they're present in
        # (this will account for double coverage cases too)
        # Step 2 - Now that we know the mapping, go through each connection in the fig,
        # Step 3 - if both source and target are in the same cn, skip, create an edge between
        # the cn's

        # Step 1 - create a map for each fig element and see what all cn's they're present in
        # (this will account for double coverage cases too)

        # TODO - For combinatorial design space, figure out what to do with this
        fig_nodes_cn_reverse_map: Dict[str, List] = dict()
        for cn in self.construction_nodes:
            # TODO - Assumption here is that there is only 1 mapping option, else its a
            # combinatorial design space
            assert(len(cn.mapping_options) == 1)
            for mapping_option in cn.mapping_options:
                for node_id in mapping_option.fig_subgraph.nodes:
                    if node_id in fig_nodes_cn_reverse_map.keys():
                        fig_nodes_cn_reverse_map[node_id].append(node_id)
                    else:
                        fig_nodes_cn_reverse_map[node_id] = []
                        fig_nodes_cn_reverse_map[node_id].append(node_id)

        # Step 2 - Now that we know the mapping, go through each connection in the fig,
        for edge in fig.edges:
            src = edge[0]
            tar = edge[1]
            if src not in fig_nodes_cn_reverse_map.keys() or tar not in fig_nodes_cn_reverse_map.keys():
                raise Exception("Src or Tar not in the construction graph, under coverage issue")
            else:
                # TODO - When the asserts fail, its an overcoverage issue, decide what needs to be done here
                src_cn = fig_nodes_cn_reverse_map[src]
                assert(len(src_cn) == 1)
                tar_cn = fig_nodes_cn_reverse_map[tar]
                assert(len(tar_cn) == 1)

                # Step 3 - now check to see if both are in the same cn or not, if they're not create an cn_edge
                # TODO - implement list search/edge creation incase there are multiple cn's associated
                if src_cn[0] == tar_cn[0]:
                    self.add_edge(src_cn[0].id, tar_cn[0].id)

    def generate_flow_cn_edges(self, module: Module) -> None:
        # TODO - Figure out what we need for the generating the edges here
        print("Impement ConstructionGrpah:generate_flow_cn_edges method stub ")
        pass

    def generate_control_cn_edges(self, module: Module) -> None:
        # TODO - Figure what we need for the generating the edges here
        print("Impement ConstructionGrpah:generate_control_cn_edges method stub ")
        pass
