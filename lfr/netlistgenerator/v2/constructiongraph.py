from pymint.minttarget import MINTTarget
from lfr.fig.fluidinteractiongraph import FluidInteractionGraph
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
        self._construction_nodes: Dict[str, ConstructionNode] = dict()
        self._component_refs: Dict[str, List[str]] = dict()

    @property
    def construction_nodes(self) -> List[ConstructionNode]:
        return [v for k, v in self._construction_nodes.items()]

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

    def construct_components(self, name_generator: NameGenerator, device: MINTDevice) -> None:
        for cn in self.construction_nodes:
            if len(cn.mapping_options) > 1:
                # TODO - update for combinatorial design space exploration
                raise Exception("Does not support Combinatorial design exploration")
            elif len(cn.mapping_options) == 1:
                cn.load_connection_options()
                mapping_option = cn.mapping_options[0]
                if mapping_option.primitive.type is PrimitiveType.COMPONENT:
                    # Create a new component here based on the primitive technology
                    # and the name generator
                    # Then merge with the larger device
                    # Save the copy of subgraph view of the netlist in the construction node
                    component_to_add = mapping_option.primitive.get_default_component(name_generator)
                    device.add_component(component_to_add)
                    self._component_refs[cn.id] = [component_to_add.ID]
                    # for connecting_option in cn
                    # TODO - save the subgraph view reference
                elif mapping_option.primitive.type is PrimitiveType.NETLIST:
                    netlist = mapping_option.primitive.get_default_netlist(cn.id, name_generator)
                    self._component_refs[cn.id] = [component.ID for component in netlist.components]
                    device.merge_netlist(netlist)
                    # TODO - Save the subgraph view reference
            else:
                print("No mappings found to the current construction node {0}".format(cn))

    def construct_connections(self, name_generator: NameGenerator, device: MINTDevice) -> None:
        # TODO - Modify this to enable mapping options for edges

        # # Step 1 - Loop through each of the edges
        # for edge in self.edges:
        #     src = self._construction_nodes[edge[0]]
        #     tar = self._construction_nodes[edge[1]]

        # Step 2 - Get the output requirement from src mapping option and the input mapping
        # option and make a simple channel between them (I guess no parameters right now)
        # TODO - Modify this based on what mapping option is enabled here later on

        # src.load_connection_options()
        # tar.load_connection_options()

        # Step 3 - Loop through all the nodes and start filling out this input/output requirements
        # This exploration could be using the reverse DFS traversal this way we can probably fill out
        # the entire set of flows that way.
        # -----------------------
        # TODO - This could probably be converted into network flow problems. Since this an extension
        # of bipartitie matching at every step, I think that can be converted into a max flow problem
        # However, what needs to be determined is what factor becomes the capacity, weight, etc.
        # The only constraints that are known is that everything will have infinite capacity,
        # Technically every node might be an edge and every edge might be a node, that way we can
        # take the input / output capacities and treat them as. This needs to eb thought through a little

        for cn_id in self.nodes:
            # Step 3.1 - Check to see if there are as many input options are there are incoming edges
            # if its n->n or n->1, it'll be easy otherwise we need to figure out something else
            in_neighbours = self.in_edges(cn_id)
            cn = self._construction_nodes[cn_id]

            if len(in_neighbours) == 0:
                continue

            # This 1->1 condition
            # TODO - deal with n->n 1->n , etc. later
            assert(len(in_neighbours) == 1)
            src_id = list(in_neighbours)[0][0]
            src = self._construction_nodes[src_id]
            start_point = src.output_options[0]

            if start_point.component_name is None:
                # This means a single component was mapped here
                src_component_name = self._component_refs[src_id][0]
            else:
                src_component_name = name_generator.get_cn_name(src_id, start_point.component_name)

            end_point = cn.input_options[0]

            if end_point.component_name is None:
                # This means a single component was mapped here
                tar_component_name = self._component_refs[cn.id][0]
            else:
                tar_component_name = name_generator.get_cn_name(cn.id, end_point.component_name)

            print("Generating the channel - Source: {0} {2}, Target: {1} {3}".format(src_component_name, tar_component_name, start_point.component_port, end_point.component_port))

            # TODO - Change how we retrieve the technology type for the channel
            tech_string = "CHANNEL"
            # channel_name = name_generator.generate_name(tech_string)

            # TODO - Figure out how to hande a scenario where this isn't ture
            assert(len(end_point.component_port) == 1)
            for component_port in start_point.component_port:
                channel_name = name_generator.generate_name(tech_string)
                source = MINTTarget(src_component_name, component_port)
                sink = MINTTarget(tar_component_name, end_point.component_port[0])
                # TODO - Figure out how to make this layer generate automatically
                device.addConnection(channel_name, tech_string, dict(), source, [sink], "0")

            # TODO - Once we are done creating a path, we need to delete the start and end point options
            # from their respective construction nodes.
            print("Updated the connectionoptions in {} - Removing {}".format(src, start_point))
            src.output_options.remove(start_point)

            print("Updated the connectionoptions in {} - Removing {}".format(cn, end_point))
            cn.input_options.remove(end_point)

        # TODO - I need to figure out how to pipeline the loadings/carriers and other things
        pass

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

                        # Make sure there are no repeats here
                        if node_id not in fig_nodes_cn_reverse_map[cn.id]:
                            fig_nodes_cn_reverse_map[node_id].append(cn.id)
                    else:
                        fig_nodes_cn_reverse_map[node_id] = []
                        fig_nodes_cn_reverse_map[node_id].append(cn.id)

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
                if src_cn[0] != tar_cn[0]:
                    self.add_edge(src_cn[0], tar_cn[0])
                else:
                    pass

    def generate_flow_cn_edges(self, module: Module) -> None:
        # TODO - Figure out what we need for the generating the edges here
        print("Impement ConstructionGrpah:generate_flow_cn_edges method stub ")
        pass

    def generate_control_cn_edges(self, module: Module) -> None:
        # TODO - Figure what we need for the generating the edges here
        print("Impement ConstructionGrpah:generate_control_cn_edges method stub ")
        pass
