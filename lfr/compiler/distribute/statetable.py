from typing import Dict, List
from BitVector import BitVector
import networkx as nx


class StateTable(object):

    def __init__(self, header_list: List[str]) -> None:
        self._headers = header_list
        # TODO - Do a combinatorial explosion for all the states available
        # TODO - Figure out from Nada's paper on how to transform the 
        # state table into flow annotations using z3
        self._self_states: Dict[BitVector, nx.DiGraph] = dict()

    def save_state(self, signal_list: List[str], state: BitVector) -> None:
        # Go through the each of the signal and update the specific BitVector value
        full_state_bitvector = BitVector(size=len(self._headers))
        for i in range(len(signal_list)):
            signal = signal_list[i]
            pos = self._headers.index(signal)
            full_state_bitvector[pos] = state[i]
