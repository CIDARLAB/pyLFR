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
            raise Exception("Cannot create interaction between the same fluids")
        self.id = fluid1.id + "_" + fluid2.id
        self.customInteraction = custominteraction


