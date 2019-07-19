from .technologymapper import mapTechnologies

class DeviceGenerator(object):

    def __init__(self, name, module):
        self.devicename = name
        self.devicemodule = module

    def generatenetlist(self):
        # Process the direct technology mapping
        interactiongraph = self.devicemodule.G
        mapTechnologies(interactiongraph)

