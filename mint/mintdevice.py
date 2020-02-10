from pyparchmint.device import Device
from mint.mintcomponent import MINTComponent
from mint.mintconnection import MINTConnection


class MINTDevice(Device):

    def __init__(self, name) -> None:
        super().__init__()
        self.name = name

    def addComponent(self, name: str, technology: str, params: dict):
        component = MINTComponent(name, technology, params)
        self.components.append(component)
    
    def addConnection(self, name, technology, params , source, sinks:[]):
        connection = MINTConnection(name, technology, params, source, sinks)
        self.connections.append(connection)

    def toMINT(self):

        componenttext = "\n".join([item.toMINT() for item in self.components])
        connectiontext = "\n".join([item.toMINT() for item in self.connections])

        flow = "LAYER FLOW\n{} \n\n{}\n\nEND LAYER\n".format(componenttext, connectiontext)

        full = "DEVICE {}\n\n{}".format(self.name, flow)
        return full