from __future__ import annotations
from typing import List, Union
from lfr.fig.fignode import FIGNode


class DistributeAnnotation:
    def __init__(self, id: str) -> None:
        self._id = id
        self._annotated_items: List[Union[FIGNode, DistributeAnnotation]] = []

    @property
    def id(self) -> str:
        return self._id

    def rename(self, new_id: str) -> None:
        self._id = new_id

    def add_annotated_item(self, item: Union[FIGNode, DistributeAnnotation]) -> None:
        self._annotated_items.append(item)

    def remove_item(self, item: Union[FIGNode, DistributeAnnotation]) -> None:
        self._annotated_items.remove(item)

    def get_items(self) -> List[Union[FIGNode, DistributeAnnotation]]:
        return self._annotated_items

    def clear_fignodes(self) -> None:
        self._annotated_items.clear()

    def __hash__(self) -> int:
        return hash(hex(id(self)))


class ANDAnnotation(DistributeAnnotation):
    def __init__(self, id: str) -> None:
        super(ANDAnnotation, self).__init__(id)

    @property
    def match_string(self):
        return "DISTRIBUTE-AND"


class ORAnnotation(DistributeAnnotation):
    def __init__(self, id: str) -> None:
        super(ORAnnotation, self).__init__(id)

    @property
    def match_string(self):
        return "DISTRIBUTE-OR"


class NOTAnnotation(DistributeAnnotation):
    def __init__(self, id: str) -> None:
        super(NOTAnnotation, self).__init__(id)

    @property
    def match_string(self):
        return "DISTRIBUTE-NOT"
