class VectorRange:
    def __init__(self, vector, startindex: int, endindex: int):
        self.vector = vector
        self.startindex = startindex
        self.endindex = endindex

    def __getitem__(self, key: int):
        return self.vector[self.startindex + key]

    def __len__(self):
        return abs(self.startindex - self.endindex + 1)
