from lfr.compiler.language.vectorrange import VectorRange


class Vector:
    def __init__(self, id: str, vectortype=None, startindex: int = 0, endindex: int = 0):
        self.id = id
        self.startindex = startindex
        self.endindex = endindex
        self.vec = []

        if vectortype is not None:
            # If its a singular item avoid the indexing
            if len(self) == 1:
                self.vec.append(vectortype(self.id))
            else:
                for i in range(len(self)):
                    self.vec.append(vectortype(self.id + "_" + str(i)))

    def __len__(self):
        return abs(self.startindex - self.endindex)+1

    def get_items(self) -> list:
        return self.vec

    def get_range(self, startindex: int = None, endindex: int = None) -> VectorRange:
        start = startindex if startindex is not None else self.startindex
        end = endindex if endindex is not None else self.endindex
        ret = VectorRange(self, start, end)

        return ret

    def __getitem__(self, key: int):
        if isinstance(key, slice):
            start, stop, step = key.indices(len(self.vec))
            return [self.vec[i] for i in range(start, stop, step)]
        if key > len(self.vec) - 1:
            raise IndexError()
        return self.vec[key]

    @classmethod
    def create_from_list_things(cls, id: str, list_of_things):
        ret = cls(id)
        ret.vec = list_of_things
        ret.startindex = 0
        ret.endindex = len(list_of_things) - 1
        return ret
