from enum import Enum
from typing import Optional

MATCH_STRING_ORDERING = [
    "IO",
    "FLOW",
    "VALUE",
    "STORAGE",
    "SIGNAL",
    "DISTRIBUTE-AND",
    "DISTRIBUTE-OR",
]


class IOType(Enum):
    FLOW_INPUT = 1
    FLOW_OUTPUT = 2
    CONTROL = 3


class FIGNode:
    def __init__(self, id: str) -> None:
        self._id: str = id

    @property
    def ID(self):
        return self._id

    @property
    def match_string(self):
        return "-"

    def __str__(self) -> str:
        return self.ID

    def __eq__(self, other):
        if isinstance(other, FIGNode):
            return self.ID == other.ID
        else:
            return False

    def rename(self, id: str) -> None:
        self._id = id

    def __hash__(self) -> int:
        return hash(hex(id(self)))


class ValueNode(FIGNode):
    def __init__(self, id: str, val: float) -> None:
        super(ValueNode, self).__init__(id)
        self._value = val

    @property
    def value(self):
        return self._value

    @property
    def match_string(self):
        return "VALUE"

    def __str__(self) -> str:
        return "VALUE - {}".format(self._value)


class Flow(FIGNode):
    def __init__(self, id) -> None:
        super(Flow, self).__init__(id)

    @property
    def match_string(self):
        return "FLOW"

    def __str__(self) -> str:
        return "FLOW - {}".format(self.ID)


class IONode(Flow):
    def __init__(self, id: str, iotype: Optional[IOType] = None) -> None:
        super(IONode, self).__init__(id)
        if iotype is None:
            self._type = IOType.FLOW_INPUT
        else:
            self._type = iotype

    @property
    def type(self) -> IOType:
        if self._type is None:
            raise ValueError("Type not set for IO: {}".format(self.ID))
        return self._type

    @type.setter
    def type(self, iotype: IOType) -> None:
        self._type = iotype

    def __str__(self) -> str:
        return "IO - Name: {0.ID}, Type : {0.type}".format(self)

    @property
    def match_string(self):
        return "IO"


class Storage(Flow):
    def __init__(self, id: str) -> None:
        super(Storage, self).__init__(id)

    @property
    def match_string(self):
        return "STORAGE"

    def __str__(self) -> str:
        return "STORAGE - {}".format(self.ID)


class Pump(Flow):
    def __init__(self, id: str) -> None:
        super(Pump, self).__init__(id)

    @property
    def match_string(self) -> str:
        return "PUMP"

    def __str__(self) -> str:
        return "PUMP - {}".format(self.ID)


class Signal(FIGNode):
    def __init__(self, id: str) -> None:
        super(Signal, self).__init__(id)

    @property
    def match_string(self):
        return "SIGNAL"

    def __str__(self) -> str:
        return "SIGNAL - {}".format(self.ID)
