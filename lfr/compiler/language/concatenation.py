from __future__ import annotations

from typing import List, Optional
from lfr.compiler.language.vector import Vector

from lfr.compiler.language.vectorrange import VectorRange


class Concatenation:
    """
    A concatenation is the represetnation of mutiple
    vector ranges stitched togeter.

    TODO - A concatenation of concatenations should be a concatenation,
    while this needs to be tested more thoroughly, this is future work.
    """

    def __init__(self, ranges: List[VectorRange]):
        self.ranges: List[VectorRange] = []
        if ranges is not None:
            self.ranges = ranges
            name = "CONCAT"
            for r in ranges:
                name = name + "_" + r.id
            self.id = name

    def __getitem__(self, key):
        temp = []
        for vrange in self.ranges:
            temp.extend(vrange)

        return temp[key]

    def __iter__(self):
        vec = []
        for r in self.ranges:
            vec.extend(r)
        return iter(vec)

    def __len__(self):
        size = 0
        for vrange in self.ranges:
            size = size + len(vrange)
        return size

    def get_range(
        self, startindex: int = 0, endindex: Optional[int] = None
    ) -> VectorRange:
        start = startindex
        end = endindex if endindex is not None else len(self) - 1
        concatenated_data = []
        for data in self.ranges:
            concatenated_data.extend(data)
        concatenated_vector = Vector(
            self.id,
        )
        concatenated_vector.vec = concatenated_data
        ret = VectorRange(concatenated_vector, start, end)

        return ret
