from lfr.compiler.distribute.statetable import StateTable
from typing import List
from lfr.compiler.language.vectorrange import VectorRange
from lfr.fig.fluidinteractiongraph import FluidInteractionGraph
from BitVector import BitVector


class DistributeBlock(object):

    def __init__(self) -> None:
        self._sensitivity_list: List[VectorRange] = None
        self._state_header: List[str] = None
        self._state_table: StateTable = None

    def generate_fig(self, fig: FluidInteractionGraph) -> None:
        # TODO - Create the fig based on the given distribute logic shown here
        pass

    @property
    def state_header(self) -> List[str]:
        return self._state_header

    @property
    def sensitivity_list(self) -> List[VectorRange]:
        return self._sensitivity_list

    @sensitivity_list.setter
    def sensitivity_list(self, signal_list: List[VectorRange]) -> None:
        self._sensitivity_list = signal_list
        self._state_header = self.__generate_state_header()
        self._state_table = StateTable(self._state_header)

    def set_connectivity(self, state, source, target) -> None:
        # TODO - Make the connectivity here based on the state
        # This will be called mulitple times per distributeassignstat
        pass

    def __generate_state_header(self) -> List[str]:
        state_header = []
        for vector_range in self._sensitivity_list:
            for i in range(len(vector_range)):
                state_header.append("{}_{}".format(vector_range.id, str(i)))
        return state_header

    def generate_states(self, condition) -> List[BitVector]:
        # TODO - Utilize the logic expression and generate
        # bitvectors for each of the states represented by the
        # logic condition that is imported here

        # Return dummmy data
        ret = []
        ret.append(BitVector(intVal=1))
        ret.append(BitVector(intVal=2))
        ret.append(BitVector(intVal=3))

        return ret

    def get_remaining_states(self, states: List[BitVector]) -> List[BitVector]:
        # TODO - Return the remaining states
        ret = []
        return ret
