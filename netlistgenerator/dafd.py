from mint.mintcomponent import MINTComponent
from pyparchmint.component import Component
from mint.mintdevice import MINTDevice
from typing import List
from DAFD.bin.DAFD_Interface import DAFD_Interface


class Constraint:
    def __init__(self) -> None:
        self.__constraint_key = None
        self.__target_value = None
        self.__min_value = None
        self.__max_value = None

    @property
    def key(self):
        return self.__constraint_key

    def add_target_value(self, key:str, value:str) -> None:
        self.__target_value = value
        self.__constraint_key = key

    def get_target_value(self):
        return self.__target_value

    def add_min_value(self, key:str, value:str) -> None:
        self.__min_value = value
        self.__constraint_key = key

    def get_min_value(self):
        return self.__min_value

    def add_max_value(self, key:str, value:str) -> None:
        self.__max_value = value
        self.__constraint_key = key

    def get_max_value(self):
        return self.__max_value



class PerformanceConstraint(Constraint):

    def __init__(self) -> None:
        super().__init__()

class GeometryConstraint(Constraint):

    def __init__(self) -> None:
        super().__init__()

class FunctionalConstraint(Constraint):
    
    def __init__(self) -> None:
        super().__init__()

class MaterialConstraint(Constraint):

    def __init__(self):
        super().__init__()

class ConstraintList:
    def __init__(self):
        super().__init__()
        self.__constraints:List[Constraint] = []
        self.__component:MINTComponent = None
    
    def add_constraint(self, constraint: Constraint) -> None:
        constraint = FunctionalConstraint()
        self.__constraints.append(constraint)

    @property
    def component(self) -> MINTComponent:
        return self.__component

    def __len__(self):
        return len(self.__constraints)

    def __getitem__(self, key: int):
        if key > len(self.__constraints) - 1:
            raise IndexError()
        return self.__constraints[key]

class DAFDSizingAdapter:

    def __init__(self, device: MINTDevice) -> None:
        self.__device = device
        self.solver = DAFD_Interface()

    def size_droplet_generator(self, constriants: ConstraintList) -> None:
        #TODO: Check the type of the component and pull info from DAFD Interface
        targets_dict = dict()
        constriants_dict = dict()

        for constraint in constriants:
            if isinstance(constraint, FunctionalConstraint):
                if constraint.key == 'volume':
                    #r≈0.62035V1/3
                    volume = constraint.get_target_value()
                    targets_dict['droplet_size'] =  pow(volume,1/3) * 0.62035 * 2
            elif isinstance(constraint, PerformanceConstraint):
                if constraint.key == 'generation_rate':
                    generate_rate = constraint.get_target_value()
                    targets_dict['generation_rate'] = generate_rate
            elif isinstance(constraint, GeometryConstraint):
                raise Exception("Error: Geometry constraint not defined")
        
        results = self.solver.runInterp(targets_dict, constriants_dict)
        
        #TODO: Figure out how to propagate the results to the rest of the design
        pass
        
        

    def size_component(self, technology:str, constriants: List[PerformanceConstraint]) -> None:
        if technology == "DROPLET GENERATOR":
            self.size_droplet_generator(constriants)
        else:
            print("Error: {} is not supported".format(technology))

