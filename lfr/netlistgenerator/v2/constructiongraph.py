from parchmint.device import Device
from lfr.compiler.module import Module
from lfr.netlistgenerator.namegenerator import NameGenerator
from lfr.netlistgenerator.mappinglibrary import PrimitiveType
from lfr.fig.interaction import InteractionType
from typing import List
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
                pass
            elif mapping.type is ExplicitMappingType.STORAGE:
                # TODO - Identify which construction nodes need to be overrridden
                # TODO - Since the explicit mapping required for this might vary a bit
                # we need to figure out how multiple mappings can work with storage
                pass
            elif mapping.type is ExplicitMappingType.NETWORK:
                # TODO - Identify which subgraph need to be replaced here
                pass

    def generate_components(self, name_generator: NameGenerator, device: MINTDevice) -> None:
        for cn in [v for k, v in self._construction_nodes.items()]:
            if len(cn.mapping_options) > 1:
                raise Exception("Does not support Combinatorial design exploration")
            elif len(cn.mapping_options) == 1:
                # TODO - Do the work that needs to be done
                mapping_option = cn.mapping_options[0]
                if mapping_option.primitive.type is PrimitiveType.COMPONENT:
                    # Create a new component here based on the primitive technology
                    # and the name generator
                    # Then merge with the larger device
                    # Save the copy of subgraph view of the netlist in the construction node
                    component_to_add = mapping_option.primitive.get_default_component(name_generator)
                    device.add_component(component_to_add)
                elif mapping_option.primitive.type is PrimitiveType.NETLIST:
                    # TODO - Do something else
                    netlist = mapping_option.primitive.get_default_netlist(name_generator)
                    device.merge_netlist(netlist)
            else:
                print("No mappings found to the current construction node {0}".format(cn))

    def generate_flow_cn_edges(self, module: Module) -> None:
        # TODO - Figure out what we need for the generating the edges here
        pass

    def generate_control_cn_edges(self, module: Module) -> None:
        # TODO - Figure what we need for the generating the edges here
        pass
