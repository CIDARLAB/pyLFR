from enum import Enum


MATCH_STRING_ORDERING = [
    "IO",
    "FLOW",
    "VALUE",
    "STORAGE",
    "SIGNAL",
    "DISTRIBUTE-AND",
    'DISTRIBUTE-OR'
]


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
        if isinstance(other, FIGNode):
            return self.id == other.id
        else:
            False

    def rename(self, id: str) -> None:
        self._id = id


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
    def type(self) -> IOType:
        return self._type

    @type.setter
    def type(self, iotype: IOType) -> None:
        self._type = iotype

    def __str__(self) -> str:
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


class Pump(Flow):

    def __init__(self, id: str) -> None:
        super().__init__(id)

    @property
    def match_string(self) -> str:
        return "PUMP"


class Signal(FIGNode):

    def __init__(self, id: str) -> None:
        super().__init__(id)

    @property
    def match_string(self):
        return "SIGNAL"


class DistributeNode(FIGNode):

    def __init__(self, id: str) -> None:
        super().__init__(id)


class ANDAnnotation(DistributeNode):

    def __init__(self, id: str) -> None:
        super().__init__(id)

    @property
    def match_string(self):
        return "DISTRIBUTE-AND"


class ORAnnotation(DistributeNode):

    def __init__(self, id: str) -> None:
        super().__init__(id)

    @property
    def match_string(self):
        return "DISTRIBUTE-OR"


class NOTAnnotation(DistributeNode):

    def __init__(self, id: str) -> None:
        super().__init__(id)

    @property
    def match_string(self):
        return "DISTRIBUTE-NOT"
