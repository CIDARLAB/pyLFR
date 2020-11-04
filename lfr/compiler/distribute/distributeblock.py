from lfr.compiler.distribute.statetable import StateTable
from typing import List
from lfr.compiler.language.vectorrange import VectorRange
from lfr.fig.fluidinteractiongraph import FluidInteractionGraph
from lfr.compiler.distribute.BitVector import BitVector


class DistributeBlock(object):

    def __init__(self) -> None:
        self._sensitivity_list: List[VectorRange] = None
        # self._state_header: List[str] = None
        self._state_table: StateTable = None

    def generate_fig(self, fig: FluidInteractionGraph) -> None:
        # TODO - Create the fig based on the given distribute logic shown here
        print("Implement the fig generation from this")
        pass

    @property
    def state_table(self) -> StateTable:
        return self._state_table

    @property
    def sensitivity_list(self) -> List[VectorRange]:
        return self._sensitivity_list

    @sensitivity_list.setter
    def sensitivity_list(self, signal_list: List[VectorRange]) -> None:
        self._sensitivity_list = signal_list
        # self._state_header = self.__generate_state_header()
        self._state_table = StateTable(signal_list)

    def set_connectivity(self, state, source, target) -> None:
        # TODO - Make the connectivity here based on the state
        # This will be called mulitple times per distributeassignstat
        pass

    def get_remaining_states(self, states: List[BitVector]) -> List[BitVector]:
        # TODO - Return the remaining states
        ret = []
        return ret

    def generate_state_vector(self, signal_list: List[VectorRange], value_list: List[bool]) -> BitVector:
        # self._state_table.convert_to_fullstate_vector()
        individual_signal_list = []
        individual_value_list = []
        for signal, value in zip(signal_list, value_list):
            for i in range(len(signal)):
                # signal_name = "{}_{}".format(signal.id, str(i))
                individual_signal_list.append(signal[i].id)
                individual_value_list.append(value)

        ret = self._state_table.convert_to_fullstate_vector(
            individual_signal_list,
            individual_value_list
        )
        return ret
