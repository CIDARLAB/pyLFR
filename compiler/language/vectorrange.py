class VectorRange:
    def __init__(self, vector, startindex: int, endindex: int):
        self.vector = vector
        self.startindex = startindex
        self.endindex = endindex

    # def get_id(self) -> str:
    #     return self.vector.id

    @property
    def id(self):
        return self.vector.id

    def __getitem__(self, key: int):
        return self.vector[self.startindex + key]

    def __len__(self):
        return abs(self.startindex - self.endindex + 1)

    def __str__(self):     
        return "< VectorRange : {0} [{1} : {2}]>".format(self.vector.id, self.startindex, self.endindex)