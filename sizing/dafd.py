from mint.mintcomponent import MINTComponent
from pyparchmint.component import Component
from mint.mintdevice import MINTDevice
from typing import Iterator
from DAFD.bin.DAFD_Interface import DAFD_Interface

class Constraint:

    def __init__(self, component:MINTComponent) -> None:
        self.__component = component
        self.__constraint_key = None
        self.__target_value = None
        self.__min_value = None
        self.__max_value = None

    @property
    def key(self):
        return self.__constraint_key

    def add_target_constraint(self, key:str, value:str) -> None:
        self.__target_value = value
        self.__constraint_key = key

    def get_target_constraint(self):
        return self.__target_value

    def add_min_constraint(self, key:str, value:str) -> None:
        self.__min_value = value
        self.__constraint_key = key

    def get_min_constraint(self):
        return self.__min_value

    def add_max_constraint(self, key:str, value:str) -> None:
        self.__max_value = value
        self.__constraint_key = key

    def get_max_constraint(self):
        return self.__max_value

class PerformanceConstraint(Constraint):

    def __init__(self, component:MINTComponent) -> None:
        super().__init__(component)

class GeometryConstraint(Constraint):

    def __init__(self, component, MINTComponent) -> None:
        super().__init__(component)

class FunctionalConstraint(Constraint):
    
    def __init__(self, component, MINTComponent) -> None:
        super().__init__(component)

class MaterialConstraint(Constraint):

    def __init__(self, component):
        super().__init__(component)

class DAFDSizingAdapter:

    def __init__(self, device: MINTDevice) -> None:
        self.__device = device
        self.solver = DAFD_Interface()

    def size_droplet_generator(self, constriants: Iterator[Constraint]) -> None:
        #TODO: Check the type of the component and pull info from DAFD Interface
        targets_dict = dict()
        constriants_dict = dict()

        for constraint in constriants:
            if isinstance(constraint, FunctionalConstraint):
                if constraint.key == 'generation_rate':
                    targets_dict['generation_rate'] = constraint.get_target_constraint('generation_rate')
            elif isinstance(constraint, PerformanceConstraint):
                if constraint.key == 'generation_rate':
                    targets_dict['generation_rate']
            elif isinstance(constraint, GeometryConstraint):
                pass
        
        results = self.solver.runInterp(targets_dict, constriants_dict)
        return results

    def size_component(self, technology:str, constriants: Iterator[PerformanceConstraint]) -> None:
        if technology == "DROPLET GENERATOR":
            self.size_droplet_generator(constriants)
        else:
            print("Error: {} is not supported".format(technology))

