from __future__ import annotations

import copy
import uuid
from typing import Dict, List, Tuple, Union

import networkx as nx

from lfr.compiler.distribute.statetable import StateTable
from lfr.fig.annotation import (
    ANDAnnotation,
    DistributeAnnotation,
    NOTAnnotation,
    ORAnnotation,
)
from lfr.fig.fignode import FIGNode, IONode, IOType, ValueNode
from lfr.fig.interaction import (
    FluidFluidInteraction,
    FluidIntegerInteraction,
    FluidNumberInteraction,
    FluidProcessInteraction,
    Interaction,
    InteractionType,
)


class FluidInteractionGraph(nx.DiGraph):
    """Fluid Interaction Graph

    This is the main data structure for the Fluid Interaction Graph. It is a directed graph
    where the nodes are the fluid objects and the interactions between the fluid objects.

    It additionally stores the annotations and the state tables.
    """

    def __init__(self, data=None, val=None, **attr) -> None:
        """Constructor for the FluidInteractionGraph

        Args:
            data (dict, optional): Networkx data dict. Defaults to None.
            val (dict, optional): Networkx val dict. Defaults to None.
        """
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

    def add_state_table(self, state_table: StateTable) -> None:
        """Adds a state table to the FluidInteractionGraph

        Args:
            state_table (StateTable): State table to add
        """
        self._state_tables.append(state_table)

    @property
    def annotations(self) -> List[DistributeAnnotation]:
        """Returns the list of annotations

        Returns:
            List[DistributeAnnotation]: List of annotations
        """
        return self._annotations

    def get_annotation_by_id(self, id: str) -> DistributeAnnotation:
        """Returns the annotation with the given ID

        Args:
            id (str): ID of the annotation

        Raises:
            KeyError: If the annotation is not found

        Returns:
            DistributeAnnotation: Annotation with the given ID
        """
        for annotation in self._annotations:
            if annotation.id == id:
                return annotation
        raise KeyError(f"Cannot find the annotation with ID: {id}")

    def add_fignode(self, node: FIGNode) -> None:
        """Adds a FIGNode to the FluidInteractionGraph

        Args:
            node (FIGNode): FIGNode to add
        """
        self._fignodes[node.ID] = node
        self._annotations_reverse_map[node] = []
        self.add_node(node.ID)

    def get_fignode(self, id: str) -> FIGNode:
        """Returns the FIGNode with the given ID

        Args:
            id (str): ID of the FIGNode

        Raises:
            Exception: If the FIGNode is not found

        Returns:
            FIGNode: FIGNode with the given ID
        """
        if id in self._fignodes:
            return self._fignodes[id]
        else:
            raise Exception(f"Cannot find the node '{id}' in the FluidInteractionGraph")

    def load_fignodes(self, fig_nodes: List[FIGNode]) -> None:
        """Loads the FIGNodes into the FluidInteractionGraph

        Args:
            fig_nodes (List[FIGNode]): List of FIGNodes to load
        """
        for node in fig_nodes:
            self._fignodes[node.ID] = node

            # Add an entry for the reverse map here to make things simpler
            self._annotations_reverse_map[node] = []

    def load_annotations(self, annotations: List[DistributeAnnotation]) -> None:
        """Loads the annotations into the FluidInteractionGraph

        Args:
            annotations (List[DistributeAnnotation]): List of annotations to load
        """
        self._annotations.extend(annotations)
        for annotation in annotations:
            for item in annotation.get_items():
                if isinstance(item, DistributeAnnotation):
                    self.__add_to_reverse_map(item, annotation)
                else:
                    self.__add_to_reverse_map(item[0], annotation)
                    self.__add_to_reverse_map(item[1], annotation)

    def contains_fignode(self, fluid_object: FIGNode) -> bool:
        """Returns true if the FIGNode is present in the FluidInteractionGraph

        Args:
            fluid_object (FIGNode): FIGNode to check

        Returns:
            bool: True if the FIGNode is present in the FluidInteractionGraph
        """
        return fluid_object.ID in self._fignodes

    def switch_fignode(self, old_fignode: FIGNode, new_fignode: FIGNode) -> None:
        """Switch the old fignode with the new fignode

        Args:
            old_fignode (FIGNode): the old fignode
            new_fignode (FIGNode): the new fignode
        """
        self._fignodes[old_fignode.ID] = new_fignode

    def rename_nodes(self, rename_map: Dict[str, str]) -> None:
        """Rename the nodes in the FIG

        Args:
            rename_map (Dict[str, str]): a map from the old node ID to the new node ID
        """
        for node in self.nodes:
            fig_node = self._fignodes[node]
            fig_node.rename(rename_map[node])
            self._fignodes[rename_map[node]] = fig_node

            # Deleted the old key in the dictionary
            del self._fignodes[node]

        nx.relabel_nodes(self, rename_map, False)

    def rename_annotations(
        self, fig_node_rename_map: Dict[str, str], annotation_rename_map: Dict[str, str]
    ) -> None:
        """Rename the annotations in the FIG

        Args:
            fig_node_rename_map (Dict[str, str]): a map from the old fignode ID to the new
            annotation_rename_map (Dict[str, str]): a map from the old annotation ID to the
        """
        for annotation in self._annotations:
            annotation.rename(annotation_rename_map[annotation.id])

        fig_copy = self
        # Switch all the items of the annotations to the new fignodes
        for annotation in list(fig_copy.annotations):
            new_items_list: List[
                Union[Tuple[FIGNode, FIGNode], DistributeAnnotation]
            ] = []

            old_fignode_item_id_list = [
                (item[0].ID, item[1].ID)
                for item in annotation.get_items()
                if isinstance(item, tuple())
            ]

            # Now switch the items to the new fignodes
            for (
                old_fignode_item_id_1,
                old_fignode_item_id_2,
            ) in old_fignode_item_id_list:
                new_fignode_item_id_1 = fig_node_rename_map[old_fignode_item_id_1]
                new_fignode_item_id_2 = fig_node_rename_map[old_fignode_item_id_2]
                tuple_to_add: Tuple[FIGNode, FIGNode] = (
                    fig_copy.get_fignode(new_fignode_item_id_1),
                    fig_copy.get_fignode(new_fignode_item_id_2),
                )
                new_items_list.append(tuple_to_add)

            old_annotation_item_id_list = [
                item.id
                for item in annotation.get_items()
                if isinstance(item, DistributeAnnotation)
            ]

            for old_annotation_item_id in old_annotation_item_id_list:
                new_annotation_item_id = annotation_rename_map[old_annotation_item_id]
                annotation_to_add: DistributeAnnotation = fig_copy.get_annotation_by_id(
                    new_annotation_item_id
                )
                new_items_list.append(annotation_to_add)

            # now replace the annotation items with the new ones
            annotation.clear_items()
            for item in new_items_list:
                annotation.add_annotated_item(item)

    def add_interaction(self, interaction: Interaction):
        """Add an interaction to the FIG

        Args:
            interaction (Interaction): the interaction to add

        Raises:
            Exception: If the interaction is already present in the FIG
            Exception: If the interaction is of an invalid type
        """
        if interaction.ID not in self._fignodes:
            self.add_fignode(interaction)
        else:
            raise Exception(f"Interaction already present in the FIG: {interaction.ID}")

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
        """Connect two fignodes in the FIG

        Args:
            source (FIGNode): source fignode
            target (FIGNode): target fignode

        Raises:
            Exception: if the source fignode is not present in the FIG
        """
        if source.ID not in self._fignodes:
            raise Exception(
                f"Unable to add interaction because of missing flow: {source.ID}"
            )
        if target.ID not in self._fignodes:
            raise Exception(
                f"Unable to add interaction because of missing flow: {target.ID}"
            )

        self.add_edge(source.ID, target.ID)

    def get_interactions(self) -> List[Interaction]:
        """Get all the interactions in the FIG

        Returns:
            List[Interaction]: a list of all the interactions in the FIG
        """
        ret = []
        for item in self._fignodes.values():
            if isinstance(item, Interaction):
                ret.append(item)

        return ret

    @property
    def io(self) -> List[IONode]:
        """Get all the IONodes in the FIG

        Returns:
            List[IONode]: a list of all the IONodes in the FIG
        """
        ret = []
        for key in self._fignodes:
            node = self._fignodes[key]
            if isinstance(node, IONode):
                ret.append(node)

        return ret

    def get_fig_annotations(self, fig_node: FIGNode) -> List[DistributeAnnotation]:
        """Get the annotations for a given FIGNode

        Args:
            fig_node (FIGNode): the FIGNode to get the annotations for

        Returns:
            List[DistributeAnnotation]: a list of the annotations for the given FIGNode
        """
        return self._annotations_reverse_map[fig_node]

    def add_and_annotation(
        self, fignode_tuples: List[Tuple[FIGNode, FIGNode]]
    ) -> ANDAnnotation:
        annotation_name = "DIST_AND_" + str(uuid.uuid4())
        print(f"Adding DIST-AND annotation '{annotation_name}' for fig nodes:")
        for item in fignode_tuples:
            print(f"{item[0]}->{item[1]}")
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
        """Add a new OR annotation to the FIG

        Args:
            constrained_items (List[Union[Tuple[FIGNode, FIGNode], DistributeAnnotation]]): a list
            of tuples of FIGNodes or DistributeAnnotations

        Returns:
            ORAnnotation: the new ORAnnotation
        """
        annotation_name = "DIST_OR_" + str(uuid.uuid4())
        print(f"Adding DIST-OR annotation '{annotation_name}' for fig nodes:")
        for item in constrained_items:
            if isinstance(item, DistributeAnnotation):
                print(f"{item.id} (Annotation)")
            else:
                print(f"{item[0]}->{item[1]}")

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
        """Add a new NOT annotation to the FIG

        Args:
            fignode_tuple (Tuple[FIGNode, FIGNode]): a tuple of FIGNodes

        Returns:
            NOTAnnotation: the new NOTAnnotation
        """
        annotation_name = "DIST_NOT_" + str(uuid.uuid4())
        print(f"Adding DIST-AND annotation '{annotation_name}' for fig nodes:")
        print(f"{fignode_tuple[0]}->{fignode_tuple[1]}")

        annotation = NOTAnnotation(annotation_name)
        self._annotations.append(annotation)
        self._annotations_reverse_map[annotation] = []
        annotation.add_annotated_item(fignode_tuple)
        self.__add_to_reverse_map(fignode_tuple[0], annotation)
        self.__add_to_reverse_map(fignode_tuple[1], annotation)
        return annotation

    def add_fig(self, fig_to_add: FluidInteractionGraph) -> None:
        """Add a FluidInteractionGraph to this FIG

        Args:
            fig_to_add (FluidInteractionGraph): the FIG to add

        Raises:
            Exception: if any of the nodes in the FIG to add are already present in this FIG
        """
        # Check if any of the incoming fig nodes are already present here
        for node_id in fig_to_add.nodes:
            if node_id in self._fignodes:
                raise Exception(f"Node '{node_id}' already present in the FIG")
            self.add_fignode(fig_to_add.get_fignode(node_id))

        for edge in fig_to_add.edges:
            self.add_edge(edge[0], edge[1])

        # TODO - Verify if the cloned annotations are correct or not
        self.load_annotations(fig_to_add.annotations)

    def get_input_fignodes(self) -> List[IONode]:
        """Get all the input IONodes in the FIG

        Returns:
            List[IONode]: a list of all the input IONodes in the FIG
        """
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
        fignodes_copy_map: Dict[FIGNode, FIGNode] = {}

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
        figannotations_copy_map: Dict[DistributeAnnotation, DistributeAnnotation] = {}

        # Copy the annotations into the new fig copy
        for current_annotation in self._annotations:
            copy_annotation = copy.deepcopy(current_annotation)
            copy_annotation.clear_items()
            figannotations_copy_list.append(copy_annotation)
            figannotations_copy_map[current_annotation] = copy_annotation

        # TODO - Copy the annotations items
        for current_annotation in self._annotations:
            copy_annotation = figannotations_copy_map[current_annotation]
            for annotation_item in current_annotation.get_items():
                if isinstance(annotation_item, DistributeAnnotation):
                    annotation_to_add = figannotations_copy_map[annotation_item]
                    copy_annotation.add_annotated_item(annotation_to_add)
                else:
                    tuple_to_add = (
                        fignodes_copy_map[annotation_item[0]],
                        fignodes_copy_map[annotation_item[1]],
                    )
                    copy_annotation.add_annotated_item(tuple_to_add)

        fig_copy.load_annotations(figannotations_copy_list)
        return fig_copy

    # ---------- HELPER METHODS -----------

    def __add_to_reverse_map(
        self,
        item: Union[FIGNode, DistributeAnnotation],
        annotation: DistributeAnnotation,
    ) -> None:
        """Adds to reverse map

        Args:
            item (Union[FIGNode, DistributeAnnotation]): Add to reverse map
            annotation (DistributeAnnotation): the annotation to add

        Raises:
            Exception: if the annotation is already present in the reverse map
        """
        if self._annotations_reverse_map is None:
            self._annotations_reverse_map = dict()

        if isinstance(item, DistributeAnnotation):
            self.__add_to_reverse_map(item, annotation)
        else:
            if item in self._annotations_reverse_map:
                annotation_list = self._annotations_reverse_map[item]
                if annotation not in annotation_list:
                    annotation_list.append(annotation)
            else:
                if annotation in self._annotations_reverse_map[item]:
                    raise Exception("Annotation already present in the reverse map !")

                self._annotations_reverse_map[item] = [annotation]

    def __get_val_node_id(self) -> str:
        """Get a unique ID for a value node

        Returns:
            str: a unique ID for a value node
        """
        self._gen_id += 1
        return f"val_{self._gen_id}"

    def __add_fluid_fluid_interaction(self, interaction: FluidFluidInteraction) -> None:
        """Adds a fluid-fluid interaction to the FIG

        Args:
            interaction (FluidFluidInteraction): the interaction to add

        Raises:
            Exception: if the interaction is not a fluid-fluid interaction
            Exception: if the interaction is not a valid interaction
        """
        # Check if flow exists
        if interaction.fluids[0].ID not in self._fignodes:
            raise Exception(
                "Unable to add interaction because of missing flow:"
                f" {interaction.fluids[0].ID}"
            )
        if interaction.fluids[1].ID not in self._fignodes:
            raise Exception(
                "Unable to add interaction because of missing flow:"
                f" {interaction.fluids[1].ID}"
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
        """adds a single fluid interaction to the FIG

        Args:
            interaction (FluidProcessInteraction): the interaction to add

        Raises:
            Exception: if the interaction is not a fluid-process interaction
        """
        if interaction.fluid.ID not in self._fignodes:
            raise Exception(
                "Unable to add interaction because of missing flow:"
                " {interaction.fluid.ID}"
            )

        self.add_node(interaction.ID)
        self.add_edge(interaction.fluid.ID, interaction.ID)

        # TODO: Need to add an output node

    def __add_fluid_number_interaction(
        self, interaction: FluidNumberInteraction
    ) -> None:
        """adds a fluid-number interaction to the FIG

        Args:
            interaction (FluidNumberInteraction): the interaction to add

        Raises:
            Exception: if the interaction is not a fluid-number interaction
        """
        if interaction.fluid.ID not in self._fignodes:
            raise Exception(
                "Unable to add interaction because of missing flow:"
                f" {interaction.fluid.ID}"
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
        """adds a fluid-integer interaction to the FIG

        Args:
            interaction (FluidIntegerInteraction): the interaction to add

        Raises:
            Exception: if the interaction is not a fluid-integer interaction
        """
        if interaction.fluid.ID not in self._fignodes:
            raise Exception(
                "Unable to add interaction because of missing flow:"
                f" {interaction.fluid.ID}"
            )

        # Create new Value node
        val_node = ValueNode(self.__get_val_node_id(), interaction.value)
        self.add_fignode(val_node)

        self.add_node(interaction.ID)
        self.add_edge(interaction.fluid.ID, interaction.ID)
        self.add_edge(val_node.ID, interaction.ID)
