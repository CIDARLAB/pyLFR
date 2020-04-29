from .mappinglibrary import MappingLibrary, Primitive
from compiler.fluidinteraction import FluidInteraction
from compiler.fluidinteractiongraph import FluidInteractionGraph
from mint.mintdevice import MINTDevice

class FluidicMapping(object):

    def __init__(self, finteraction: FluidInteraction, device_generator = None) -> None:
        if device_generator is None:
            raise Exception("Need to provide a default library")
        self.__library: MappingLibrary = device_generator.library
        self.__name_generator = device_generator.namegenerator
        self.__finteraction = finteraction
        self.__blacklist_map = device_generator.blacklist_map
        self.__primitive_map = device_generator.primitive_map
        
        self.technology: str = ''
        self.params = dict()

    def get_technology(self, finteraction:FluidInteraction) -> Primitive:
        #TODO: Insert algorithm to figure which component would be the best fit for this scenario

        #Naive approach, pick the first component in the mapping library
        primitive = self.__library.get_operators(finteraction.interactionType)[0]
        return primitive

    def map(self, netlist:MINTDevice, fig:FluidInteractionGraph):
        #TODO: map the operator  
        interaction_id = self.__finteraction.id
        primitive = self.get_technology(self.__finteraction)
        if interaction_id not in fig.G.nodes:
            raise Exception("Could not find interaction `{}` in fig".format(interaction_id))

        print("Found {} in FIG, constructing design now ...".format(interaction_id))

        #TODO: Pull the data of the default params from whereever
        
        #Add the component first into the netlist
        name = self.__name_generator.generate_name(primitive.mint)
        netlist.addComponent(name, primitive.mint, {}, '0')
        self.__blacklist_map[interaction_id] = name
        self.__primitive_map[interaction_id] = primitive
        #TODO: Stitch together the default netlist

        #Create arcs to it's neighbours ?
        # inputs = fig.get_input_nodes(interaction_id)
        # for _input in inputs :
        #     if not netlist.componentExists(_input):
                #Create create a temporary that connects them
            
            #Create the arcs

            
        
        #Check if inputs exist in 
        #TODO: Connect the outputs to the component created

        #TODO:Connect the inputs to the component created