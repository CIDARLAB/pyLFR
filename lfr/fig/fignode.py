from enum import Enum
from typing import overload


class IOType(Enum):
    FLOW_INPUT = 1
    FLOW_OUTPUT = 2
    CONTROL = 3


class FIGNode(object):

    def __init__(self, id: str) -> None:
        self._id: str = id

    @property
    def id(self):
        return self._id

    def __str__(self) -> str:
        return self.id

    def __eq__(self, other) -> bool:
        return self.id == other.id


class ValueNode(FIGNode):

    def __init__(self, id: str, val) -> None:
        super().__init__(id)
        self._value = val

    @property
    def value(self):
        return self._value

    @property
    def match_string(self):
        return "VALUE"


class Flow(FIGNode):

    def __init__(self, id) -> None:
        super().__init__(id)

    @property
    def match_string(self):
        return "FLOW"


class IONode(Flow):

    def __init__(self, id: str, iotype=None):
        super().__init__(id)
        self._type = iotype

    @property
    def type(self):
        return self._type

    @overload
    def __str__(self):
        return "Name: {0.id}, Type : {0.type}".format(self)

    @property
    def match_string(self):
        return "IO"


class Storage(Flow):

    def __init__(self, id: str) -> None:
        super().__init__(id)

    @property
    def match_string(self):
        return "STORAGE"


class Signal(FIGNode):

    def __init__(self, id: str) -> None:
        super().__init__(id)

    @property
    def match_string(self):
        return "SIGNAL"
