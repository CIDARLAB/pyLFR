class VectorRange:
    def __init__(self, vector, startindex: int, endindex: int):
        self.vector = vector
        if startindex is None:
            self.startindex = 0
        else:
            self.startindex = startindex

        if endindex is None:
            self.endindex = len(self.vector) - 1
        else:
            self.endindex = endindex

    @property
    def id(self):
        return self.vector.id

    def __getitem__(self, key: int):
        return self.vector[self.startindex + key]

    def __iter__(self):
        return iter(self.vector[self.startindex:self.endindex+1])

    def __len__(self):
        return abs(self.startindex - self.endindex) + 1

    def __str__(self):
        return "< VectorRange : {0} [{1} : {2}]>".format(self.vector.id, self.startindex, self.endindex)
