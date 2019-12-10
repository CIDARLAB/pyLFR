from enum import Enum


class IOType(Enum):
    FLOW_INPUT = 1
    FLOW_OUTPUT = 2
    CONTROL = 3


class ModuleIO:
    def __init__(self, name, iotype=None):
        self.type = iotype
        self.id = name

    def __str__(self):
        return "Name: {0.id}, Type : {0.type}".format(self)
