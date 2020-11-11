from enum import Enum
from typing import List


class ExplicitMappingType(Enum):
    FLUID_INTERACTION = 0
    STORAGE = 1
    NETWORK = 2


class ExplicitMapping(object):

    def __init__(self, mapping_type: ExplicitMappingType = ExplicitMappingType.FLUID_INTERACTION):
        self._startlist: List[str] = []
        self._endlist: List[str] = []
        self._technology: str = ''
        self._operator: str = ''
        self._mapping_type: ExplicitMappingType = mapping_type

    @property
    def startlist(self):
        return self._startlist

    @property
    def endlist(self):
        return self._endlist

    @property
    def technology(self):
        return self._technology

    @property
    def type(self):
        return self._mapping_type

    def map(self, netlist, fig):
        # TODO: Basically go through the start and stop and insert a bunch of components between the
        # start and end and remove the correspoinding connections.
        # TODO: In scenarios where there are inbetween nodes, we probably need to be more careful and
        # this might not be the right place to do that kind of mapping
        pass
