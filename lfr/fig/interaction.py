from typing import List
from lfr.fig.fignode import FIGNode, Flow
from enum import Enum


class InteractionType(Enum):
    TECHNOLOGY_PROCESS = 1      # Explicit Mapped operators
    MIX = 2                     # +
    SIEVE = 3                   # -
    METER = 4                   # %
    DILUTE = 5                  # *
    DIVIDE = 6                  # /


class Interaction(Flow):

    def __init__(self, id: str, interaction_type: InteractionType) -> None:
        super().__init__(id)
        self._interaction_type: InteractionType = interaction_type
        self._input_fignodes: List[FIGNode] = []
        self._output_fignode: FIGNode = None
        self._operator: str = ""

    @property
    def type(self) -> InteractionType:
        return self._interaction_type

    @staticmethod
    def get_id(fluid1: FIGNode = None, fluid2: FIGNode = None, operator_string: str = '') -> str:
        id = None

        if fluid2 is not None:
            if fluid1.id < fluid2.id:
                id = fluid1.id + "_" + operator_string + "_" + fluid2.id
            else:
                id = fluid2.id + "_" + operator_string + "_" + fluid1.id
        else:
            id = fluid1.id + "_" + operator_string

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
    def get_operator_str(interaction_type: InteractionType, process_operator='') -> str:
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

    def __init__(self, fluid1: Flow, fluid2: Flow, interaction_type: InteractionType = None, interaction_data: str = None) -> None:
        """Creates an interaction between two fluids

        Args:
            fluid1 (FIGNode): [description]
            fluid2 (FIGNode): [description]
            interaction_type (InteractionType, optional): [description]. Defaults to None.
            interaction_data (str, optional): [description]. Defaults to None.
        """
        id = Interaction.get_id(fluid1, fluid2, Interaction.get_operator_str(interaction_type))
        super().__init__(id, interaction_type)
        self._input_fignodes.append(fluid1)
        self._input_fignodes.append(fluid2)

    @property
    def fluids(self) -> List[FIGNode]:
        return self._input_fignodes


class FluidFluidCustomInteraction(FluidFluidInteraction):

    def __init__(self, fluid1: Flow, fluid2: Flow, custom_operator: str) -> None:
        id = Interaction.get_id(fluid1, fluid2, operator_string=custom_operator)
        super().__init__(fluid1, fluid2, InteractionType.TECHNOLOGY_PROCESS)
        self._id = id
        self._operator = custom_operator


class FluidProcessInteraction(Interaction):

    def __init__(self, fluid: Flow, process_operator: str) -> None:
        """Creates an instance of a Fluidic Interaction that shows the process
        is happening on the fluid using a custom operator (typically unary)

        Args:
            fluid (FIGNode): [description]
            process_operator (str): [description]
        """
        operator_str = Interaction.get_operator_str(InteractionType.TECHNOLOGY_PROCESS, process_operator)
        id = Interaction.get_id(fluid, operator_string=operator_str)
        super().__init__(id, InteractionType.TECHNOLOGY_PROCESS)
        self._input_fignodes.append(fluid)

    @property
    def fluid(self) -> FIGNode:
        return self._input_fignodes[0]


class FluidNumberInteraction(Interaction):

    def __init__(self, fluid: Flow, value: float, interaction_type: InteractionType) -> None:
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

    def __init__(self, fluid: Flow, value: int, interaction_type: InteractionType) -> None:
        """Creates an instance of a fluidic interactions between integers and fluids

        Args:
            fluid (FIGNode): [description]
            value (int): [description]
            interaction_type (InteractionType): [description]
        """
        id = Interaction.get_id(fluid1=fluid, operator_string=Interaction.get_operator_str(interaction_type))
        super().__init__(id, interaction_type)
        self._input_fignodes.append(fluid)
        self._value: int = value

    @property
    def fluid(self) -> FIGNode:
        return self._input_fignodes[0]

    @property
    def value(self) -> float:
        return self._value
