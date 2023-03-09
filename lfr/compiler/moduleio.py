from typing import Optional

from lfr.compiler.language.vectorrange import VectorRange
from lfr.fig.fignode import IOType


class ModuleIO:
    def __init__(self, name: str, iotype: IOType):
        self.type = iotype
        self._id = name
        self._vector_ref: Optional[VectorRange] = None

    @property
    def id(self) -> str:
        return self._id

    @property
    def vector_ref(self) -> VectorRange:
        if self._vector_ref is None:
            raise ValueError(
                f"Vector Reference is not set for ModuleIO: {self.id}, type:"
                f" {self.type}"
            )
        return self._vector_ref

    @vector_ref.setter
    def vector_ref(self, node: VectorRange):
        self._vector_ref = node

    def __str__(self):
        return "Name: {0.id}, Type : {0.type}".format(self)
