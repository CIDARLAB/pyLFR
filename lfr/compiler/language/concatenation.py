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

    def __getitem__(self, key: int):
        # TODO: Check if the logic is correct
        offset = 0
        for vrange in self.ranges:
            if key < len(vrange) + offset:
                return vrange[key - offset]
            else:
                offset = offset + len(vrange)

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

    def get_range(self, startindex: int = None, endindex: int = None) -> VectorRange:
        start = startindex if startindex is not None else 0
        end = endindex if endindex is not None else len(self)-1
        # vec = []
        # for r in self.ranges:
        #     vec.extend(r)
        ret = VectorRange(self, start, end)

        return ret