

from lfr.fig.fignode import IOType
from lfr.compiler.language.vectorrange import VectorRange


class ModuleIO:
    def __init__(self, name: str, iotype: IOType=None):
        self.type = iotype
        self._id = name
        self._vector_ref = None

    @property
    def id(self) -> str:
        return self._id

    @property
    def vector_ref(self) -> VectorRange:
        return self._vector_ref

    @vector_ref.setter
    def vector_ref(self, node: VectorRange):
        self._vector_ref = node

    def __str__(self):
        return "Name: {0.id}, Type : {0.type}".format(self)
