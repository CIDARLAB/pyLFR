from enum import Enum
from .fluid import Fluid
from typing import Optional


class InteractionType(Enum):
    TECHNOLOGY_PROCESS = 1      # Explicit Mapped operators
    MIX = 2                     # + 
    SIEVE = 3                   # -
    METER = 4                   # %
    DILUTE = 5                  # *
    DIVIDE = 6                  # /


class FluidInteraction(object):
    # TODO: WE need to rehaul this system
    def __init__(self, fluid1: Fluid = None, fluid2: Fluid = None, interactiontype: InteractionType = None, custominteraction=None):
        self.interactionType = interactiontype
        self.interaction_data = dict()
        self.fluids = []
        self.fluids.append(fluid1)
        self._output_fluid: Optional[Fluid] = None

        # Single fluid interaction case
        if fluid2 is None:
            self.id = "interaction_" + fluid1.id
            self.fluid1 = fluid1
            
        else:
            self.fluids.append(fluid2)
    
            if fluid1 == fluid2:
                raise Exception(
                    "Cannot create interaction between the same fluids")
            if fluid1.id < fluid2.id:
                self.id = fluid1.id + "_" + fluid2.id
                self.fluid1 = fluid1
                self.fluid2 = fluid2
            else:
                self.id = fluid2.id + "_" + fluid1.id
                self.fluid1 = fluid2
                self.fluid2 = fluid1

        self.customInteraction = custominteraction

    def get_output_fluid(self):
        if self._output_fluid is None:
            print("Warning: Interaction has no comupted output fluid, hence we are sending this later")
            return Fluid("output_" + self.id)
        else:
            return self._output_fluid

    @staticmethod
    def get_id(fluid1: Fluid = None, fluid2: Fluid = None, operator: str = '') -> str:
        id = None

        if fluid2 is not None:
            if fluid1.id < fluid2.id:
                id = fluid1.id + "_" + operator + "_" + fluid2.id
            else:
                id = fluid2.id + "_" + operator + "_" + fluid1.id
        else:
            id = fluid1.id + "_" + operator

        return id
