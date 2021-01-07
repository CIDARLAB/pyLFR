from typing import List, Optional
from pymint import MINTComponent


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
