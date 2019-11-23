from enum import Enum
from .fluid import Fluid


class InteractionType(Enum):
    TECHNOLOGY_PROCESS = 1
    MIX = 2
    SEPARATE = 3
    DISTRIBUTE = 4,
    CONTROL = 5


class FluidInteraction(object):
    def __init__(self, fluid1: Fluid, fluid2: Fluid, interactiontype: InteractionType, custominteraction=None):
        self.interactionType = interactiontype
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
