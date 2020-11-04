from lfr.compiler.language.vectorrange import VectorRange
from typing import Dict, List
import networkx as nx
from lfr.compiler.distribute.BitVector import BitVector


class StateTable(object):

    def __init__(self, signal_list: List[VectorRange]) -> None:
        self._headers: List[str] = self.__generate_state_header(signal_list)
        # TODO - Do a combinatorial explosion for all the states available
        # TODO - Figure out from Nada's paper on how to transform the
        # state table into flow annotations using z3
        self._self_states: Dict[BitVector, nx.DiGraph] = dict()
        self._colored_graph: nx.DiGraph = None

    @property
    def headers(self) -> List[str]:
        return self._headers

    def convert_to_fullstate_vector(self, signal_list: List[str], state: BitVector) -> BitVector:
        # Go through the each of the signal and update the specific BitVector value
        full_state_bitvector = BitVector(size=len(self._headers))
        for i in range(len(signal_list)):
            signal = signal_list[i]
            pos = self._headers.index(signal)
            full_state_bitvector[pos] = state[i]
        return full_state_bitvector

    def save_connectivity(self, full_state_vector: BitVector, source: str, target: str) -> None:
        if full_state_vector in self._self_states.keys():
            # Add the connectivity in here
            digraph = self._self_states[full_state_vector]

            # Add source and target if they are not present
            if source not in list(digraph.nodes):
                print("Could not find source - {} in state table connectivity graph".format(source))
                digraph.add_node(source)

            if target not in list(digraph.nodes):
                print("Could not find target - {} in state table connectivity graph".format(target))
                digraph.add_node(target)

            # Add the edge to show the connectivity
            digraph.add_edge(source, target)

    def __generate_state_header(self, signal_list: List[VectorRange]) -> List[str]:
        state_header = []
        for vector_range in signal_list:
            for i in range(len(vector_range)):
                state_header.append(vector_range[i].id)
        return state_header
