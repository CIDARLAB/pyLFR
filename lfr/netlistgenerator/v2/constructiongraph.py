from copy import copy
from typing import Dict, List, Set, Tuple

from networkx import nx
from networkx.algorithms import isomorphism
from networkx.classes.digraph import DiGraph
from networkx.classes.function import subgraph
from pymint.mintcomponent import MINTComponent
from pymint.mintdevice import MINTDevice
from pymint.minttarget import MINTTarget

from lfr.compiler.module import Module
from lfr.fig.fignode import FIGNode
from lfr.fig.fluidinteractiongraph import FluidInteractionGraph
from lfr.netlistgenerator.namegenerator import NameGenerator
from lfr.netlistgenerator.primitive import PrimitiveType, ProceduralPrimitive
from lfr.netlistgenerator.v2.constructionnode import ConstructionNode
from lfr.netlistgenerator.v2.networkmappingoption import (
    NetworkMappingOption, NetworkMappingOptionType)


class ConstructionGraph(nx.DiGraph):
    def __init__(self, data=None, val=None, **attr) -> None:
        super(ConstructionGraph, self).__init__()
        self._construction_nodes: Dict[str, ConstructionNode] = dict()
        # Stores the references for each construction node and component ID's
        self._component_refs: Dict[str, List[str]] = dict()
        self._fixed_edges: List[Tuple[str, str]] = []

    @property
    def construction_nodes(self) -> List[ConstructionNode]:
        return [v for k, v in self._construction_nodes.items()]

    def get_cn(self, id: str) -> ConstructionNode:
        if id in self._construction_nodes.keys():
            return self._construction_nodes[id]
        else:
            raise KeyError()

    def add_construction_node(self, node: ConstructionNode) -> None:
        self._construction_nodes[node.id] = node
        self.add_node(node.id)

    def delete_node(self, id: str) -> None:
        self.remove_node(id)
        del self._construction_nodes[id]

    def construct_components(
        self, name_generator: NameGenerator, device: MINTDevice
    ) -> None:
        # TODO - Figure out a smart way to get the right layer every single time
        layer = device.layers[0]
        for cn in self.construction_nodes:
            if len(cn.mapping_options) > 1:
                # TODO - update for combinatorial design space exploration
                raise Exception("Does not support Combinatorial design exploration")
            elif len(cn.mapping_options) == 1:
                mapping_option = cn.mapping_options[0]

                # TODO - Make sure we skip the mapping option if pass through is enabled
                if isinstance(mapping_option, NetworkMappingOption):
                    if (
                        mapping_option.mapping_type
                        is NetworkMappingOptionType.PASS_THROUGH
                    ):
                        continue
                    elif (
                        mapping_option.mapping_type
                        == NetworkMappingOptionType.COMPONENT_REPLACEMENT
                    ):
                        # Create a new component here based on the primitive technology
                        # and the name generator
                        # Then merge with the larger device
                        # Save the copy of subgraph view of the netlist in the construction node
                        component_to_add = None

                        if (
                            mapping_option.primitive.type == PrimitiveType.PROCEDURAL
                            or isinstance(mapping_option.primitive, ProceduralPrimitive)
                        ):
                            component_to_add = (
                                mapping_option.primitive.get_procedural_component(
                                    name_generator, layer, mapping_option.fig_subgraph
                                )
                            )
                        else:
                            component_to_add = (
                                mapping_option.primitive.get_default_component(
                                    name_generator, layer
                                )
                            )

                        device.add_component(component_to_add)
                        self._component_refs[cn.id] = [component_to_add.ID]
                        # for connecting_option in cn
                        # TODO - save the subgraph view reference

                elif mapping_option.primitive.type is PrimitiveType.COMPONENT:
                    # Create a new component here based on the primitive technology
                    # and the name generator
                    # Then merge with the larger device
                    # Save the copy of subgraph view of the netlist in the construction node
                    component_to_add = mapping_option.primitive.get_default_component(
                        name_generator, layer
                    )
                    device.add_component(component_to_add)
                    self._component_refs[cn.id] = [component_to_add.ID]
                    # for connecting_option in cn
                    # TODO - save the subgraph view reference
                elif mapping_option.primitive.type is PrimitiveType.NETLIST:
                    netlist = mapping_option.primitive.get_default_netlist(
                        cn.id, name_generator
                    )
                    self._component_refs[cn.id] = [
                        component.ID for component in netlist.components
                    ]
                    device.merge_netlist(netlist)
                    # print(device.components)
                    # TODO - Save the subgraph view reference
                elif mapping_option.primitive.type is PrimitiveType.PROCEDURAL:
                    netlist = mapping_option.primitive.get_default_netlist(
                        cn.id, name_generator
                    )
                    self._component_refs[cn.id] = [
                        component.ID for component in netlist.components
                    ]
                    device.merge_netlist(netlist)
                else:
                    raise Exception(
                        "Does not work with any known option for primitive type"
                    )

                cn.load_connection_options()

            else:
                print(
                    "No mappings found to the current construction node {0}".format(cn)
                )

    def get_fignode_cn(self, fig_node: FIGNode) -> ConstructionNode:
        for cn in self._construction_nodes.values():
            for mapping_option in cn.mapping_options:
                if fig_node.id in mapping_option.fig_subgraph.nodes:
                    return cn

        raise Exception(
            "Could not find construction node with an active mappingoption that covers FIG node: {}".format(
                fig_node.id
            )
        )

    def split_cn(
        self,
        cn_to_split: ConstructionNode,
        split_groups: List[Set[str]],
        fig: FluidInteractionGraph,
    ) -> None:
        """This method splits the construction node into multiple pieces.
        This is driven by the lists of strings holding the FIG node id's.
        It put each list of ID's in the split_groups variable into individual
        construction nodes.

        WARNING ! - Generates CN edges only between the new CN's

        In addition to splitting up the node, the method also creates edges
        between all the nodes based on how the FIG subgraph is connected

        Args:
            cn_to_split (ConstructionNode): Construction node that needs to be split into multiple nodes
            split_groups (List[List[str]]): A list of lists where each list should contain the FIG node IDs that neet to be in differnt nodes
        """
        name = cn_to_split.id
        fig_nodes = []
        for nodes in split_groups:
            fig_nodes.extend(nodes)
        full_subgraph = fig.subgraph(fig_nodes)
        for group_index in range(len(split_groups)):
            split_group = split_groups[group_index]
            fig_subgraph = fig.subgraph(split_group)
            cn = ConstructionNode("{}_split_{}".format(name, group_index))
            # Copy all the mapping options but have a differet fig_subgraph
            for mapping_option in cn_to_split.mapping_options:
                # TODO = Figure out what kind of a network mapping I need to get for this
                mapping_copy = copy(mapping_option)
                mapping_copy.fig_subgraph = fig_subgraph
                cn.add_mapping_option(mapping_option)

            self.add_construction_node(cn)

        # Delete the node now
        self.delete_node(cn_to_split.id)

        # TODO - create connections between the cns based on the figs
        self.generate_edges(full_subgraph)

        raise NotImplementedError()

    def insert_cn(
        self,
        cn_to_insert: ConstructionNode,
        input_cns: List[ConstructionNode],
        output_cns: List[ConstructionNode],
        fig: FluidInteractionGraph,
    ) -> None:
        # Delete all the edges between the input nodes and the output nodes
        for input_cn in input_cns:
            for output_cn in output_cns:
                if self.has_edge(input_cn.id, output_cn.id):
                    self.remove_edge(input_cn.id, output_cn.id)

        # Add the cn
        self.add_construction_node(cn_to_insert)
        # Create the connections between the intermediate cn
        for input_cn in input_cns:
            self.add_edge(input_cn.id, cn_to_insert.id)

        for output_cn in output_cns:
            self.add_edge(cn_to_insert.id, output_cn.id)

    def get_component_cn(self, component: MINTComponent) -> ConstructionNode:
        """Get the Construction Node associated with the given component

        Args:
            component (MINTComponent): The component whose corresponding
            construction node is supposed to be returned

        Raises:
            Exception: If no Construction node is referenced against the
            component

        Returns:
            ConstructionNode: The construction node for which this Component
            was synthesized
        """
        for key, component_list in self._component_refs.items():
            if component.ID in component_list:
                return self.get_cn(key)

        raise Exception(
            "Could not find Construction Node for component: {}".format(component.ID)
        )

    def construct_connections(
        self, name_generator: NameGenerator, device: MINTDevice
    ) -> None:
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

        # We first do the channel creation for the pass throughs so that we don't finish up the input
        # output resources.
        skip_list = []
        for cn_id in self.nodes:
            # Step 3.1 - Check to see if there are as many input options are there are incoming edges
            # if its n->n or n->1, it'll be easy otherwise we need to figure out something else
            in_neighbours = self.in_edges(cn_id)
            cn = self._construction_nodes[cn_id]

            if len(in_neighbours) == 0:
                continue

            # TODO - Go through netlist and then figure out what needs to get done
            # based on the strategy we need to do different things. This is the requirement for when its a
            # FLOW-FLOW-CONSTRUCTION-NODE

            # In this case it needs to treat as an empty netlist because a pass through would just connect the neighbours instead
            # TODO - This will potentially get removed later as we might just want to eliminate the construction node later on
            # if isinstance(cn.mapping_options[0], NetworkMappingOption):
            #     if cn.mapping_options[0].mapping_type is NetworkMappingOptionType.PASS_THROUGH:
            #         # Figure out what the pass through strategy is for this, find the input
            #         # to this cn and link the outputs to the cn
            #         out_neighbours = self.out_edges(cn_id)

            #         # Add to skip list
            #         skip_list.append(cn_id)

            #         # If this is pass through, the in edges should be equal to out edges (I think)
            #         assert(len(in_neighbours) == len(out_neighbours))
            #         # TODO - Figure out what to do if this assert fails
            #         for i in range(len(in_neighbours)):
            #             cn_start_id = list(in_neighbours)[i][0]
            #             cn_end_id = list(out_neighbours)[i][1]

            #             self.__create_passthrough_channel(
            #                 cn_start_id,
            #                 cn_end_id,
            #                 name_generator,
            #                 device
            #             )

            # TODO - Figure out if these conditions require any more thought in terms of implementation
            # elif self._mapping_type is NetworkMappingOptionType.COMPONENT_REPLACEMENT:
            #     # TODO - In this case it needs to be an component with the corresponding
            #     # input and output options loaded into the placeholder primitive
            #     raise Exception("Network Mapping Option Type 'COMPONENT_REPLACEMENT' is not supported for this method")
            #     pass
            # elif self._mapping_type is NetworkMappingOptionType.CHANNEL_NETWORK:
            #     # TODO - This would be a netlist but I'll need to enable terminals/nodes
            #     # where the network will connect through. Most likely we will not need to
            #     # use this

        for cn_id in self.nodes:
            # Skip the round if in skip list
            if cn_id in skip_list:
                continue

            # Step 3.1 - Check to see if there are as many input options are there are incoming edges
            # if its n->n or n->1, it'll be easy otherwise we need to figure out something else
            in_neighbours = self.in_edges(cn_id)
            cn = self._construction_nodes[cn_id]

            # Check if any inputs are left to deal with , skip if there are no more inputs left
            if len(cn.input_options) == 0:
                continue

            if len(in_neighbours) == 0:
                continue
            # This 1->1, n->1 condition
            # TODO - deal with n->n 1->n , etc. later
            for edge in list(in_neighbours):
                src_id = edge[0]

                self.__create_intercn_channel(src_id, name_generator, cn, device)

        # TODO - I need to figure out how to pipeline the loadings/carriers and other things
        pass

    def get_subgraph_cn(self, netlist_subgraph) -> ConstructionNode:
        """Returns the Construction node matching the subgraph

        Args:
            subgraph (subgraph_view): Subgraph to match against

        Returns:
            ConstructionNode: Construction node that contains the
            same subgraph
        """
        subgraph_node_list = list(netlist_subgraph.nodes)
        for cn in list(self._construction_nodes.values()):
            for mapping_option in cn.mapping_options:
                cn_subgraph = mapping_option.fig_subgraph
                cn_subgraph_nodelist = list(cn_subgraph.nodes)
                if (
                    str_lists_equal(subgraph_node_list, cn_subgraph_nodelist)
                    is not True
                ):
                    continue
                graph_matcher = isomorphism.DiGraphMatcher(
                    cn_subgraph, netlist_subgraph
                )
                is_it_isomorphic = graph_matcher.is_isomorphic()
                if is_it_isomorphic:
                    return cn

        raise Exception(
            "Could not find construction node with the same netlist subgraph"
        )

    def __create_passthrough_channel(
        self,
        cn_start_id: str,
        cn_end_id: str,
        name_generator: NameGenerator,
        device: MINTDevice,
    ) -> None:
        cn_start = self._construction_nodes[cn_start_id]
        start_point = cn_start.output_options[0]

        cn_end = self._construction_nodes[cn_end_id]
        end_point = cn_end.input_options[0]

        if start_point.component_name is None:
            # This means a single component was mapped here
            src_component_name = self._component_refs[cn_start_id][0]
        else:
            src_component_name = name_generator.get_cn_name(
                cn_start_id, start_point.component_name
            )

        if end_point.component_name is None:
            # This means a single component was mapped here
            tar_component_name = self._component_refs[cn_end_id][0]
        else:
            tar_component_name = name_generator.get_cn_name(
                cn_end_id, end_point.component_name
            )

        # TODO - Change how we retrieve the technology type for the channel
        tech_string = "CHANNEL"
        # channel_name = name_generator.generate_name(tech_string)

        # TODO - Figure out how to hande a scenario where this isn't ture
        assert len(end_point.component_port) == 1
        if len(start_point.component_port) == 0:
            channel_name = name_generator.generate_name(tech_string)
            source = MINTTarget(src_component_name, None)
            sink = MINTTarget(tar_component_name, end_point.component_port[0])
            device.create_mint_connection(
                channel_name, tech_string, {"channelWidth": 400}, source, [sink], "0"
            )
        else:
            for component_port in start_point.component_port:
                channel_name = name_generator.generate_name(tech_string)
                source = MINTTarget(src_component_name, component_port)
                sink = MINTTarget(tar_component_name, end_point.component_port[0])
                # TODO - Figure out how to make this layer generate automatically
                device.create_mint_connection(
                    channel_name,
                    tech_string,
                    {"channelWidth": 400},
                    source,
                    [sink],
                    "0",
                )

        # TODO - Once we are done creating a path, we need to delete the start and end point options
        # from their respective construction nodes.
        print(
            "Updated the connectionoptions in {} - Removing {}".format(
                cn_start, start_point
            )
        )
        cn_start.output_options.remove(start_point)

        print(
            "Updated the connectionoptions in {} - Removing {}".format(
                cn_end, end_point
            )
        )
        cn_end.input_options.remove(end_point)

    def __create_intercn_channel(
        self,
        src_id: str,
        name_generator: NameGenerator,
        cn: ConstructionNode,
        device: MINTDevice,
    ) -> None:
        src = self._construction_nodes[src_id]
        start_point = src.output_options[0]

        if start_point.component_name is None:
            # This means a single component was mapped here
            src_component_name = self._component_refs[src_id][0]
        else:
            src_component_name = name_generator.get_cn_name(
                src_id, start_point.component_name
            )

        end_point = cn.input_options[0]

        if end_point.component_name is None:
            # This means a single component was mapped here
            tar_component_name = self._component_refs[cn.id][0]
        else:
            tar_component_name = name_generator.get_cn_name(
                cn.id, end_point.component_name
            )

        print(
            "Generating the channel - Source: {0} {2}, Target: {1} {3}".format(
                src_component_name,
                tar_component_name,
                start_point.component_port,
                end_point.component_port,
            )
        )

        # TODO - Change how we retrieve the technology type for the channel
        tech_string = "CHANNEL"
        # channel_name = name_generator.generate_name(tech_string)

        # TODO - Figure out how to hande a scenario where this isn't ture
        assert len(end_point.component_port) == 1
        if len(start_point.component_port) == 0:
            channel_name = name_generator.generate_name(tech_string)
            source = MINTTarget(src_component_name, None)
            sink = MINTTarget(tar_component_name, end_point.component_port[0])
            device.create_mint_connection(
                channel_name, tech_string, {"channelWidth": 400}, source, [sink], "0"
            )
        else:
            for component_port in start_point.component_port:
                channel_name = name_generator.generate_name(tech_string)
                source = MINTTarget(src_component_name, component_port)
                sink = MINTTarget(tar_component_name, end_point.component_port[0])
                # TODO - Figure out how to make this layer generate automatically
                device.create_mint_connection(
                    channel_name,
                    tech_string,
                    {"channelWidth": 400},
                    source,
                    [sink],
                    "0",
                )

        # TODO - Once we are done creating a path, we need to delete the start and end point options
        # from their respective construction nodes.
        print(
            "Updated the connectionoptions in {} - Removing {}".format(src, start_point)
        )
        src.output_options.remove(start_point)

        print("Updated the connectionoptions in {} - Removing {}".format(cn, end_point))
        cn.input_options.remove(end_point)

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
        fig_nodes_cn_reverse_map: Dict[str, List[str]] = dict()
        for cn in self.construction_nodes:
            # TODO - Assumption here is that there is only 1 mapping option, else its a
            # combinatorial design space
            assert len(cn.mapping_options) == 1
            for mapping_option in cn.mapping_options:

                # TODO - Figure out how to not explicity check for this scenario'
                # right now I'm using component replace as a coarse way of ensure
                # no double takes
                # if (
                #     isinstance(mapping_option, NetworkMappingOption)
                #     and mapping_option.mapping_type
                #     == NetworkMappingOptionType.COMPONENT_REPLACEMENT
                #     and cn.is_explictly_mapped
                # ):
                #     print(
                #         "Skipping creating edge creation reverse map entry for Construction None: {}".format(
                #             cn.id
                #         )
                #     )
                #     continue
                for node_id in mapping_option.fig_subgraph.nodes:
                    if node_id in fig_nodes_cn_reverse_map.keys():

                        # Make sure there are no repeats here
                        if cn.id not in fig_nodes_cn_reverse_map[node_id]:
                            fig_nodes_cn_reverse_map[node_id].append(cn.id)
                    else:
                        fig_nodes_cn_reverse_map[node_id] = []
                        fig_nodes_cn_reverse_map[node_id].append(cn.id)

        # Step 1.5 - Handle the overcoverage scenarios, currently we assume that
        # the undercoverage scenarios are only in the case of networkmappings.
        # In the case of networkmappings, we will see that the fig_subgraph on one of
        # the construction node would be the subset of another construction node.

        # Overcoverage scenario list:
        # SCENARIO 1 - Network mapping exists, hence overcoverage. One of the subgraph
        # is a subset of the other
        set_relationship_graph = DiGraph()

        for cn_list in list(fig_nodes_cn_reverse_map.values()):
            over_coverage_scenario_1 = False
            if not len(cn_list) > 1:
                continue
            for i in range(len(cn_list)):
                cn_i_id = cn_list[i]
                cn_i = self.get_cn(cn_i_id)
                cn_i_subset = set(cn_i.mapping_options[0].fig_subgraph.nodes)
                for j in range(i + 1, len(cn_list)):
                    cn_j_id = cn_list[j]
                    cn_j = self.get_cn(cn_j_id)
                    cn_j_subset = set(cn_j.mapping_options[0].fig_subgraph)
                    # Check if one is the subset of the other
                    if cn_i_subset.issubset(cn_j_subset):
                        # cn_j is the superset, add to relationship graph
                        raise Exception("Create Dependency chain")
                        # Generate edge between the cn's
                        over_coverage_scenario_1 = True
                        self.add_edge(cn_i.id, cn_j.id)

                    elif cn_i_subset.issuperset(cn_j_subset):
                        # cn_i is the superset
                        raise Exception("Create Dependency chain")

                        # Generate edge between the cn's
                        over_coverage_scenario_1 = True
                        self.add_edge(cn_j.id, cn_i.id)

                # This is the sanity check to see if its valid
                # TODO - if this fails, we need to identify the scenario
                assert over_coverage_scenario_1

                # Remove all the supersets marked to leave only 1 at the end
                # this will get flagged in the assert later on
                # for cn in superset_cn_set:
                #     cn_list.remove(cn)

                pass

        # Overcoverage Part 2
        # TODO- Figure out how to handle the overcoverage scenario where are no subset/superset scenarios
        pass

        # Step 2 - Now that we know the mapping, go through each connection in the fig,
        for edge in fig.edges:
            src = edge[0]
            tar = edge[1]
            if (
                src not in fig_nodes_cn_reverse_map.keys()
                or tar not in fig_nodes_cn_reverse_map.keys()
            ):
                print(
                    "Warning in generating Construction graph edges ! - Src `{}` or Tar `{}` not in the reverse-mapping of construction , under coverage issue".format(
                        src, tar
                    )
                )
                # raise Exception(
                #     "Src or Tar not in the construction graph, under coverage issue"
                # )
                continue
            else:
                # TODO - When the asserts fail, its an overcoverage issue, decide what needs to be done here
                src_cn = fig_nodes_cn_reverse_map[src]
                assert len(src_cn) == 1
                tar_cn = fig_nodes_cn_reverse_map[tar]
                assert len(tar_cn) == 1

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


def str_lists_equal(list_1: List[str], list_2: List[str]) -> bool:
    """Checks if the two lists of strings are equal or not. It sorts the list
    and then return true if both of them are equal else returns false

    Args:
        list_1 (List[str]): First List to compare
        list_2 (List[str]): Second List to compare

    Returns:
        bool: Returns True if both the lists are equal or else it returns False
    """
    list_1.sort()
    list_2.sort()
    if len(list_1) != len(list_2):
        return False

    for str1, str2 in zip(list_1, list_2):
        if str1 != str2:
            return False

    return True
