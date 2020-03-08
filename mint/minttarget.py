from pyparchmint.port import Port
from pyparchmint.target import Target


class MINTTarget(Target):
    def __init__(self, componentstring:str, portstring:str = None ) -> None:
        super().__init__()
        self.component = componentstring
        self.port = portstring

    def toMINT(self):
        ret = "{} {}".format(self.component, '' if self.port is None else self.port )
        return ret