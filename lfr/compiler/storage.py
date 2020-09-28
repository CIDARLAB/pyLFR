from lfr.compiler.fluid import Fluid


class Storage(Fluid):
    def __init__(self, id: str):
        self.id = id
