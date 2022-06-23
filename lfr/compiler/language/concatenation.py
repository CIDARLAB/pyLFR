from typing import Optional

from lfr.compiler.language.vectorrange import VectorRange


class Concatenation:
    def __init__(self, ranges=None):
        self.ranges = []
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

        ret = VectorRange(self, start, end)

        return ret
