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

        #First map all the i/o to PORT

        device = MINTDevice("testdevice")
        device.addComponent("p1", "PORT", { "portRadius": "2000"})
        device.addComponent("p2", "PORT", { "portRadius": "2000"})
        device.addConnection("c1", "CHANNEL", {"channelWidth":"400", "height":"400"}, MINTTarget("p1"), [MINTTarget("p2")])


        minttext = device.toMINT()

        mint_file = open(utils.get_ouput_path(self.devicemodule.name + ".uf"), "wt")
        mint_file.write(minttext)
        mint_file.close()
        

        #Second map all the operators to their respective primitives

        #Third map all the 'assign' mappings to specific primitives

        #Fourth generate the MINT file from the pyparchmint device