from __future__ import annotations

from typing import Dict, List, Tuple

import networkx as nx
import numpy as np
from tabulate import tabulate

from lfr.compiler.distribute.BitVector import BitVector
from lfr.fig.fignode import ANDAnnotation, NOTAnnotation, ORAnnotation
from lfr.fig.fluidinteractiongraph import FluidInteractionGraph


class StateTable:
    def __init__(self, signal_list: List[str]) -> None:
        self._headers: List[str] = signal_list
        # TODO - Do a combinatorial explosion for all the states available
        # TODO - Figure out from Nada's paper on how to transform the
        # state table into flow annotations using z3
        self._connectivity_states: Dict[BitVector, nx.DiGraph] = {}
        # self._colored_graph: nx.DiGraph = None
        self._connectivity_matrix = None
        self._connectivity_column_headers = None
        self._connectivity_edges = {}
        self._and_annotations: List[ANDAnnotation] = []
        self._or_annotations: List[ORAnnotation] = []
        self._not_annotations: List[NOTAnnotation] = []
        self._annotated_connectivity_edges: List[Tuple[str, str]] = []

        self._or_column_skip_list: List[int] = []

    @property
    def headers(self) -> List[str]:
        return self._headers

    def get_connectivity_edge(self, i: int) -> Tuple[str, str]:
        # Returns the edge from here
        edge_name = self._connectivity_column_headers[i]
        edge = self._connectivity_edges[edge_name]
        return edge

    def convert_to_fullstate_vector(
        self, signal_list: List[str], state: BitVector
    ) -> BitVector:
        # Go through the each of the signal and update the specific BitVector value
        full_state_bitvector = BitVector(size=len(self._headers))
        for i in range(len(signal_list)):
            signal = signal_list[i]
            pos = self._headers.index(signal)
            full_state_bitvector[pos] = state[i]
        return full_state_bitvector

    def save_connectivity(
        self, state_vector: BitVector, source: str, target: str
    ) -> None:
        if state_vector not in self._connectivity_states.keys():
            self._connectivity_states[state_vector] = nx.DiGraph()

        # Add the connectivity in here
        digraph = self._connectivity_states[state_vector]

        # Add source and target if they are not present
        if source not in list(digraph.nodes):
            print(
                "Could not find source - {} in state table connectivity graph, adding node".format(
                    source
                )
            )
            digraph.add_node(source)

        if target not in list(digraph.nodes):
            print(
                "Could not find target - {} in state table connectivity graph, adding node".format(
                    target
                )
            )
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
        for state in self._connectivity_states:
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
        for state in self._connectivity_states:
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
            candidate.append(self.get_connectivity_edge(i))
            found_flag = False
            if i in skip_list:
                continue
            for j in range(i + 1, n_cols):
                if j in skip_list:
                    continue

                col_i = m[:, i]
                col_j = m[:, j]
                if np.array_equal(col_i, col_j):
                    skip_list.append(i)
                    skip_list.append(j)
                    candidate.append(self.get_connectivity_edge(j))
                    found_flag = True

            if found_flag is True:
                all_candidates.append(candidate)

        print("DISTRIBUTE-AND CANDIDATES:")
        print(all_candidates)

        # Populating this skip list is important to make sure
        # that all the nodes with the AND annotation are zero'ed
        # This will simplify how the or-compuation can be done
        for candidate in all_candidates:
            # Skip the first one and add the rest of
            # the edges into the skip list
            for i in range(1, len(candidate)):
                self.add_to_column_skip_list(candidate[i])

        # Add all the annotated edges to the list that keeps
        # track of used edges, this way we can ensrue that all
        # used edges are accounted for when we need to use the
        # NOTAnnotation

        for candidate in all_candidates:
            self._annotated_connectivity_edges.extend(candidate)

        # Generate all the different AND annotations necessary
        for candidate in all_candidates:
            for edge in candidate:
                # TODO - Figure out if the edge needs any additional markup here
                source_node = fig.get_fignode(edge[0])
                target_node = fig.get_fignode(edge[1])
                if source_node is None:
                    raise Exception(
                        "Could not find the corresponding nodes {}".format(source_node)
                    )
                if target_node is None:
                    raise Exception(
                        "could not find the corresponding nodes {}".format(target_node)
                    )
                fig.connect_fignodes(source_node, target_node)

            origin_nodes = [fig.get_fignode(edge[0]) for edge in candidate]
            print("Added AND annotation on FIG: {}".format(str(origin_nodes)))
            assert origin_nodes is not None
            annotation = fig.add_and_annotation(origin_nodes)
            self._and_annotations.append(annotation)

    def generate_or_annotations(self, fig: FluidInteractionGraph) -> None:

        self.print_connectivity_table()
        m = np.copy(self._connectivity_matrix)
        # Zerofill SKIPPED COLUMS
        print(m)
        for col in self._or_column_skip_list:
            m[:, col] = 0
        print(m)
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
            for j in range(i + 1, n_rows):
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

        print("DISTRIBUTE-OR CANDIDATES")
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
                        edge = self.get_connectivity_edge(i)

                        # Add all the annotated edges to the list that keeps
                        # track of used edges, this way we can ensrue that all
                        # used edges are accounted for when we need to use the
                        # NOTAnnotation
                        self._annotated_connectivity_edges.append(edge)

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

    def generate_not_annotations(self, fig: FluidInteractionGraph) -> None:
        m = self._connectivity_matrix
        shape = m.shape
        n_cols = shape[1]
        annotated_edges = self._annotated_connectivity_edges
        # Pick whatever single connectivity descriptions are left in this design
        for i in range(n_cols):
            edge = self.get_connectivity_edge(i)
            if edge not in annotated_edges:
                source_node = fig.get_fignode(edge[0])
                target_node = fig.get_fignode(edge[1])
                print(
                    "Found new NOT-DISTRIBUTE Candidate : {} -> {}".format(
                        edge[0], edge[1]
                    )
                )
                fig.connect_fignodes(source_node, target_node)
                annotation = fig.add_not_annotation([source_node, target_node])
                self._not_annotations.append(annotation)

    @staticmethod
    def __hamming_distance(vec1, vec2) -> int:
        assert vec1.size == vec2.size
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

    @staticmethod
    def __ones_count(vec1) -> int:
        ret = 0
        for i in range(len(vec1)):
            if vec1[i] == 1 or vec1[i] is True:
                ret += 1
        return ret

    @staticmethod
    def __convert_edge_to_name(edge: Tuple[str, str]) -> str:
        return "{}->{}".format(edge[0], edge[1])

    def __update_connectivity_matix(self, edge, row, value):
        edge_name = self.__convert_edge_to_name(edge)
        m = self._connectivity_matrix
        column = self._connectivity_column_headers.index(edge_name)
        m[row, column] = value

    def add_to_column_skip_list(self, edge: Tuple[str, str]):
        # TODO - add the column to skip edge list to
        #  prevent double count during xor finding
        edge_index = self._connectivity_column_headers.index(
            self.__convert_edge_to_name(edge)
        )
        self._or_column_skip_list.append(edge_index)

    def print_connectivity_table(self):
        m = self._connectivity_matrix
        headers = self._connectivity_column_headers
        table = tabulate(m, headers, tablefmt="fancy_grid")
        print(table)
