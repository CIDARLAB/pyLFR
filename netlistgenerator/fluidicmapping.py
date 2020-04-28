from compiler.fluidinteractiongraph import FluidInteractionGraph
from mint.mintdevice import MINTDevice

class FluidicMapping(object):

    def __init__(self, finteraction, library = None) -> None:
        if library is None:
            raise Exception("Need to provide a default library")
        self.__library = library
        self.__finteraction = finteraction
        self.technology: str = ''
        self.params = dict()

    def map(self, netlist:MINTDevice, fig:FluidInteractionGraph):
        #TODO: map the operator  
        
        pass