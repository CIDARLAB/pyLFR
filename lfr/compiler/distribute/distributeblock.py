from lfr.compiler.distribute.statetable import StateTable
from typing import List
from lfr.compiler.language.vectorrange import VectorRange
from lfr.fig.fluidinteractiongraph import FluidInteractionGraph
from lfr.compiler.distribute.BitVector import BitVector


class DistributeBlock(object):

    def __init__(self) -> None:
        self._sensitivity_list: List[VectorRange] = []
        # self._state_header: List[str] = None
        self._state_table: StateTable = None

    def generate_fig(self, fig: FluidInteractionGraph) -> None:
        # TODO - Create the fig based on the given distribute logic shown here
        print("Implement the fig generation from this")
        self._state_table.generate_connectivity_table()

        self._state_table.generate_and_annotations(fig)

        self._state_table.generate_or_annotations(fig)

        # TODO - How to map the control mappings for each
        # of the annotations to the control signals
        # self._state_table.compute_control_mapping()

        # TODO - Mark all the single items with no pairs
        pass

    @property
    def state_table(self) -> StateTable:
        return self._state_table

    @property
    def sensitivity_list(self) -> List[VectorRange]:
        return self._sensitivity_list

    @sensitivity_list.setter
    def sensitivity_list(self, signal_list: List[VectorRange]) -> None:
        if self._state_table is not None:
            raise Exception("Cannot update the sensitivity list since \
                state table has already been generated !")
        self._sensitivity_list = signal_list
        # self._state_header = self.__generate_state_header()
        self._state_table = StateTable(self.__generate_state_header(signal_list))

    def set_connectivity(self, state, source, target) -> None:
        # Make the connectivity here based on the state
        # This will be called mulitple times per distributeassignstat
        self._state_table.save_connectivity(state, source, target)

    def get_remaining_states(self, states: List[BitVector]) -> List[BitVector]:
        # Return the remaining states
        ret = []
        # Get the size of the state, generate every state until that size and add
        # whatever is not done into the ret
        vector_size = len(states[0])
        for i in range(pow(2, vector_size)):
            bv = BitVector(intVal=i, size=vector_size)
            if bv not in states:
                ret.append(bv)

        return ret

    def generate_state_vector(self, signal_list: List[VectorRange], value_list: List[bool]) -> BitVector:
        # self._state_table.convert_to_fullstate_vector()
        individual_signal_list = []
        individual_value_list = []

        i = 0
        for signal in signal_list:
            for j in range(len(signal)):
                individual_signal_list.append(signal[j].id)
                value = value_list[i + j]
                individual_value_list.append(value)
            i += 1

        ret = self._state_table.convert_to_fullstate_vector(
            individual_signal_list,
            individual_value_list
        )
        return ret

    def __generate_state_header(self, signal_list: List[VectorRange]) -> List[str]:
        state_header = []
        for vector_range in signal_list:
            for i in range(len(vector_range)):
                state_header.append(vector_range[i].id)
        return state_header
