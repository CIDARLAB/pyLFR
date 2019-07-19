class Fluid(object):
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return self.id

    def __eq__(self, other):
        return self.id == other.id
