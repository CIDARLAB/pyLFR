from typing import List, Optional

from pymint import MINTComponent

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


class Constraint:
    def __init__(self) -> None:
        self.__constraint_key = None

        # Store here if its '='
        # Also store here when its '<=' and '>='
        self.__target_value = None

        # Store here if its '>'
        self.__min_value = None

        # Store here if its '<'
        self.__max_value = None

        self.__unit_string: Optional[str] = None

    @property
    def unit(self) -> Optional[str]:
        return self.__unit_string

    @unit.setter
    def unit(self, value: str) -> None:
        self.__unit_string = value

    @property
    def key(self):
        return self.__constraint_key

    def add_target_value(self, key: str, value: float) -> None:
        self.__target_value = value
        self.__constraint_key = key

    def get_target_value(self):
        return self.__target_value

    def add_min_value(self, key: str, value: float) -> None:
        self.__min_value = value
        self.__constraint_key = key

    def get_min_value(self):
        return self.__min_value

    def add_max_value(self, key: str, value: float) -> None:
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
    def __init__(self, component: MINTComponent):
        super().__init__()
        self.__constraints: List[Constraint] = []
        self.__component: Optional[MINTComponent] = component

    def add_constraint(self, constraint: Constraint) -> None:
        constraint = FunctionalConstraint()
        self.__constraints.append(constraint)

    @property
    def component(self) -> Optional[MINTComponent]:
        return self.__component

    def __len__(self):
        return len(self.__constraints)

    def __getitem__(self, key: int):
        if key > len(self.__constraints) - 1:
            raise IndexError()
        return self.__constraints[key]
