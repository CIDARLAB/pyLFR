from typing import Dict, List
import networkx as nx
from lfr.compiler.distribute.BitVector import BitVector
import numpy as np


class StateTable(object):

    def __init__(self, signal_list: List[str]) -> None:
        self._headers: List[str] = signal_list
        # TODO - Do a combinatorial explosion for all the states available
        # TODO - Figure out from Nada's paper on how to transform the
        # state table into flow annotations using z3
        self._connectivity_states: Dict[BitVector, nx.DiGraph] = dict()
        self._colored_graph: nx.DiGraph = None
        self._connectivity_matrix: np.array = None
        self._connectivy_column_headers = None

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

    def save_connectivity(self, state_vector: BitVector, source: str, target: str) -> None:
        if state_vector not in self._connectivity_states.keys():
            self._connectivity_states[state_vector] = nx.DiGraph()

        # Add the connectivity in here
        digraph = self._connectivity_states[state_vector]

        # Add source and target if they are not present
        if source not in list(digraph.nodes):
            print("Could not find source - {} in state table connectivity graph, adding node".format(source))
            digraph.add_node(source)

        if target not in list(digraph.nodes):
            print("Could not find target - {} in state table connectivity graph, adding node".format(target))
            digraph.add_node(target)

        # Add the edge to show the connectivity
        print("Added the edge {} -> {}".format(source, target))
        digraph.add_edge(source, target)

    def generate_connectivity_table(self) -> None:

        connectivy_column_headers = []
        self._connectivy_column_headers = connectivy_column_headers
        # First setup the dimensions for the matrix
        row_size = len(self._connectivity_states.keys())
        full_connectivity_graph = nx.DiGraph()
        for state in self._connectivity_states.keys():
            graph = self._connectivity_states[state]
            for node in list(graph.nodes):
                if node not in connectivy_column_headers:
                    # connectivy_column_headers.append(node)
                    full_connectivity_graph.add_node(node)

            for edge in list(graph.edges):
                full_connectivity_graph.add_edge(edge[0], edge[1])

        column_size = len(list(full_connectivity_graph.edges))

        for edge in list(full_connectivity_graph.edges):
            edge_name = self.__convert_edge_to_name(edge)
            connectivy_column_headers.append(edge_name)

        self._connectivity_matrix = np.zeros((column_size, row_size))

        i = 0
        for state in self._connectivity_states.keys():
            graph = self._connectivity_states[state]
            for edge in list(full_connectivity_graph.edges):
                self.__update_connectivity_matix(edge, i, 1)

            i += 1

    # def __str__(self) -> str:
    #     ret = str(self.headers)
    #     ret += "\n"
    #     for state in self._connectivity_states.keys():
    #         ret += 
    
    def __convert_edge_to_name(self, edge) -> str:
        return "{}->{}".format(edge[0], edge[1])

    def __update_connectivity_matix(self, edge, row, value):
        edge_name = self.__convert_edge_to_name(edge)
        m = self._connectivity_matrix
        column = self._connectivy_column_headers.index(edge_name)
        m[column][row] = value
