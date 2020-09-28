from typing import List


class ExplicitMapping(object):

    def __init__(self):
        self.__startlist: List[str] = []
        self.__endlist: List[str] = []
        self.__technology: str = ''

    @property
    def startlist(self):
        return self.__startlist

    @property
    def endlist(self):
        return self.__endlist

    @property
    def technology(self):
        return self.__technology

    def map(self, netlist, fig):
        # TODO: Basically go through the start and stop and insert a bunch of components between the 
        # start and end and remove the correspoinding connections.
        # TODO: In scenarios where there are inbetween nodes, we probably need to be more careful and
        # this might not be the right place to do that kind of mapping
        pass
