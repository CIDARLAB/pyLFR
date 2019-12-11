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
        
        # TODO: Figure out how to pass selected points for the graph optimization
        # map_technologies(interactiongraph)

        utils.printgraph(interactiongraph.G, self.devicename + '.dot')
