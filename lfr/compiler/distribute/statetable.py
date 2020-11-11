from __future__ import annotations
from lfr.fig.fignode import ANDAnnotation, ORAnnotation
from lfr.fig.fluidinteractiongraph import FluidInteractionGraph
from typing import Dict, List, Tuple
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
        # self._colored_graph: nx.DiGraph = None
        self._connectivity_matrix: np.array = None
        self._connectivity_column_headers = None
        self._connectivity_edges = dict()
        self._and_annotations: List[ANDAnnotation] = []
        self._or_annotations: List[ORAnnotation] = []

    @property
    def headers(self) -> List[str]:
        return self._headers

    def get_edge(self, j: int) -> Tuple[str, str]:
        return self._connectivity_edges[self._connectivity_column_headers[j]]

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
        self._connectivity_column_headers = connectivy_column_headers
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
            self._connectivity_edges[edge_name] = edge

        self._connectivity_matrix = np.zeros((row_size, column_size), dtype=int)

        i = 0
        for state in self._connectivity_states.keys():
            graph = self._connectivity_states[state]
            for edge in list(graph.edges):
                self.__update_connectivity_matix(edge, i, 1)

            i += 1

    def generate_and_annotations(self, fig: FluidInteractionGraph) -> None:
        m = self._connectivity_matrix
        shape = m.shape
        n_cols = shape[1]

        # Find all the different columns which are equal
        all_candidates = []
        skip_list = []
        for i in range(n_cols):
            candidate = []
            candidate.append(self.get_fig(i))
            found_flag = False
            if i in skip_list:
                continue
            for j in range(i+1, n_cols):
                if j in skip_list:
                    continue

                col_i = m[:, i]
                col_j = m[:, j]
                if np.array_equal(col_i, col_j):
                    skip_list.append(i)
                    skip_list.append(j)
                    candidate.append(self.get_edge(j))
                    found_flag = True

            if found_flag is True:
                all_candidates.append(candidate)

        print(all_candidates)
        # Generate all the different AND annotations necessary
        for candidate in all_candidates:
            for edge in candidate:
                # TODO - Figure out if the edge needs any additional markup here
                source_node = fig.get_fignode(edge[0])
                target_node = fig.get_fignode(edge[1])
                if source_node is None:
                    raise Exception("Could not find the corresponding nodes {}".format(source_node))
                if target_node is None:
                    raise Exception("could not find the corresponding nodes {}".format(target_node))
                fig.connect_fignodes(source_node, target_node)

            origin_nodes = [fig.get_fignode(edge[0]) for edge in candidate]
            print("Added AND annotation on FIG: {}".format(str(origin_nodes)))
            assert(origin_nodes is not None)
            annotation = fig.add_and_annotation(origin_nodes)
            self._and_annotations.append(annotation)

    def generate_or_annotations(self, fig: FluidInteractionGraph) -> None:

        m = self._connectivity_matrix
        shape = m.shape
        n_rows = shape[0]
        # n_cols = shape[1]

        all_candidates = []
        skip_list = []
        for i in range(n_rows):
            candidate_row_index = [i]
            accumulate_vector = m[i, :]
            ones_count = self.__ones_count(accumulate_vector)
            found_flag = False
            if i in skip_list:
                continue
            for j in range(i+1, n_rows):
                if j in skip_list:
                    continue
                # Compute XOR and see if the hamming distance is
                # row_i = m[i, :]
                row_j = m[j, :]

                # distance = self.__hamming_distance(row_i, row_c)
                # if distance != 2:
                #     continue

                # TODO - Go through the rows, see if the row-i and row-j
                # compute the XOR of the current vector with the accumulate
                xord_vector = np.logical_xor(accumulate_vector, row_j)
                distance = self.__hamming_distance(xord_vector, accumulate_vector)
                count = self.__ones_count(xord_vector)

                if distance == 1 and count == ones_count + 1:
                    candidate_row_index.append(j)
                    accumulate_vector = xord_vector
                    ones_count = count
                    skip_list.append(j)
                    found_flag = True

            if found_flag:
                all_candidates.append(candidate_row_index)

        print(all_candidates)
        # Generate all the different OR annotations necessary

        # Figure out how to process the candidates:
        # We should be able to go through each row,
        # figure out if the row's->positive's->source are in any of the AND annotations
        # if they are pick up the AND annotation node as one of the targets
        # else (is not present in AND annotation) pick up the positive's corresponding
        # flow node as one of the targets for the or annotation
        for candidate in all_candidates:
            args_for_annotation = []
            for row_index in candidate:
                row = m[row_index, :]
                for i in range(len(row)):
                    if row[i] == 1:
                        # Find the corresponding collumn edge:
                        edge = self.get_edge(i)
                        # First make a connection so that this is taken care or
                        source_node = fig.get_fignode(edge[0])
                        target_node = fig.get_fignode(edge[1])
                        fig.connect_fignodes(source_node, target_node)

                        # Add the connection target in inot the annotion targets we want
                        # this representated for the entire converage
                        target = edge[1]
                        args_for_annotation.append(fig.get_fignode(target))
                        # Check if the source is in any of the AND annotations
                        source = edge[0]
                        found_flag = False
                        annotation_to_use = None
                        for annotation in self._and_annotations:
                            if source in fig.neighbors(annotation.id):
                                found_flag = True
                                annotation_to_use = fig.get_fignode(annotation.id)
                                break
                        if found_flag is True:
                            if annotation_to_use not in args_for_annotation:
                                args_for_annotation.append(annotation_to_use)
                        else:
                            if source not in args_for_annotation:
                                args_for_annotation.append(fig.get_fignode(source))

            self._or_annotations.append(fig.add_or_annotation(args_for_annotation))

    def __hamming_distance(self, vec1, vec2) -> int:
        assert(vec1.size == vec2.size)
        # Start with a distance of zero, and count up
        distance = 0
        # Loop over the indices of the string
        L = len(vec1)
        for i in range(L):
            # Add 1 to the distance if these two characters are not equal
            if vec1[i] != vec2[i]:
                distance += 1

        # Return the final count of differences
        return distance

    def __ones_count(self, vec1) -> int:
        ret = 0
        for i in range(len(vec1)):
            if vec1[i] == 1 or vec1[i] is True:
                ret += 1
        return ret

    def __convert_edge_to_name(self, edge) -> str:
        return "{}->{}".format(edge[0], edge[1])

    def __update_connectivity_matix(self, edge, row, value):
        edge_name = self.__convert_edge_to_name(edge)
        m = self._connectivity_matrix
        column = self._connectivity_column_headers.index(edge_name)
        m[row, column] = value

    def get_fig(self, i: int):
        # Returns the edge from here
        edge_name = self._connectivity_column_headers[i]
        edge = self._connectivity_edges[edge_name]
        return edge
