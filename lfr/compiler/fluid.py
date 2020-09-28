class Fluid(object):
    def __init__(self, id: str):
        self.id = id

    def __str__(self) -> str:
        return self.id

    def __eq__(self, other) -> bool:
        return self.id == other.id
