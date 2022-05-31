from enum import Enum
from typing import List, Optional

from lfr.fig.fignode import FIGNode, Flow


class InteractionType(Enum):
    TECHNOLOGY_PROCESS = 1  # Explicit Mapped operators
    MIX = 2  # +
    SIEVE = 3  # -
    METER = 4  # %
    DILUTE = 5  # *
    DIVIDE = 6  # /


class Interaction(Flow):

    INTERACTION_ID = 0

    def __init__(self, id: str, interaction_type: InteractionType) -> None:
        super().__init__(id)
        self._interaction_type: InteractionType = interaction_type
        self._input_fignodes: List[FIGNode] = []
        self._output_fignode: Optional[FIGNode] = None
        self._operator: str = ""

    @property
    def operator(self) -> str:
        return self._operator

    @operator.setter
    def operator(self, value):
        self._operator = value

    @property
    def type(self) -> InteractionType:
        return self._interaction_type

    @staticmethod
    def get_id(
        fluid1: FIGNode, fluid2: Optional[FIGNode] = None, operator_string: str = ""
    ) -> str:
        """Generates a unique ID for the interaction

        The user needs to provide atleast one fignode and the operator string to generate the ID.

        Args:
            fluid1 (FIGNode): First fignode
            fluid2 (Optional[FIGNode]): Second FIGNode
            operator_string (str): Operator String

        Raises:
            ValueError: If there is no fignode provided
            ValueError: If there is no operator string provided

        Returns:
            str: unique ID for the interaction
        """

        id = None

        # If no operator string is given then we cannot proceed
        if operator_string is None or operator_string == "":
            raise ValueError("Operator string cannot be None")

        if fluid1 is None:
            raise ValueError("id of fluid1 is found to be None")

        if fluid2 is not None:
            if fluid1.ID < fluid2.ID:
                id = fluid1.ID + "_" + operator_string + "_" + fluid2.ID
            else:
                id = fluid2.ID + "_" + operator_string + "_" + fluid1.ID
        else:
            id = fluid1.ID + "_" + operator_string

        id = id + "_" + str(Interaction.INTERACTION_ID)
        Interaction.INTERACTION_ID += 1
        return id

    @property
    def match_string(self):
        interaction_type = self.type
        if interaction_type is InteractionType.DILUTE:
            return "DILUTE"
        elif interaction_type is InteractionType.DIVIDE:
            return "DIVIDE"
        elif interaction_type is InteractionType.METER:
            return "METER"
        elif interaction_type is InteractionType.MIX:
            return "MIX"
        elif interaction_type is InteractionType.SIEVE:
            return "SIEVE"
        else:
            return "PROCESS"

    @staticmethod
    def get_operator_str(interaction_type: InteractionType, process_operator="") -> str:
        if interaction_type is InteractionType.DILUTE:
            return "DILUTE_(*)"
        elif interaction_type is InteractionType.DIVIDE:
            return "DIVIDE_(/)"
        elif interaction_type is InteractionType.METER:
            return "METER_(%)"
        elif interaction_type is InteractionType.MIX:
            return "MIX_(+)"
        elif interaction_type is InteractionType.SIEVE:
            return "SIEVE_(-)"
        else:
            return "PROCESS_({0})".format(process_operator)


class FluidFluidInteraction(Interaction):
    def __init__(
        self,
        fluid1: Flow,
        fluid2: Flow,
        interaction_type: InteractionType,
        interaction_data: Optional[str] = None,
    ) -> None:
        """Creates an interaction between two fluids

        Args:
            fluid1 (FIGNode): Fluid1 that needs to be included in the interaction
            fluid2 (FIGNode): Fluid2 that needs to be included in the interaction
            interaction_type (InteractionType, optional): Type of Fluid Interaction.
                Defaults to None.
            interaction_data (str, optional): Interaction data (typically used for
                fluid-number interactions). Defaults to None.
        """
        id = Interaction.get_id(
            fluid1, fluid2, Interaction.get_operator_str(interaction_type)
        )
        super().__init__(id, interaction_type)
        self._input_fignodes.append(fluid1)
        self._input_fignodes.append(fluid2)

    @property
    def fluids(self) -> List[FIGNode]:
        return self._input_fignodes


class FluidProcessInteraction(Interaction):
    def __init__(self, fluid: Flow, process_operator: str) -> None:
        """Creates an instance of a Fluidic Interaction that shows the process
        is happening on the fluid using a custom operator (typically unary)

        Args:
            fluid (FIGNode): [description]
            process_operator (str): [description]
        """
        operator_str = Interaction.get_operator_str(
            InteractionType.TECHNOLOGY_PROCESS, process_operator
        )
        self._operator = process_operator
        id = Interaction.get_id(fluid, operator_string=operator_str)
        super().__init__(id, InteractionType.TECHNOLOGY_PROCESS)
        self._input_fignodes.append(fluid)

    @property
    def fluid(self) -> FIGNode:
        return self._input_fignodes[0]


class FluidNumberInteraction(Interaction):
    def __init__(
        self, fluid: Flow, value: float, interaction_type: InteractionType
    ) -> None:
        """Creates an instance of a fluidic interactions shows that a fluid is
        interacting with a real number

        Args:
            fluid (FIGNode): [description]
            value (float): [description]
            interaction_type (InteractionType): [description]
        """
        # TODO: Add operator to this mix
        operator_str = Interaction.get_operator_str(interaction_type)
        id = Interaction.get_id(fluid1=fluid, operator_string=operator_str)
        super().__init__(id, interaction_type)
        self._input_fignodes.append(fluid)
        self._value: float = value

    @property
    def fluid(self) -> FIGNode:
        return self._input_fignodes[0]

    @property
    def value(self) -> float:
        return self._value


class FluidIntegerInteraction(Interaction):
    def __init__(
        self, fluid: Flow, value: int, interaction_type: InteractionType
    ) -> None:
        """Creates an instance of a fluidic interactions between integers and fluids

        Args:
            fluid (FIGNode): [description]
            value (int): [description]
            interaction_type (InteractionType): [description]
        """
        id = Interaction.get_id(
            fluid1=fluid, operator_string=Interaction.get_operator_str(interaction_type)
        )
        super().__init__(id, interaction_type)
        self._input_fignodes.append(fluid)
        self._value: int = value

    @property
    def fluid(self) -> FIGNode:
        return self._input_fignodes[0]

    @property
    def value(self) -> float:
        return self._value
