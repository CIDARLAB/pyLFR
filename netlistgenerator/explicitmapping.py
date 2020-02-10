class ExplicitMapping(object):
    
    def __init__(self):
        self.startlist:[str] = []
        self.endlist:[str] = []
        self.technology: str = ''
    
    def map(self, netlist, fig):
        #TODO: Basically go through the start and stop and insert a bunch of components between the 
        #start and end and remove the correspoinding connections.
        #TODO: In scenarios where there are inbetween nodes, we probably need to be more careful and
        # this might not be the right place to do that kind of mapping
        pass