from mint.minttarget import MINTTarget
from mint.mintdevice import MINTDevice
from .technologymapper import map_technologies
from networkx import nx
import utils


class DeviceGenerator(object):

    def __init__(self, name, module):
        self.devicename = name
        self.devicemodule = module

    def generate_netlist(self):
        # Process the direct technology mapping
        interactiongraph = self.devicemodule.FIG
        
        utils.printgraph(interactiongraph.G, self.devicename + '.dot')


        mapping_blacklist = []
        port_list = []
        device = MINTDevice("testdevice")

        #1 map all the i/o to PORT
        for key in self.devicemodule.io.keys():
            io = self.devicemodule.io[key]
            device.addComponent(io.id, "PORT", { "portRadius": "2000"})
            port_list.append(io.id)
        
        
        #2 map all the operators to their respective primitives
        # 2.1 map all the 'assign' mappings to specific primitives
        # EDIT: 2.1 is a subcase because how we are storing all the mappings
        for mapping in self.devicemodule.mappings:
            #TODO: Make this for all the elements. Also each mapping is 1 component
            start = mapping.startlist[0]
            end = mapping.endlist[0]
            device.addComponent("{}_{}".format(start, end), mapping.technology, {})
            mapping_blacklist.extend(mapping.startlist)
            mapping_blacklist.extend(mapping.endlist)
            
            #Check the traversal and find all the paths that are broken
            for path in nx.all_simple_paths(self.devicemodule.FIG.G, source=start, target=end):
                mapping_blacklist.extend(path)

        # 2.2 Create a node for each of the the other fluid notes that are not in eith of the start or end lists
        for node in self.devicemodule.FIG.G.nodes:
            if node not in mapping_blacklist and node not in port_list:
                device.addComponent(node, "NODE", {})

        i = 1
        # 3 generate all the channels for every connecting arc in the fig (except for the ones between the start and end lists)
        for arc in self.devicemodule.FIG.G.edges():
            if not (arc[0] in mapping_blacklist and arc[1]  in mapping_blacklist):
                #Create the arc
                device.addConnection("c_{}_{}".format(arc[0], arc[1]), "CHANNEL", {"channelWidth":"400", "height":"400"}, MINTTarget(arc[0]), [MINTTarget(arc[1])])
                i += 1 
        
        #4 generate the MINT file from the pyparchmint device
        minttext = device.toMINT()
        mint_file = open(utils.get_ouput_path(self.devicemodule.name + ".uf"), "wt")
        mint_file.write(minttext)
        mint_file.close()