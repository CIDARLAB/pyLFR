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
    """
    IO Types for the fignode
    """

    FLOW_INPUT = 1
    FLOW_OUTPUT = 2
    CONTROL = 3


class FIGNode:
    """The fundamental unit of the fluid interaction graph

    All the fignodes are build on top of this.
    """

    def __init__(self, id: str) -> None:
        """Creates a new instance of FIGNode

        Args:
            id (str): unique ID of the fignode
        """
        self._id: str = id

    @property
    def ID(self) -> str:
        """Returns the ID of the fignode

        Returns:
            str: ID of the fignode
        """
        return self._id

    @property
    def match_string(self):
        """Returns the Match String

        For the fig node the match string is "-"

        Returns:
            _type_: _description_
        """
        return "-"

    def __str__(self) -> str:
        return self.ID

    def __eq__(self, other):
        if isinstance(other, FIGNode):
            return self.ID == other.ID
        else:
            return False

    def rename(self, id: str) -> None:
        """Renames the ID of the fignode

        Args:
            id (str): the new ID for the fignode
        """
        self._id = id

    def __hash__(self) -> int:
        return hash(hex(id(self)))


class ValueNode(FIGNode):
    """FIGNodes that carries the value that you
    use to operate on the fluid interaction graph
    """

    def __init__(self, id: str, val: float) -> None:
        """Creates a new instance of ValueNode

        Args:
            id (str): ID of the value node
            val (float): value that we need to store on the node
        """
        super(ValueNode, self).__init__(id)
        self._value = val

    @property
    def value(self) -> float:
        """Returns the value stored on the node

        Returns:
            float: value stored on the node
        """
        return self._value

    @property
    def match_string(self) -> str:
        """Returns the match string

        Returns:
            str: the value fo the match_string
        """
        return "VALUE"

    def __str__(self) -> str:
        return "VALUE - {}".format(self._value)


class Flow(FIGNode):
    """
    Flow node is the node used represent fluids flowing around
    node that we use
    """

    def __init__(self, id: str) -> None:
        """Creates a new instance of Flow

        Args:
            id (str): id of the flow node
        """
        super(Flow, self).__init__(id)

    @property
    def match_string(self):
        """Returns the match string

        Returns:
            str: the value fo the match_string
        """
        return "FLOW"

    def __str__(self) -> str:
        return "FLOW - {}".format(self.ID)


class IONode(Flow):
    """
    The IONode is used to identify ports (inputs, outputs and control)
    are represented using this fig node
    """

    def __init__(self, id: str, iotype: Optional[IOType] = None) -> None:
        """Creates a new IONode

        Args:
            id (str): ID of the IONode
            iotype (Optional[IOType], optional): IOType of the node. Defaults to None.
        """
        super(IONode, self).__init__(id)
        if iotype is None:
            self._type = IOType.FLOW_INPUT
        else:
            self._type = iotype

    @property
    def type(self) -> IOType:
        """Returns the IOType of the node

        Raises:
            ValueError: If no IOType is not assigned

        Returns:
            IOType: Type of IO for the node
        """
        if self._type is None:
            raise ValueError("Type not set for IO: {}".format(self.ID))
        return self._type

    @type.setter
    def type(self, iotype: IOType) -> None:
        """Sets the IOType of the node

        Args:
            iotype (IOType): IOType we want to set
        """
        self._type = iotype

    def __str__(self) -> str:
        return "IO - Name: {0.ID}, Type : {0.type}".format(self)

    @property
    def match_string(self) -> str:
        """Returns the match string

        Returns:
            str: the value fo the match_string
        """
        return "IO"


class Storage(Flow):
    """
    The Storage Node is the node that we use for represnting storage units
    where flow stops.
    """

    def __init__(self, id: str) -> None:
        """Creates a new Storage element

        Args:
            id (str): ID of the fignode
        """
        super(Storage, self).__init__(id)

    @property
    def match_string(self) -> str:
        """Returns the match string

        Returns:
            str: the value fo the match_string
        """
        return "STORAGE"

    def __str__(self) -> str:
        return "STORAGE - {}".format(self.ID)


class Pump(Flow):
    """The pump element is a node that represents
    active flow movement within the fluid interaction
    graph
    """

    def __init__(self, id: str) -> None:
        """Creates a new instance of a Pump elemeent

        Args:
            id (str): ID of the pump
        """
        super(Pump, self).__init__(id)

    @property
    def match_string(self) -> str:
        """Returns the match string

        Returns:
            str: the value fo the match_string
        """
        return "PUMP"

    def __str__(self) -> str:
        return "PUMP - {}".format(self.ID)


class Signal(FIGNode):
    """
    The signal node represents the control signal
    that flows through the device
    """

    def __init__(self, id: str) -> None:
        """Creates a new instance of the
        signal node

        Args:
            id (str): ID of the node
        """
        super(Signal, self).__init__(id)

    @property
    def match_string(self):
        """Returns the match string

        Returns:
            str: the value fo the match_string
        """
        return "SIGNAL"

    def __str__(self) -> str:
        return "SIGNAL - {}".format(self.ID)
