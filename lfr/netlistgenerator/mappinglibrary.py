from typing import Dict, List

from lfr.fig.interaction import InteractionType
from lfr.netlistgenerator.primitive import Primitive, ProceduralPrimitive


class MappingLibrary:
    def __init__(self, name) -> None:
        self.__name = name
        self.__mix_operators = []
        self.__meter_operators = []
        self.__seive_operators = []
        self.__dilute_operators = []
        self.__divide_operators = []
        self.__technology_process_operators = []
        self.__storage_primitives = []
        self.__pump_primitives = []
        self.__io_primitives = []
        self.__all_primitives: Dict[str, Primitive] = {}
        self.__procedural_primitves: List[ProceduralPrimitive] = []
        self._default_IO_primitive = None

    @property
    def name(self) -> str:
        return self.__name

    def add_io_entry(self, primitive: Primitive) -> None:
        self.__io_primitives.append(primitive)
        self.__all_primitives[primitive.mint] = primitive

    def add_operator_entry(
        self, primitive: Primitive, interaction_type: InteractionType
    ) -> None:
        if interaction_type is InteractionType.MIX:
            self.__mix_operators.append(primitive)
            self.__all_primitives[primitive.mint] = primitive
        elif interaction_type is InteractionType.SIEVE:
            self.__seive_operators.append(primitive)
            self.__all_primitives[primitive.mint] = primitive
        elif interaction_type is InteractionType.DILUTE:
            self.__dilute_operators.append(primitive)
            self.__all_primitives[primitive.mint] = primitive
        elif interaction_type is InteractionType.METER:
            self.__meter_operators.append(primitive)
            self.__all_primitives[primitive.mint] = primitive
        elif interaction_type is InteractionType.DIVIDE:
            self.__divide_operators.append(primitive)
            self.__all_primitives[primitive.mint] = primitive
        else:
            self.__technology_process_operators.append(primitive)
            self.__all_primitives[primitive.mint] = primitive

    def add_procedural_entry(self, primitive: ProceduralPrimitive) -> None:
        self.__procedural_primitves.append(primitive)
        self.__all_primitives[primitive.mint] = primitive

    def add_storage_entry(self, primitive: Primitive) -> None:
        self.__storage_primitives.append(primitive)
        self.__all_primitives[primitive.mint] = primitive

    def add_pump_entry(self, primitive: Primitive) -> None:
        self.__pump_primitives.append(primitive)
        self.__all_primitives[primitive.mint] = primitive

    def get_storage_entries(self) -> List[Primitive]:
        return self.__storage_primitives

    def get_pump_entries(self) -> List[Primitive]:
        return self.__pump_primitives

    def get_default_IO(self) -> Primitive:
        if self._default_IO_primitive is None:
            return self.__io_primitives[0]
        else:
            return self._default_IO_primitive

    def get_operators(self, interaction_type: InteractionType) -> List[Primitive]:
        if interaction_type is InteractionType.MIX:
            return self.__mix_operators
        elif interaction_type is InteractionType.SIEVE:
            return self.__seive_operators
        elif interaction_type is InteractionType.DILUTE:
            return self.__dilute_operators
        elif interaction_type is InteractionType.METER:
            return self.__meter_operators
        elif interaction_type is InteractionType.DIVIDE:
            return self.__divide_operators
        else:
            return self.__technology_process_operators

    def get_primitive(self, technology_string: str) -> Primitive:
        return self.__all_primitives[technology_string]

    def has_primitive(self, technology_string: str) -> bool:
        return technology_string in self.__all_primitives.keys()
