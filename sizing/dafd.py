from mint.mintcomponent import MINTComponent
from pyparchmint.component import Component
from mint.mintdevice import MINTDevice
from typing import Iterator


class PerformanceConstraint:

    def __init__(self, component:MINTComponent) -> None:
        self.__component = component
        self.__target_values = dict()
        self.__min_values = dict()
        self.__max_values = dict()

    def add_target_constraint(self, key:str, value:str) -> None:
        self.__target_values[key] = value

    def add_min_constraint(self, key:str, value:str) -> None:
        self.__min_values = dict()

    def add_max_constraint(self, key:str, value:str) -> None:
        self.__max_values = dict()

class GeometryConstraint:

    def __init__(self, component, MINTComponent) -> None:
        self.__entity = component
        self.__target_values = dict()
        self.__min_values = dict()
        self.__max_values = dict()

class DAFDSizingAdapter:

    def __init__(self, device: MINTDevice) -> None:
        self.__device = device

    def size_performance_constraints(self, constriants: Iterator[PerformanceConstraint]) -> None:
        #TODO: Check the type of the component and pull info from DAFD Interface
        pass

