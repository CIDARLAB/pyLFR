from __future__ import annotations

from typing import List, Optional


from lfr.netlistgenerator.constructiongraph.constructiongraph import ConstructionGraph


class VariantNode:
    """ Variant Node Describes the node in the variant tree 
    
    Its payload is a ConstructionGraph object and it contains the links to the parent 
    and children
    """
    
    def __init__(self, variant: ConstructionGraph) -> None:
        self._payload: ConstructionGraph = variant
        self._parent: Optional[VariantNode] = None
        self._children: List[VariantNode] = []

    @property
    def payload(self) -> ConstructionGraph:
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

    
class VariantTree:
    
    def __init__(self,) -> None:
        self._root: Optional[VariantNode] = None
        
    def add_variant(self, variant_root: ConstructionGraph, variant_leaf: Optional[ConstructionGraph]) -> None:
        if self._root is None:
            root = VariantNode(variant_root)
            self._root = root
            
            if variant_leaf is not None:
                leaf = VariantNode(variant_leaf)
                leaf.parent = root
                self._root.add_child(leaf)
                
        else:
            # Cancel if only the variant root is provided
            if variant_leaf is None:
                return
            
            # Find the parent of the variant and add the variant as the child
            parent = self._find_node(variant_root)
            if parent is None:
                raise ValueError(f"Could not find parent of variant {variant_root.name}")
            
            leaf = VariantNode(variant_leaf)
            leaf.parent = parent
            parent.add_child(leaf)
            
    
    def _find_node(self, variant: ConstructionGraph) -> Optional[VariantNode]:
        """ Find the node in the tree that matches the variant """
        if self._root is None:
            return None
        
        # Perform recursive search to identify the variant provided
        # If the variant is found, return the node
        # If the variant is not found, return None
        
        def _find_node_recursive(node: VariantNode, variant: ConstructionGraph) -> Optional[VariantNode]:
            if node.payload == variant:
                return node
            
            for child in node.children:
                result = _find_node_recursive(child, variant)
                if result is not None:
                    return result
                
            return None
        
        return _find_node_recursive(self._root, variant)
                          
    def prune_variant(self, variant:ConstructionGraph) -> None:
        """ Prune the variant tree to remove any variants that do not fully cover the fig """
        
        def _prune_variant_recursive(node: VariantNode, variant: ConstructionGraph) -> None:
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