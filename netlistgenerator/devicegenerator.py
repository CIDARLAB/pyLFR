from .technologymapper import mapTechnologies
from networkx import nx
import utils


class DeviceGenerator(object):

    def __init__(self, name, module):
        self.devicename = name
        self.devicemodule = module

    def generatenetlist(self):
        # Process the direct technology mapping
        interactiongraph = self.devicemodule.G
        mapTechnologies(interactiongraph)

        utils.printgraph(interactiongraph.G, self.devicename + '.dot')
