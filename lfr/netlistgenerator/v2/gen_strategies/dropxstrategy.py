from lfr.fig.interaction import Interaction, InteractionType
from lfr.netlistgenerator.v2.dafdadapter import DAFDAdapter
from lfr.fig.fluidinteractiongraph import FluidInteractionGraph
from lfr.netlistgenerator.v2.constructiongraph import ConstructionGraph
from lfr.netlistgenerator.v2.constructionnode import ConstructionNode
from lfr.netlistgenerator.v2.gen_strategies.genstrategy import GenStrategy
import networkx as nx
from pymint import MINTDevice


class DropXStrategy(GenStrategy):
    def __init__(
        self, construction_graph: ConstructionGraph, fig: FluidInteractionGraph
    ) -> None:
        super().__init__(construction_graph, fig)

    def reduce_mapping_options(self) -> None:
        # Generate a topological order for the FIG to make sure athat we know the order of things
        figs_in_order = list(nx.topological_sort(self._fig))
        # Generate the mapping between fignodes and construction nodes
        # input_fignodes = self._fig.get_input_fignodes
        for fignode_id in self._fig.nodes:
            fignode = self._fig.get_fignode(fignode_id)

            # check if construction node
            if ConstructionNode(fignode.id).is_explictly_mapped:
                pass
            # TODO - Implement Generalized Ali Strategy 1
            # Rule 1 - The first level of % should be mapping to a Droplet Generator (TODO - Talk to ali about this or a T junction generator)
            # Step 1 - Check if fig node is interaction and of type METER (%) this is the check condition for rule 1
            else:
                if isinstance(fignode, Interaction):
                    if fignode.type is InteractionType.METER:
                        is_first_metering_node = True
                        # TODO - Check if DROPLET GENERATOR is one of the mapping options, skip if not
                        # Step 2 - If type is meter then check to see if other it is the first meter operation from inputs to current fignode
                        for sorted_fignode_id in figs_in_order:
                            if fignode_id == sorted_fignode_id:
                                # End of checking
                                if is_first_metering_node is True:
                                    # TODO - Eliminate all options other than Nozzle droplet generator for the associated construction node(s)
                                    cn = self._construction_graph.get_fignode_cn(
                                        fignode
                                    )
                                    # check mapping options
                                    print("***Detect Nozzle Droplet Gen***")
                                    for cn_part in cn.mapping_options:
                                        if (
                                            cn_part.primitive.mint
                                            != "NOZZLE DROPLET GENERATOR"
                                        ):
                                            # remove if its not nozzle droplet generator
                                            cn.mapping_options.remove(cn_part)
                                else:
                                    raise Exception(
                                        "No scheme for assign METER after initial droplet generation"
                                    )
                            else:
                                # get the sorted fignode
                                sorted_fignode = self._fig.get_fignode(
                                    sorted_fignode_id
                                )
                                if isinstance(sorted_fignode, Interaction):
                                    if sorted_fignode.type is InteractionType.METER:
                                        # check if node is connected to our node of interest
                                        if sorted_fignode_id in self._fig.predecessors(
                                            fignode_id
                                        ):
                                            is_first_metering_node = False

            # Rule 2 – Any +-, distribute nodes before % should be in continuous flow (figure out components for this)
            # TODO - Go through each of the FIG nodes, if the fig node has

        for fignode_id in self._fig.nodes:
            fignode = self._fig.get_fignode(fignode_id)

            # check if explicitly mapped
            if not ConstructionNode(fignode.id).is_explictly_mapped:
                if isinstance(fignode, Interaction):
                    if (fignode.type is InteractionType.MIX or fignode.type is InteractionType.SIEVE):
                        if self.__check_continuous(fignode_id):
                            # this is NOT continuous
                            raise Exception("flow before METER is not continuous")

        # Rule 3 – Any Remetering (%) should require a droplet breakdown and regeneration (Ask Ali)
        # Rule 4 – Distribute network post Metering stage should be mapped to different kinds of separator / selection/ storage networks
        # Rule 5 – If plus is shown between node that has % in pred and non % in pred, then its pico injection

        for fignode_id in self._fig.nodes:
            fignode = self._fig.get_fignode(fignode_id)

            # check if map
            if not ConstructionNode(fignode.id).is_explictly_mapped:
                if isinstance(fignode, Interaction):
                    # if +
                    if (
                        fignode.type is InteractionType.MIX
                        or fignode.type is InteractionType.SIEVE
                    ):
                        # compare predecessors, not successors
                        # create warning for more than 2 (mix can have more than 2 inputs)

                        meter_in_pred = []

                        # check pred

                        for prednode_id in self._fig.predecessors(fignode_id):
                            # check the first pred

                            meter_in_pred.append(
                                self.__search_predecessors(
                                    prednode_id, InteractionType.METER
                                )
                            )

                        numTrue = meter_in_pred.count(True)

                        if fignode.type is InteractionType.MIX:

                            if numTrue == 1:
                                # this is a pico injection
                                cn = self._construction_graph.get_fignode_cn(
                                    fignode
                                )
                                print("***Detect Pico Injector***")
                                # check mapping options
                                while(self.__exist_in_cn(cn, "PICOINJECTOR")):
                                    for cn_part in cn.mapping_options:
                                        print("-", cn_part.primitive.mint)
                                        if cn_part.primitive.mint != "PICOINJECTOR":
                                            # remove if its not [ico injection
                                            cn.mapping_options.remove(cn_part)
                                    print("after----")

                                for cn_part in cn.mapping_options:
                                    print("-", cn_part.primitive.mint)

                            # Rule 6
                            elif numTrue == 2:
                                # this is a droplet merging
                                cn = self._construction_graph.get_fignode_cn(
                                    fignode
                                )

                                print("***Detect Droplet Merger***")
                                while(self.__exist_in_cn(cn, "DROPLET MERGER")):
                                    for cn_part in cn.mapping_options:
                                        print("-", cn_part.primitive.mint)
                                        if cn_part.primitive.mint != "DROPLET MERGER":
                                            cn.mapping_options.remove(cn_part)
                                    print("after----")

                                for cn_part in cn.mapping_options:
                                    print("-", cn_part.primitive.mint)

                            else:
                                print("***Mixer***")
                                cn = self._construction_graph.get_fignode_cn(
                                    fignode
                                )
                                while(self.__exist_in_cn(cn, "MIXER")):
                                    for cn_part in cn.mapping_options:
                                        print("-", cn_part.primitive.mint)
                                        if cn_part.primitive.mint != "MIXER":
                                            cn.mapping_options.remove(cn_part)

                                    print("after------")
                                for cn_part in cn.mapping_options:
                                    print("-", cn_part.primitive.mint)
                                pass


        # Rule 6 – if plus is sown between two nodes that has % in pred, then its droplet merging
        # Rule 7 – TBD Rule for droplet splitting
        # Finally just reduce the total number of mapping options if greater than 1
        super().reduce_mapping_options()


    def __exist_in_cn(self, cn, mint_name):
        """helper function to check if the construction node contains undesired mints.

        Args:
            cn (ConstructionNode): ConstructionNode to be checked
            mint_name (string): mint name to check

        Returns:
            Bool: if mint names other than the specified mint_name is found, returns true. Else false.
        """
        for cn_part in cn.mapping_options:
            if cn_part.primitive.mint != mint_name:
                return True

        return False


    def __search_predecessors(self, fignode_id, search_type):
        """recursive function searches for the specified InteractionType in the predecessors of the specified fignode_id

        Args:
            fignode_id (elements in self._fig.nodes): Starting node to find the predecessors
            search_type (InteractionType): Interaction type to find in the predecessors

        Returns:
            Bool: If found, returns true. Else false
        """
        fignode = self._fig.get_fignode(fignode_id)

        if self.__check_if_type(fignode, search_type):
            return True

        else:
            for prednode_id in self._fig.predecessors(fignode_id):
                if self.__search_predecessors(prednode_id, search_type):
                    return True

        return False

    def __check_if_type(self, fignode, search_type):
        """helper function for __search_predecessors and __check_continuous. Check if the specified search_type matches to the fignode.type

        Args:
            fignode (FIGNode): fignode that contains InteractionType as type
            search_type ([type]): desired type to check

        Returns:
            Bool: if fignode.type matches to search_type, returns true. Else false
        """
        if isinstance(fignode, Interaction):
            if fignode.type is search_type:
                return True

        return False

    # this function checks if the predecessors before METER has METER or not. If not, continuous.
    def __check_continuous(self, fignode_id):
        """recursive function to check if the flow before METER is continuous at MIX or SIEVE

        Args:
            fignode_id (elements in self._fig.nodes): Starting node to find predecessors

        Returns:
            Bool: if METER is found in the predecessors of METER, returns true (not continuous), Else false
        """
        fignode = self._fig.get_fignode(fignode_id)

        if self.__check_if_type(fignode, InteractionType.METER):
            for prednode_id in self._fig.predecessors(fignode_id):
                if self.__search_predecessors(prednode_id, InteractionType.METER):
                    return True

        else:
            for other_pred_id in self._fig.predecessors(fignode_id):
                if self.__check_continuous(other_pred_id):
                    return True

        return False

    def size_netlist(self, device: MINTDevice) -> None:
        """
        Sizes the device based on either lookup tables, inverse design algorithms, etc.
        """
        dafd_adapter = DAFDAdapter(device)
        # Default size for PORT is 2000 um
        for component in device.components:
            constraints = self._construction_graph.get_component_cn(
                component
            ).constraints
            if component.entity == "NOZZLE DROPLET GENERATOR":
                # dafd_adapter.size_droplet_generator(component, constraints)
                print("Skipping calling DAFD since its crashing everything right now")
            elif component.entity == "PORT":
                component.params.set_param("portRadius", 2000)
