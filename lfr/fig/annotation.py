from typing import List
from lfr.fig.fignode import FIGNode


class DistributeAnnotation:
    def __init__(self, id: str) -> None:
        self._id = id
        self._fignodes = []

    @property
    def id(self) -> str:
        return self._id

    def add_fignode(self, fignode: FIGNode) -> None:
        self._fignodes.append(fignode)

    def remove_fignode(self, fignode: FIGNode) -> None:
        self._fignodes.remove(fignode)

    def get_annotations(self) -> List[FIGNode]:
        return self._fignodes

    def clear_annotations(self) -> None:
        self._fignodes.clear()


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
