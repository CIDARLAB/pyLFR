from mint.mintparams import MINTParams
from pyparchmint.component import Component

class MINTComponent(Component):

    def __init__(self, name:str , technology:str, params:dict) -> None:
        super().__init__()
        self.name = name
        self.ID = name
        self.entity = technology
        self.params = MINTParams(params)

    def toMINT(self) -> str:
        ret = "{} {} {};".format(self.entity, self.name, self.params.toMINT())
        return ret