from .technologymapper import mapTechnologies
from networkx import nx

class DeviceGenerator(object):

    def __init__(self, name, module):
        self.devicename = name
        self.devicemodule = module

    def generatenetlist(self):
        # Process the direct technology mapping
        interactiongraph = self.devicemodule.G
        mapTechnologies(interactiongraph)

        interactiongraph.generate_dot_file(self.devicename + '.dot')
