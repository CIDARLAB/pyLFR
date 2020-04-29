from mint.mintlayer import MINTLayer, MINTLayerType
from mint.minttarget import MINTTarget
from mint.mintdevice import MINTDevice
from .technologymapper import map_technologies
from .fluidicmapping import FluidicMapping
from networkx import nx
import utils


class NameGenerator(object):
    def __init__(self) -> None:
        self.dictionary = dict()
       
    def generate_name(self, technology_string: str) -> str:
        if technology_string in self.dictionary.keys():
            #Increment the number in dictionary and return the name
            ret = self.dictionary[technology_string] + 1
            self.dictionary[technology_string] = ret
            return '{}_{}'.format(technology_string, ret).lower().replace(' ', "_")
        else:
            self.dictionary[technology_string] = 1
            return '{}_{}'.format(technology_string, 1).lower().replace(' ', "_")


class DeviceGenerator(object):

    def __init__(self, name, module, library):
        self.devicename = name
        self.devicemodule = module
        self.namegenerator = NameGenerator()
        self.library = library
        self.__temp_component_list = []
        self.blacklist_map = dict()
        self.primitive_map = dict()


    def generate_dummy_netlist(self):
        # Process the direct technology mapping
        interactiongraph = self.devicemodule.FIG
        
        utils.printgraph(interactiongraph.G, self.devicename + '.dot')

        mapping_blacklist = []
        blacklist_map = dict()
        port_list = []
        device = MINTDevice(self.devicemodule.name)

        #1 map all the i/o to PORT
        for key in self.devicemodule.io.keys():
            io = self.devicemodule.io[key]
            device.addComponent(io.id, "PORT", { "portRadius": "2000"}, '0')
            port_list.append(io.id)
        
        
        #2 map all the operators to their respective primitives
        # 2.1 map all the 'assign' mappings to specific primitives
        # EDIT: 2.1 is a subcase because how we are storing all the mappings
        for mapping in self.devicemodule.mappings:
            #TODO: Make this for all the elements. Also each mapping is 1 component
            start = mapping.startlist[0]
            end = mapping.endlist[0]
            new_component_name = self.namegenerator.generate_name(mapping.technology)
            device.addComponent(new_component_name, mapping.technology, {"numberOfBends": "5", "bendSpacing":"2000", "bendLength": "2000", "channelWidth": "400", "height":"400"}, '0')
            mapping_blacklist.extend(mapping.startlist)
            mapping_blacklist.extend(mapping.endlist)
            # Set this mapping such that, all the items in the blacklist have an alternatethingy
            for item in mapping.startlist:
                blacklist_map[item] = new_component_name
            
            for item in mapping.endlist:
                blacklist_map[item] = new_component_name
            
            #Check the traversal and find all the paths that are broken
            for path in nx.all_simple_paths(self.devicemodule.FIG.G, source=start, target=end):
                mapping_blacklist.extend(path)

        # 2.2 Create a node for each of the the other fluid notes that are not in eith of the start or end lists
        for node in self.devicemodule.FIG.G.nodes:
            if node not in mapping_blacklist and node not in port_list:
                device.addComponent(node, "NODE", {}, '0')

        i = 1
        # 3 generate all the channels for every connecting arc in the fig (except for the ones between the start and end lists)
        for arc in self.devicemodule.FIG.G.edges():
            if not (arc[0] in mapping_blacklist and arc[1]  in mapping_blacklist):
                #Create the arc
                channel_start = arc[0]
                channel_end = arc[1]
                if arc[0] in mapping_blacklist:
                    # get the mapping item connected to arc[0] and use it instead
                    channel_start = blacklist_map[arc[0]]
                if arc[1] in mapping_blacklist:
                    channel_end = blacklist_map[arc[1]]
                device.addConnection(self.namegenerator.generate_name("channel"), "CHANNEL", {"channelWidth":"400", "height":"400"}, MINTTarget(channel_start), [MINTTarget(channel_end)], '0')
                i += 1 
        
        #4 generate the MINT file from the pyparchmint device
        minttext = device.toMINT()
        mint_file = open(utils.get_ouput_path(self.devicemodule.name + ".mint"), "wt")
        mint_file.write(minttext)
        mint_file.close()


    def generate_fluidic_netlist(self):
        # Process the direct technology mapping
        fig = self.devicemodule.FIG
        
        utils.printgraph(fig.G, self.devicename + '.dot')

        mapping_blacklist = []
        
        port_list = []
        device = MINTDevice(self.devicemodule.name)

        device.addLayer('0',0, MINTLayerType.FLOW)

        #1 map all the i/o to PORT
        for key in self.devicemodule.io.keys():
            io = self.devicemodule.io[key]
            device.addComponent(io.id, "PORT", { "portRadius": "2000"}, '0')
            port_list.append(io.id)
        
        
        #2 map all the operators to their respective primitives
        # 2.1 map all the 'assign' mappings to specific primitives
        # EDIT: 2.1 is a subcase because how we are storing all the mappings
        for mapping in self.devicemodule.mappings:
            #TODO: Make this for all the elements. Also each mapping is 1 component
            start = mapping.startlist[0]
            end = mapping.endlist[0]
            new_component_name = self.namegenerator.generate_name(mapping.technology)
            device.addComponent(new_component_name, mapping.technology, {}, '0')
            mapping_blacklist.extend(mapping.startlist)
            mapping_blacklist.extend(mapping.endlist)
            # Set this mapping such that, all the items in the blacklist have an alternatethingy
            for item in mapping.startlist:
                self.blacklist_map[item] = new_component_name
            
            for item in mapping.endlist:
                self.blacklist_map[item] = new_component_name
            
            #Check the traversal and find all the paths that are broken
            for path in nx.all_simple_paths(self.devicemodule.FIG.G, source=start, target=end):
                mapping_blacklist.extend(path)

        # 2.2 Run through each of the operators and start creating mappings for them
        print("Fluidic Interactions:")
        for interaction in fig.fluidinteractions.keys():
            fluidic_interaction = fig.fluidinteractions[interaction]
            print("Interaction:{} Type{}".format(fluidic_interaction, type(fluidic_interaction))) 
            fluidic_mapping = FluidicMapping(fluidic_interaction, self)
            #Map this to a component and generate a bit of the netlist
            fluidic_mapping.map(device, fig)
            #Add it to blacklist to ensure that nodes dont get generated
            mapping_blacklist.append(interaction)

        # 2.3 Create a node for each of the the other fluid notes that are not in eith of the start or end lists
        for node in self.devicemodule.FIG.G.nodes:
            if node not in mapping_blacklist and node not in port_list:
                device.addComponent(node, "NODE", {}, '0')

        i = 1
        # 3 generate all the channels for every connecting arc in the fig (except for the ones between the start and end lists)
        for arc in self.devicemodule.FIG.G.edges():
            if not (arc[0] in mapping_blacklist and arc[1]  in mapping_blacklist):
                #Create the arc
                channel_start = arc[0]
                channel_end = arc[1]
                channel_start_target = None
                channel_end_target = None
                if arc[0] in mapping_blacklist:
                    # get the mapping item connected to arc[0] and use it instead
                    channel_start = self.blacklist_map[arc[0]]
                    if arc[0] in self.primitive_map:
                        channel_start_target = str(self.primitive_map[arc[0]].outputs.pop())
                if arc[1] in mapping_blacklist:
                    channel_end = self.blacklist_map[arc[1]]
                    if arc[1] in self.primitive_map: 
                        channel_end_target = str(self.primitive_map[arc[1]].inputs.pop())
                connection_name = self.namegenerator.generate_name("channel")
                device.addConnection(connection_name, "CHANNEL", {"channelWidth":"400", "height":"400"}, MINTTarget(channel_start, channel_start_target), [MINTTarget(channel_end, channel_end_target)], '0')
                i += 1 
        
        #4 generate the MINT file from the pyparchmint device
        minttext = device.toMINT()
        mint_file = open(utils.get_ouput_path(self.devicemodule.name + ".mint"), "wt")
        mint_file.write(minttext)
        mint_file.close()