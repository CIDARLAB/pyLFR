from compiler.fluid import Fluid


class Storage(Fluid):
    def __init__(self, id: str):
        super.id = id
