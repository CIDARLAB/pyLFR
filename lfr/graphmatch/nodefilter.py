from __future__ import annotations
from typing import List, Tuple


class NodeFilter:
    def __init__(
        self,
        node_types_filter: List[str] = [],
        node_attributes_filter: List[str] = [],
        node_constraints: List[Tuple[str, str]] = [],
    ) -> None:
        self._node_types_filter: List[str] = node_types_filter
        self._node_attributes_filter: List[str] = node_attributes_filter
        self._node_constraints: List[Tuple[str, str]] = node_constraints

    def is_valid_node_type(self, type_string: str) -> bool:
        if len(self._node_types_filter) == 0:
            # If there are no node type filters, then return true
            return True
        return type_string in self._node_types_filter

    def is_valid_attribute_type(self, attributestring: str) -> bool:
        # TODO - Figure out what this will be in tuture
        raise NotImplementedError("Currently do not support node attributes")
        return True

    def get_constraints(self) -> List[Tuple[str, str]]:
        return self._node_constraints
