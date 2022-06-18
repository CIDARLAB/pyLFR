from __future__ import annotations

from typing import Dict, Generic, List, Optional, TypeVar


T = TypeVar("T")


class VariantNode(Generic[T]):
    """Variant Node Describes the node in the variant tree

    Its payload is a ConstructionGraph object and it contains the links to the parent
    and children
    """

    def __init__(self, variant: T) -> None:
        self._payload: T = variant
        self._parent: Optional[VariantNode] = None
        self._children: List[VariantNode] = []

    @property
    def payload(self) -> T:
        return self._payload

    @property
    def children(self) -> List[VariantNode]:
        return self._children

    @property
    def parent(self) -> Optional[VariantNode]:
        return self._parent

    @parent.setter
    def parent(self, parent: VariantNode) -> None:
        self._parent = parent

    def add_child(self, child: VariantNode) -> None:
        self._children.append(child)
        child._parent = self

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, VariantNode):
            # Check if the payloads are equal
            return self._payload == __o._payload
        else:
            return False


class VariantTree(Generic[T]):
    def __init__(
        self,
    ) -> None:
        self._root: Optional[VariantNode] = None
        self._node_walk: Optional[VariantNode] = None
        self._divergence_map: Dict[object, VariantNode] = {}

    def add_variant(
        self,
        variant_parent: T,
        variant_decendant: Optional[T],
    ) -> None:
        """Adds a new variant to the tree

        When adding the root node, the variant_leaf is set to None

        Args:
            variant_parent (ConstructionGraph): The parent variant to which we say that,
            when the variant tree is empty, this is the root.
            variant_decendant (Optional[ConstructionGraph]): The new variant to add to
            the tree, its set to None when adding the root.

        Raises:
            ValueError: The variant_parent is not in the tree, or the variant_decendant
            is set to None when we are not setting the root
        """
        if self._root is None:
            root = VariantNode(variant_parent)
            self._root = root

            if variant_decendant is not None:
                leaf = VariantNode(variant_decendant)
                leaf.parent = root
                self._root.add_child(leaf)

        else:
            # Cancel if only the variant root is provided
            if variant_decendant is None:
                raise ValueError("variant_decendant is None")

            # Find the parent of the variant and add the variant as the child
            parent = self._find_node(variant_parent)
            if parent is None:
                raise ValueError(f"Could not find parent of variant {variant_parent}")

            leaf = VariantNode(variant_decendant)
            leaf.parent = parent
            parent.add_child(leaf)

    def _find_node(self, variant: T) -> Optional[VariantNode]:
        """Find the node in the tree that matches the variant"""
        if self._root is None:
            return None

        # Perform recursive search to identify the variant provided
        # If the variant is found, return the node
        # If the variant is not found, return None

        def _find_node_recursive(
            node: VariantNode, variant: T
        ) -> Optional[VariantNode]:
            if node.payload == variant:
                return node

            for child in node.children:
                result = _find_node_recursive(child, variant)
                if result is not None:
                    return result

            return None

        return _find_node_recursive(self._root, variant)

    def prune_variant(self, variant: T) -> None:
        """Prune the variant tree to remove any variants that do not fully cover the
        fig"""

        def _prune_variant_recursive(node: VariantNode, variant: T) -> None:
            if node.payload == variant:
                # If the variant is found, remove the node from the tree
                if node.parent is not None:
                    node.parent.children.remove(node)
                return

            for child in node.children:
                _prune_variant_recursive(child, variant)

        if self._root is not None:
            # Check the trivial case if the root is the variant
            if self._root.payload == variant:
                self._root = None
                return

            _prune_variant_recursive(self._root, variant)

    def get_edge_leaves(self) -> List[T]:
        """Return all the ConstructionGraphs in the leaves of the variant tree"""
        leaves: List[T] = []

        def _edge_leaves_recursive(node: VariantNode) -> None:
            if len(node.children) == 0:
                leaves.append(node.payload)
                return

            for child in node.children:
                _edge_leaves_recursive(child)

        if self._root is not None:
            _edge_leaves_recursive(self._root)

        return leaves

    def walk_tree(self) -> List[T]:
        """Return an iterator that walks the variant tree

        Raises:
            ValueError: If the root is not set

        Returns:
            List[ConstructionGraph]: List of ConstructionGraphs that are in the variant
        """ """"""

        def _walker_recursive(level_nodes: List[VariantNode], output: List[T]) -> None:
            next_level_nodes: List[VariantNode] = []
            for level_node in level_nodes:
                for child in level_node.children:
                    next_level_nodes.append(child)
                    output.append(child.payload)

            for level_node in level_nodes:
                _walker_recursive(next_level_nodes, output)

        if self._root is None:
            raise ValueError("Variant tree root is empty")

        node_walk: List[T] = [self._root.payload]
        _walker_recursive([self._root], node_walk)
        return node_walk

    def has_divergence(self, divergence: object) -> bool:
        """Check if the variant has divergence

        Args:
            divergence (object): divergence object that needs to be checked

        Returns:
            bool: True if the divergence is found, False otherwise
        """
        if divergence in self._divergence_map:
            return True
        else:
            return False

    def save_divergence(self, divergence: object, variant: T) -> None:
        """Save the divergence of the variant to the variant tree

        Args:
            divergence (str): The delta that is being saved as the cause of the
            divergence
            variant (T): the payload corresponding to the divergence

        Raises:
            ValueError: If the payload cannot be found in the tree
            ValueError: If the divergence is already saved
        """
        node = self._find_node(variant)
        if node is None:
            raise ValueError(f"Could not find variant {variant}")

        if divergence in self._divergence_map:
            raise ValueError(f"Divergence {divergence} already exists")

        self._divergence_map[divergence] = node

    def get_divergence(self, divergence: object) -> Optional[T]:
        """Get the payload corresponding to the divergence

        Args:
            divergence (object): object indicating the divergence

        Returns:
            Optional[T]: the payload corresponding to the divergence
        """

        if divergence in self._divergence_map:
            return self._divergence_map[divergence].payload
        else:
            return None
