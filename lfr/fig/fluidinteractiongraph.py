from __future__ import annotations

import copy

import networkx as nx

from lfr.compiler.distribute.statetable import StateTable
from typing import List, Dict, Tuple, Union
from lfr.fig.fignode import (
    FIGNode,
    IONode,
    IOType,
    ValueNode,
)

from lfr.fig.annotation import (
    ANDAnnotation,
    DistributeAnnotation,
    NOTAnnotation,
    ORAnnotation,
)

from lfr.fig.interaction import (
    FluidFluidInteraction,
    FluidIntegerInteraction,
    FluidNumberInteraction,
    FluidProcessInteraction,
    Interaction,
    InteractionType,
)

import uuid


class FluidInteractionGraph(nx.DiGraph):
    def __init__(self, data=None, val=None, **attr) -> None:
        super(FluidInteractionGraph, self).__init__()
        self._fignodes: Dict[str, FIGNode] = {}
        # self._fluid_interactions = dict()
        self._gen_id = 0
        self._annotations_reverse_map: Dict[
            Union[FIGNode, DistributeAnnotation], List[DistributeAnnotation]
        ] = dict()
        self._annotations: List[DistributeAnnotation] = []
        # Use this to store all the control to flow logic
        self._state_tables: List[StateTable] = []

    def add_state_table(self, state_table) -> None:
        self._state_tables.append(state_table)

    @property
    def annotations(self) -> List[DistributeAnnotation]:
        return self._annotations

    def add_fignode(self, node: FIGNode) -> None:
        self._fignodes[node.ID] = node
        self._annotations_reverse_map[node] = []
        self.add_node(node.ID)

    def get_fignode(self, id: str) -> FIGNode:
        if id in self._fignodes.keys():
            return self._fignodes[id]
        else:
            raise Exception(
                "Cannot find the node '{}' in the FluidInteractionGraph".format(id)
            )

    def load_fignodes(self, fig_nodes: List[FIGNode]) -> None:
        for node in fig_nodes:
            self._fignodes[node.ID] = node

            # Add an entry for the reverse map here to make things simpler
            self._annotations_reverse_map[node] = []

    def load_annotations(self, annotations: List[DistributeAnnotation]) -> None:
        self._annotations.extend(annotations)
        for annotation in self._annotations:
            for item in annotation.get_items():
                if isinstance(item, DistributeAnnotation):
                    self.__add_to_reverse_map(item, annotation)
                else:
                    self.__add_to_reverse_map(item[0], annotation)
                    self.__add_to_reverse_map(item[1], annotation)

    def contains_fignode(self, fluid_object: FIGNode) -> bool:
        return fluid_object.ID in self._fignodes.keys()

    def switch_fignode(self, old_fignode: FIGNode, new_fignode: FIGNode) -> None:
        self._fignodes[old_fignode.ID] = new_fignode

    def rename_nodes(self, rename_map: Dict[str, str]) -> None:
        for node in self.nodes:
            fig_node = self._fignodes[node]
            fig_node.rename(rename_map[node])
            self._fignodes[rename_map[node]] = fig_node

            # Deleted the old key in the dictionary
            del self._fignodes[node]

        nx.relabel_nodes(self, rename_map, False)

    def rename_annotations(self, rename_map: Dict[str, str]) -> None:
        for annotation in self._annotations:
            annotation.rename(rename_map[annotation.id])

    def add_interaction(self, interaction: Interaction):
        if interaction.ID not in self._fignodes.keys():
            self.add_fignode(interaction)
        else:
            raise Exception(
                "Interaction already present in the FIG: {0}".format(interaction.ID)
            )

        if isinstance(interaction, FluidFluidInteraction):
            self.__add_fluid_fluid_interaction(interaction)

        elif isinstance(interaction, FluidProcessInteraction):
            self.__add_single_fluid_interaction(interaction)

        elif isinstance(interaction, FluidNumberInteraction):
            self.__add_fluid_number_interaction(interaction)

        elif isinstance(interaction, FluidIntegerInteraction):
            self.__add_fluid_integer_interaction(interaction)

        else:
            raise Exception("Invalid Interaction Type found here")

    def connect_fignodes(self, source: FIGNode, target: FIGNode):
        if source.ID not in self._fignodes.keys():
            raise Exception(
                "Unable to add interaction because of missing flow: {0}".format(
                    source.ID
                )
            )
        if target.ID not in self._fignodes.keys():
            raise Exception(
                "Unable to add interaction because of missing flow: {0}".format(
                    target.ID
                )
            )

        self.add_edge(source.ID, target.ID)

    def get_interactions(self) -> List[Interaction]:
        ret = []
        for item in self._fignodes.values():
            if isinstance(item, Interaction):
                ret.append(item)

        return ret

    @property
    def io(self) -> List[IONode]:
        ret = []
        for key in self._fignodes:
            node = self._fignodes[key]
            if isinstance(node, IONode):
                ret.append(node)

        return ret

    def get_fig_annotations(self, fig_node: FIGNode) -> List[DistributeAnnotation]:
        return self._annotations_reverse_map[fig_node]

    def add_and_annotation(
        self, fignode_tuples: List[Tuple[FIGNode, FIGNode]]
    ) -> ANDAnnotation:
        annotation_name = "DIST_AND_" + str(uuid.uuid4())
        print("Adding DIST-AND annotation '{}' for fig nodes:".format(annotation_name))
        for item in fignode_tuples:
            print("{}->{}".format(item[0], item[1]))
        annotation = ANDAnnotation(annotation_name)
        self._annotations.append(annotation)
        self._annotations_reverse_map[annotation] = []
        for fignode_tuple in fignode_tuples:
            annotation.add_annotated_item(fignode_tuple)
            self.__add_to_reverse_map(fignode_tuple[0], annotation)
            self.__add_to_reverse_map(fignode_tuple[1], annotation)
        return annotation

    def add_or_annotation(
        self,
        constrained_items: List[Union[Tuple[FIGNode, FIGNode], DistributeAnnotation]],
    ) -> ORAnnotation:
        annotation_name = "DIST_OR_" + str(uuid.uuid4())
        print("Adding DIST-OR annotation '{}' for fig nodes:".format(annotation_name))
        for item in constrained_items:
            if isinstance(item, DistributeAnnotation):
                print("{} (Annotation)".format(item.id))
            else:
                print("{}->{}".format(item[0], item[1]))

        annotation = ORAnnotation(annotation_name)
        self._annotations.append(annotation)
        self._annotations_reverse_map[annotation] = []
        for item in constrained_items:
            annotation.add_annotated_item(item)
            if isinstance(item, DistributeAnnotation):
                pass
            else:
                self.__add_to_reverse_map(item[0], annotation)
                self.__add_to_reverse_map(item[1], annotation)

        return annotation

    def add_not_annotation(
        self, fignode_tuple: Tuple[FIGNode, FIGNode]
    ) -> NOTAnnotation:
        annotation_name = "DIST_NOT_" + str(uuid.uuid4())
        print("Adding DIST-AND annotation '{}' for fig nodes:".format(annotation_name))
        print("{}->{}".format(fignode_tuple[0], fignode_tuple[1]))

        annotation = NOTAnnotation(annotation_name)
        self._annotations.append(annotation)
        self._annotations_reverse_map[annotation] = []
        annotation.add_annotated_item(fignode_tuple)
        self.__add_to_reverse_map(fignode_tuple[0], annotation)
        self.__add_to_reverse_map(fignode_tuple[1], annotation)
        return annotation

    def add_fig(self, fig_to_add: FluidInteractionGraph) -> None:
        # Check if any of the incoming fig nodes are already present here
        for node_id in fig_to_add.nodes:
            if node_id in self._fignodes.keys():
                raise Exception("Node '{}' already present in the FIG".format(node_id))
            self.add_fignode(fig_to_add.get_fignode(node_id))

        for edge in fig_to_add.edges:
            self.add_edge(edge[0], edge[1])

        # TODO - Verify if the cloned annotations are correct or not
        self.load_annotations(fig_to_add.annotations)

    def get_input_fignodes(self) -> List[IONode]:
        ret = []
        for fignode in self._fignodes.values():
            if isinstance(fignode, IONode):
                if fignode.type is IOType.FLOW_INPUT:
                    ret.append(fignode)

        return ret

    def __str__(self):
        return self.edges.__str__()

    def copy(self, as_view):
        return super().copy(as_view=as_view)

    def __deepcopy__(self, memo=None):
        if memo is None:
            memo = {}

        not_there = []
        existing = memo.get(self, not_there)
        if existing is not not_there:
            print("ALREADY COPIED TO", repr(existing))
            return existing

        fignodes_copy_list = []

        # Map old_fignode <-> new_fignode
        fignodes_copy_map: Dict[FIGNode, FIGNode] = dict()

        for fignode in self._fignodes.values():
            fignode_copy = copy.copy(fignode)
            fignodes_copy_list.append(fignode_copy)
            fignodes_copy_map[fignode] = fignode_copy

        fig_copy = self.copy(as_view=False)
        fig_copy.__class__ = FluidInteractionGraph
        assert isinstance(fig_copy, FluidInteractionGraph)
        fig_copy.load_fignodes(fignodes_copy_list)

        # Now since all the annotations are loaded up, copy the right cloned
        # references to fig nodes for the constriants
        figannotations_copy_list = []

        # Map old_annotatin <-> new_annotation
        figannotations_copy_map: Dict[
            DistributeAnnotation, DistributeAnnotation
        ] = dict()

        # Copy the annotations into the new fig copy
        for current_annotation in self._annotations:
            copy_annotation = copy.deepcopy(current_annotation)
            copy_annotation.clear_fignodes()
            figannotations_copy_list.append(copy_annotation)
            figannotations_copy_map[current_annotation] = copy_annotation

        # TODO - Copy the annotations items
        for current_annotation in self._annotations:
            copy_annotation = figannotations_copy_map[current_annotation]
            for annotation_item in current_annotation.get_items():
                if isinstance(annotation_item, DistributeAnnotation):
                    item_to_add = figannotations_copy_map[annotation_item]
                    copy_annotation.add_annotated_item(item_to_add)
                else:
                    item_to_add = (
                        fignodes_copy_map[annotation_item[0]],
                        fignodes_copy_map[annotation_item[1]],
                    )
                    copy_annotation.add_annotated_item(item_to_add)

        fig_copy.load_annotations(figannotations_copy_list)
        return fig_copy

    # ---------- HELPER METHODS -----------

    def __add_to_reverse_map(
        self,
        item: Union[FIGNode, DistributeAnnotation],
        annotation: DistributeAnnotation,
    ) -> None:
        if self._annotations_reverse_map is None:
            self._annotations_reverse_map = dict()

        if isinstance(item, DistributeAnnotation):
            self.__add_to_reverse_map(item, annotation)
        else:
            if item in self._annotations_reverse_map.keys():
                self._annotations_reverse_map[item].append(annotation)
            else:
                if annotation in self._annotations_reverse_map[item]:
                    raise Exception("Annotation already present in the reverse map !")

                self._annotations_reverse_map[item] = [annotation]

    def __get_val_node_id(self) -> str:
        self._gen_id += 1
        return "val_{0}".format(self._gen_id)

    def __add_fluid_fluid_interaction(self, interaction: FluidFluidInteraction) -> None:
        # Check if flow exists
        if interaction.fluids[0].ID not in self._fignodes.keys():
            raise Exception(
                "Unable to add interaction because of missing flow: {0}".format(
                    interaction.fluids[0].ID
                )
            )
        if interaction.fluids[1].ID not in self._fignodes.keys():
            raise Exception(
                "Unable to add interaction because of missing flow: {0}".format(
                    interaction.fluids[1].ID
                )
            )

        self.add_node(interaction.ID)
        self.add_edge(interaction.fluids[0].ID, interaction.ID)

        # Figure out how we want to connect FIGNodes
        if interaction.type is InteractionType.SIEVE:
            # In the case of a SIEVE interaction, we need to add the second
            # FIGNode as an output
            self.add_edge(interaction.ID, interaction.fluids[1].ID)
        else:
            self.add_edge(interaction.fluids[1].ID, interaction.ID)

        # TODO: Need to add an output node

    def __add_single_fluid_interaction(
        self, interaction: FluidProcessInteraction
    ) -> None:
        if interaction.fluid.ID not in self._fignodes.keys():
            raise Exception(
                "Unable to add interaction because of missing flow: {0}".format(
                    interaction.fluid.ID
                )
            )

        self.add_node(interaction.ID)
        self.add_edge(interaction.fluid.ID, interaction.ID)

        # TODO: Need to add an output node

    def __add_fluid_number_interaction(
        self, interaction: FluidNumberInteraction
    ) -> None:
        if interaction.fluid.ID not in self._fignodes.keys():
            raise Exception(
                "Unable to add interaction because of missing flow: {0}".format(
                    interaction.fluid.ID
                )
            )

        # Create new Value node
        val_node = ValueNode(self.__get_val_node_id(), interaction.value)
        self.add_fignode(val_node)

        self.add_node(interaction.ID)
        self.add_edge(interaction.fluid.ID, interaction.ID)
        self.add_edge(val_node.ID, interaction.ID)

    def __add_fluid_integer_interaction(
        self, interaction: FluidIntegerInteraction
    ) -> None:
        if interaction.fluid.ID not in self._fignodes.keys():
            raise Exception(
                "Unable to add interaction because of missing flow: {0}".format(
                    interaction.fluid.ID
                )
            )

        # Create new Value node
        val_node = ValueNode(self.__get_val_node_id(), interaction.value)
        self.add_fignode(val_node)

        self.add_node(interaction.ID)
        self.add_edge(interaction.fluid.ID, interaction.ID)
        self.add_edge(val_node.ID, interaction.ID)
