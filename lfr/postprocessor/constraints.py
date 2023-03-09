from enum import Enum
from typing import List, Optional

from parchmint import Component

"""
    # TODO - Generate the constraints in the right way:
    # GeometryConstraint - if the parameters exist, add them into it
    # PerformanceConstraint - if this is a tolerance parameter
    # FunctionalConstraint - These are target for inverse design
    # MaterialConstraint - I guess this would be checked with material constriant
    if isinstance(constriant, MaterialConstraint):
        # TODO - Add the parameters to the inverse desing constraints
        # (if it exists)
        # TODO - Figure out how one might want to use the material
        # constraints later on
        raise NotImplementedError()
    else:
        # This the bucketlist scenario
        # if constriant.key in primitive_to_use.inverse_design_query_params
        pass

    if isinstance(constriant, PerformanceConstraint):
        # TODO - Figure out how to add it to the tolerance settings
        raise NotImplementedError()
    elif isinstance(constriant, GeometryConstraint):
        # TODO - Figure out a way to check if the param exists
        # for the primitive

        # TODO - Add the parameter to the user_defined_values
        # TODO - Also add them to the Inverse design constraints
        raise NotImplementedError()
    elif isinstance(constriant, FunctionalConstraint):
        # TODO - Check if the parameter exists in the inverse design
        # parameters and set up the targets for this
        raise NotImplementedError()
"""


class ConstriantType(Enum):
    MIN = "MIN"
    MAX = "MAX"
    TARGET = "TARGET"


class Constraint:
    """Base Constraints Class that accepts the different
    kinds of constraints that will be used throughout the
    postprocessing.

    Individual constraints are currently not uniquely identifyable
    Generate the constraint and set the corresponding min max target values

    TODO - Maybe simplify the interfacet to automatically check the constraint
     type while retrieving data
    """

    def __init__(self) -> None:
        # This will always be something
        self._constraint_key = ""

        # Constraint Type that we will use in the future
        self._constraint_type: ConstriantType = ConstriantType.TARGET

        # Store here if its '='
        # Also store here when its '<=' and '>='
        self._target_value: Optional[float] = None

        # Store here if its '>'
        self._min_value: Optional[float] = None

        # Store here if its '<'
        self._max_value: Optional[float] = None

        self._unit_string: Optional[str] = None

    @property
    def unit(self) -> Optional[str]:
        return self._unit_string

    @unit.setter
    def unit(self, value: str) -> None:
        self._unit_string = value

    @property
    def key(self):
        return self._constraint_key

    def add_target_value(self, key: str, value: float) -> None:
        self._constraint_type = ConstriantType.TARGET
        self._target_value = value
        self._constraint_key = key

    def get_target_value(self) -> Optional[float]:
        return self._target_value

    def add_min_value(self, key: str, value: float) -> None:
        self._constraint_type = ConstriantType.MIN
        self._min_value = value
        self._constraint_key = key

    def get_min_value(self) -> Optional[float]:
        return self._min_value

    def add_max_value(self, key: str, value: float) -> None:
        self._constraint_type = ConstriantType.MAX
        self._max_value = value
        self._constraint_key = key

    def get_max_value(self) -> Optional[float]:
        return self._max_value


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
    def __init__(self) -> None:
        super().__init__()


class ConstraintList:
    """Stores the constraints for a specific component

    This is a mapping between a component and its constraints
    """

    def __init__(self, component: Component):
        """Creates a new instance of a constraint list

        Args:
            component (Component): Component against which we want to store the constraints
        """
        super().__init__()
        self.__constraints: List[Constraint] = []
        self.__component: Optional[Component] = component

    def add_constraint(self, constraint: Constraint) -> None:
        self.__constraints.append(constraint)

    @property
    def component(self) -> Optional[Component]:
        return self.__component

    def __len__(self):
        return len(self.__constraints)

    def __getitem__(self, key: int):
        if key > len(self.__constraints) - 1:
            raise IndexError()
        return self.__constraints[key]
