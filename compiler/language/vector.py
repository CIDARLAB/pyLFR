from compiler.language.vectorrange import VectorRange


class Vector:
    def __init__(self, id: str, type, startindex: int, endindex: int):
        self.id = id
        self.startindex = startindex
        self.endindex = endindex
        self.vectormap = None
        self.vec = []

        # If its a singular item avoid the indexing
        if len(self) is 1:
            self.vec.append(type(self.id))
        else:
            for i in range(len(self)):
                self.vec.append(type(self.id + "_" + str(i)))

    def __len__(self):
        return abs(self.startindex - self.endindex)+1

    def get_items(self) -> []:
        return self.vec

    def get_range(self, startindex:int = None, endindex:int = None) -> VectorRange:
        start = 0 if startindex is None else self.startindex
        end = 1 if endindex is None else self.endindex
        ret = VectorRange(self, start, end)

        return ret

    def __getitem__(self, key: int):
        if key > len(self.vec) - 1:
            raise IndexError()
        return self.vec[key]
