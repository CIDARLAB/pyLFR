from compiler.language.vectorrange import VectorRange


class Concatenation:
    def __init__(self, ranges: [VectorRange] = None):
        self.ranges = []
        if ranges is not None:
            self.ranges = ranges

    def __getitem__(self, key: int):
        # TODO: Check if the logic is correct
        offset = 0
        for vrange in self.ranges:
            if key < len(vrange) + offset:
                return vrange[key - offset]
            else:
                offset = offset + len(vrange)

    def __len__(self):
        size = 0
        for vrange in self.ranges:
            size = size + len(vrange)
        return size
