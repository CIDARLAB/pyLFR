from lfr.fig.interaction import Interaction, InteractionType
from lfr.netlistgenerator.v2.dafdadapter import DAFDAdapter
from lfr.fig.fluidinteractiongraph import FluidInteractionGraph
from lfr.netlistgenerator.v2.constructiongraph import ConstructionGraph
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
        # print(figs_in_order)
        # Generate the mapping between fignodes and construction nodes
        # fig_cn_map = dict()
        # input_fignodes = self._fig.get_input_fignodes
        for fignode_id in self._fig.nodes:
            fignode = self._fig.get_fignode(fignode_id)
            # TODO - Implement Generalized Ali Strategy 1
            # Rule 1 - The first level of % should be mapping to a Droplet Generator (TODO - Talk to ali about this or a T junction generator)
            # Step 1 - Check if fig node is interaction and of type METER (%) this is the check condition for rule 1
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
                                cn = self._construction_graph.get_fignode_cn(fignode)
                                # check mapping options
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
                            sorted_fignode = self._fig.get_fignode(sorted_fignode_id)
                            if isinstance(sorted_fignode, Interaction):
                                if sorted_fignode.type is InteractionType.METER:
                                    # check if node is connected to our node of interest
                                    if sorted_fignode_id in self._fig.predecessors(
                                        fignode_id
                                    ):
                                        is_first_metering_node = False

            # Rule 2 – Any +-, distribute nodes before % should be in continuous flow (figure out components for this)
            # TODO - Go through each of the FIG nodes, if the fig node has
            # for fignode_id in self._fig.nodes:
            #     fignode = self._fig.get_fignode(fignode_id)

            #     # check if % in meter or sieve
            #     if isinstance(fignode, Interaction):
            #         if (
            #             fignode.type is InteractionType.MIX
            #             or fignode.type is InteractionType.SIEVE
            #         ):
            #             if self.__search_predecessors(
            #                 fignode_id, InteractionType.METER
            #             ):
            #                 # for loop to compare two inputs

            #                 # not a continuous flow
            #                 print("NOT continuous")
            #                 pass

            #             else:
            #                 # continuous flow
            #                 print("IS continuous")
            #                 pass

            # Rule 3 – Any Remetering (%) should require a droplet breakdown and regeneration (Ask Ali)
            # Rule 4 – Distribute network post Metering stage should be mapped to different kinds of separator / selection/ storage networks
            # Rule 5 – If plus is shown between node that has % in pred and non % in pred, then its pico injection

            for fignode_id in self._fig.nodes:
                fignode = self._fig.get_fignode(fignode_id)
                if isinstance(fignode, Interaction):
                    # if +
                    if (
                        fignode.type is InteractionType.MIX
                        or fignode.type is InteractionType.SIEVE
                    ):
                        # compare predecessors, not successors
                        # create warning for more than 2 (mix can have more than 2 inputs)

                        meter_in_pred1 = False
                        nonmeter_in_pred1 = False
                        nonmeter_in_pred2 = False
                        meter_in_pred2 = False

                        count = 0

                        # check pred

                        for prednode_id in self._fig.predecessors(fignode_id):
                            # check the first pred
                            if count == 0:
                                if self.__search_predecessors(
                                    prednode_id, InteractionType.METER
                                ):
                                    meter_in_pred1 = True

                                else:
                                    nonmeter_in_pred1 = True

                                count += 1

                            # check the second pred
                            elif count == 1:
                                if self.__search_predecessors(
                                    prednode_id, InteractionType.METER
                                ):
                                    meter_in_pred2 = True

                                else:
                                    nonmeter_in_pred2 = True

                                count += 1

                            else:
                                raise Exception("more than two inputs!")

                        if fignode.type is InteractionType.MIX:

                            if (meter_in_pred1 and nonmeter_in_pred2) or (
                                nonmeter_in_pred1 and meter_in_pred2
                            ):
                                # this is a pico injection
                                cn = self._construction_graph.get_fignode_cn(fignode)

                                # check mapping options
                                for cn_part in cn.mapping_options:
                                    if cn_part.primitive.mint != "PICOINJECTOR":
                                        # remove if its not [ico injection
                                        cn.mapping_options.remove(cn_part)

                            # Rule 6
                            elif meter_in_pred1 and meter_in_pred2:
                                # this is a droplet merging
                                pass  # temp

                            else:
                                raise Exception("can't recognize the device")

                        if (fignode.type is InteractionType.MIX) or (
                            fignode.type is InteractionType.SIEVE
                        ):

                            if nonmeter_in_pred1 and nonmeter_in_pred2:
                                # this is continuous
                                pass  # temp
                            else:
                                # not continuous
                                pass

            # Rule 6 – if plus is sown between two nodes that has % in pred, then its droplet merging
            # Rule 7 – TBD Rule for droplet splitting
        # Finally just reduce the total number of mapping options if greater than 1
        super().reduce_mapping_options()

    # recursive function do go through all the predecessors
    def __search_predecessors(self, fignode_id, search_type):
        # check if the node has predecessors
        does_exist = False

        if self._fig.predecessors(fignode_id):
            for prednode_id in self._fig.predecessors(fignode_id):
                prednode = self._fig.get_fignode(prednode_id)

                # if matches with search type, return true
                if isinstance(prednode, Interaction):
                    # if true, skip all the process
                    if does_exist is False:

                        if prednode.type is search_type:
                            does_exist = True

                        # if not matched, recursive
                        else:
                            does_exist = self.__search_predecessors(
                                prednode_id, search_type
                            )

        # if end of pred
        return does_exist

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
