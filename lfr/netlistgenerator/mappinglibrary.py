from typing import Dict, List, Tuple

from lfr.fig.interaction import InteractionType
from lfr.netlistgenerator.connection_primitive import ConnectionPrimitive
from lfr.netlistgenerator.primitive import Primitive, ProceduralPrimitive

MatchPatternEntry = Tuple[str, str, str]


class MappingLibrary:
    """Mapping Lirbrary containing all the primitives we can match against"""

    def __init__(self, name: str) -> None:
        """Initializes the mapping library.

        Args:
            name (str): Name of the mapping library
        """
        self.__name = name
        self.__mix_operators: List[Primitive] = []
        self.__meter_operators: List[Primitive] = []
        self.__seive_operators: List[Primitive] = []
        self.__dilute_operators: List[Primitive] = []
        self.__divide_operators: List[Primitive] = []
        self.__technology_process_operators: List[Primitive] = []
        self.__storage_primitives: List[Primitive] = []
        self.__pump_primitives: List[Primitive] = []
        self.__io_primitives: List[Primitive] = []
        self.__all_primitives: Dict[str, Primitive] = {}
        self.__procedural_primitves: List[ProceduralPrimitive] = []
        self.__connection_primitives: List[ConnectionPrimitive] = []
        self._default_IO_primitive = None

    @property
    def name(self) -> str:
        """Returns the name of the library.

        Returns:
            str: Name of the library
        """
        return self.__name

    def add_io_entry(self, primitive: Primitive) -> None:
        """Adds a primitive to the list of IO primitives.

        Args:
            primitive (Primitive): Primitive to add to the list of IO primitives
        """
        self.__io_primitives.append(primitive)
        self.__all_primitives[primitive.uid] = primitive

    def add_operator_entry(
        self, primitive: Primitive, interaction_type: InteractionType
    ) -> None:
        """Adds a primitive to the list of operators for the given interaction type.

        Args:
            primitive (Primitive): Primitive to add to the list of operators
            interaction_type (InteractionType): Type of interaction to add the primitive to
        """
        if interaction_type is InteractionType.MIX:
            self.__mix_operators.append(primitive)
            self.__all_primitives[primitive.uid] = primitive
        elif interaction_type is InteractionType.SIEVE:
            self.__seive_operators.append(primitive)
            self.__all_primitives[primitive.uid] = primitive
        elif interaction_type is InteractionType.DILUTE:
            self.__dilute_operators.append(primitive)
            self.__all_primitives[primitive.uid] = primitive
        elif interaction_type is InteractionType.METER:
            self.__meter_operators.append(primitive)
            self.__all_primitives[primitive.uid] = primitive
        elif interaction_type is InteractionType.DIVIDE:
            self.__divide_operators.append(primitive)
            self.__all_primitives[primitive.uid] = primitive
        else:
            self.__technology_process_operators.append(primitive)
            self.__all_primitives[primitive.uid] = primitive

    def add_entry(self, primitive: Primitive) -> None:
        """Adds a primitive to the library."""
        self.__all_primitives[primitive.uid] = primitive

    def add_procedural_entry(self, primitive: ProceduralPrimitive) -> None:
        """Adds a procedural primitive to the library.

        Args:
            primitive (ProceduralPrimitive): Primitive to add to the library
        """
        self.__procedural_primitves.append(primitive)
        self.__all_primitives[primitive.uid] = primitive

    def add_storage_entry(self, primitive: Primitive) -> None:
        """Adds a primitive to the list of storage primitives.

        Args:
            primitive (Primitive): Primitive to add to the list of storage primitives
        """
        self.__storage_primitives.append(primitive)
        self.__all_primitives[primitive.uid] = primitive

    def add_pump_entry(self, primitive: Primitive) -> None:
        """Adds a primitive to the list of pump primitives.

        Args:
            primitive (Primitive): Primitive to add to the list of pump primitives
        """
        self.__pump_primitives.append(primitive)
        self.__all_primitives[primitive.uid] = primitive

    def get_storage_entries(self) -> List[Primitive]:
        """Returns the list of storage primitives.

        Returns:
            List[Primitive]: List of storage primitives
        """
        return self.__storage_primitives

    def get_pump_entries(self) -> List[Primitive]:
        """Returns the list of pump primitives.

        Returns:
            List[Primitive]: List of pump primitives
        """
        return self.__pump_primitives

    def get_default_IO(self) -> Primitive:
        """Returns the default IO primitive.

        Returns:
            Primitive: Default IO primitive
        """
        if self._default_IO_primitive is None:
            return self.__io_primitives[0]
        else:
            return self._default_IO_primitive

    def get_operators(self, interaction_type: InteractionType) -> List[Primitive]:
        """Gets the primitives for the given interaction type.

        Args:
            interaction_type (InteractionType): Type of interaction to get primitives

        Returns:
            List[Primitive]: List of primitives for the given interaction type
        """
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

    def get_primitive(self, uid: str) -> Primitive:
        """Returns the primitive with the given uid.

        Args:
            uid (str): UID of the primitive to return

        Raises:
            KeyError: If the primitive is not found

        Returns:
            Primitive: The primitive with the given uid
        """
        if uid in self.__all_primitives:
            return self.__all_primitives[uid]

        raise KeyError("No primitive with uid: " + uid)

    def get_primitives(self, technology_string: str) -> List[Primitive]:
        """Get the primitive with the given technology string.


        Args:
            technology_string (str): MINT String around which the
            primitive is defined

        Returns:
            List[Primitive]: List of primitives with the given technology string.
            Returns an empty list if no primitives are found.
        """
        ret = []
        for primitive in self.__all_primitives.values():
            if primitive.mint == technology_string:
                ret.append(primitive)
        return ret

    def has_primitive(self, technology_string: str) -> bool:
        """Checks whether the library contains a primitive with the given technology string.


        Args:
            technology_string (str): MINT String of the technology

        Returns:
            bool: whether it exists or not
        """
        # Go through each of the entries in the all_primitives dictionary and see if the
        # technology string is in there.
        ret = False
        for primitive in self.__all_primitives.values():
            if primitive.mint == technology_string:
                ret = True
                break

        return ret

    def get_match_patterns(self) -> List[MatchPatternEntry]:
        """Returns the match patterns for the library.

        Returns:
            List[MatchPattern]: Match patterns for the library
        """
        ret = []
        for primitive in self.__all_primitives.values():
            ret.append((primitive.uid, primitive.mint, primitive.match_string))

        return ret

    def add_connection_entry(self, primitive: ConnectionPrimitive) -> None:
        """Adds a primitive to the list of connection primitives.

        Args:
            primitive (Primitive): Primitive to add to the list of connection primitives
        """
        self.__connection_primitives.append(primitive)
        self.__all_primitives[primitive.uid] = primitive

    def get_default_connection_entry(self) -> ConnectionPrimitive:
        """Returns the default connection primitive.

        Returns:
            ConnectionPrimitive: Default connection primitive
        """
        return self.__connection_primitives[0]
