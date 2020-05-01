from mint.mintcomponent import MINTComponent
from pyparchmint.component import Component
from mint.mintdevice import MINTDevice
from typing import Iterator
from DAFD.bin.DAFD_Interface import DAFD_Interface

class Constraint:

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

class PerformanceConstraint(Constraint):

    def __init__(self, component:MINTComponent) -> None:
        super().__init__(component)

class GeometryConstraint(Constraint):

    def __init__(self, component, MINTComponent) -> None:
        super().__init__(component)

class FunctionalConstraint(Constraint):
    
    def __init__(self, component, MINTComponent) -> None:
        super().__init__(component)


class DAFDSizingAdapter:

    def __init__(self, device: MINTDevice) -> None:
        self.__device = device
        self.solver = DAFD_Interface()

    def size_performance_constraints(self, constriants: Iterator[PerformanceConstraint]) -> None:
        #TODO: Check the type of the component and pull info from DAFD Interface
        targets = dict()
        constriants = dict()
        results = self.solver.runInterp(targets, constriants)
        return results

