from __future__ import annotations

from typing import TYPE_CHECKING, Generic, Optional, TypeVar

if TYPE_CHECKING:
    from lfr.compiler.language.vector import Vector

T = TypeVar("T")


class VectorRange(Generic[T]):
    """
    Vector Range is akin to a slice that you can use to navigate a vector
    """

    def __init__(self, vector: Vector[T], startindex: int = 0, endindex: int = -1):
        self.vector: Vector[T] = vector

        self.startindex = startindex

        if endindex < 0:
            self.endindex = len(self.vector) + endindex
        else:
            self.endindex = endindex

    @property
    def id(self) -> str:
        return self.vector.id

    def __getitem__(self, key):
        if isinstance(key, slice):
            raise NotImplementedError("Need to implement the slice")
        if self.startindex <= self.endindex:
            return self.vector[self.startindex + key]
        else:
            return self.vector[self.endindex - key]

    def __iter__(self):
        if self.startindex <= self.endindex:
            return iter(self.vector[self.startindex : self.endindex + 1])
        else:
            return reversed((self.vector[self.startindex : self.endindex + 1]))

    def __len__(self) -> int:
        return abs(self.startindex - self.endindex) + 1

    def __str__(self) -> str:
        return "<VectorRange::Vector - {0} [{1} : {2}]>".format(
            self.vector.id, self.startindex, self.endindex
        )

    @staticmethod
    def get_range_from_vector(
        vector: Vector[T],
        startindex: Optional[int] = None,
        endindex: Optional[int] = None,
    ) -> VectorRange:
        """Returns a VectorRange from a vector

        Args:
            vector (Vector[T]): Vector that want to be able to go through
            startindex (Optional[int], optional): the start index of the range. Defaults to None.
            endindex (Optional[int], optional): the end index of the range. Defaults to None.

        Returns:
            VectorRange: Vector range for the given indices
        """
        start = startindex if startindex is not None else vector.startindex
        end = endindex if endindex is not None else vector.endindex
        ret = VectorRange(vector, start, end)

        return ret
