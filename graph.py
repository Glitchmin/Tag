from __future__ import annotations

from typing import List, Tuple, Dict, Set

from new_edges_definition import NewEdgesDefinition
from production import Production
import csv


class Graph:
    def __init__(self, labels_list: List[str], edges_list: List[Tuple[int, int, str]]):
        """edges_dict - list of 3 element tuples (vertex_begin, vertex_end, label)"""
        self.next_v_ID = 0

        self.outgoing_edges_dict: Dict[int, Set[Tuple[int, str]]] = {}
        self.ingoing_edges_dict: Dict[int, Set[Tuple[int, str]]] = {}

        self.labels_dict: Dict[int, str] = {}
        for label in labels_list:
            self.add_vertex(label)

        self.add_edges(edges_list)

    def add_vertex(self, label: str, edges_list=None) -> int:
        if edges_list is None:
            edges_list = []
        self.labels_dict.update({self.next_v_ID: label})
        self.outgoing_edges_dict.update({self.next_v_ID: set({})})
        self.ingoing_edges_dict.update({self.next_v_ID: set({})})
        self.add_edges(edges_list)
        self.next_v_ID += 1
        return self.next_v_ID - 1

    def remove_vertex(self, vertex_id: int):
        if self.labels_dict.__contains__(vertex_id):
            self.labels_dict.pop(vertex_id)
        to_delete = []
        for edge in self.outgoing_edges_dict.get(vertex_id):
            to_delete.append((vertex_id, edge[0], edge[1]))
        for edge in self.ingoing_edges_dict.get(vertex_id):
            to_delete.append((edge[0], vertex_id, edge[1]))
        self.remove_edges(to_delete)
        self.outgoing_edges_dict.pop(vertex_id)
        self.ingoing_edges_dict.pop(vertex_id)

    def add_edges(self, edges_list: List[Tuple[int, int, str]]):
        for e in edges_list:
            self.add_edge(e)

    def add_edge(self, edge: Tuple[int, int, str]):
        self.outgoing_edges_dict.get(edge[0]).add((edge[1], edge[2]))
        self.ingoing_edges_dict.get(edge[1]).add((edge[0], edge[2]))

    def remove_edges(self, edges_list: List[Tuple[int, int, str]]):
        for edge in edges_list:
            self.outgoing_edges_dict.get(edge[0]).remove((edge[1], edge[2]))
            self.ingoing_edges_dict.get(edge[1]).remove((edge[0], edge[2]))

    def get_edges(self) -> List[Tuple[int, int, str]]:
        edges: List[Tuple[int, int, str]] = []
        for (vertex, out_edges) in self.outgoing_edges_dict.items():
            for (dest_vertex, label) in out_edges:
                edges.append((vertex, dest_vertex, label))
        return edges

    def validate(self, left: Graph, lhs_to_self_mapping: Dict[int, int]) -> bool:
        self_to_lhs_mapping = {v: k for k, v in lhs_to_self_mapping.items()}
        for lhs_ID, self_ID in lhs_to_self_mapping.items():
            if self.labels_dict.get(self_ID) != left.labels_dict.get(lhs_ID):
                return False
            matched_edges = 0
            for self_edge, left_edge in zip(self.outgoing_edges_dict.get(self_ID),
                                            left.outgoing_edges_dict.get(self_to_lhs_mapping.get(self_ID))):
                if not self_to_lhs_mapping.keys().__contains__(self_edge[0]):
                    return False
                if left_edge[1] != self_edge[1] or left_edge[0] != self_to_lhs_mapping.get(self_edge[0]):
                    return False
                matched_edges += 1
            if matched_edges != len(left.outgoing_edges_dict.get(lhs_ID)):
                return False

        return True

    def get_edges_connecting_subgraph(self, indexes: Set[int]) -> List[Tuple[int, int, str]]:
        connecting_edges = []
        for vertex in indexes:
            for edge in self.outgoing_edges_dict.get(vertex):
                if edge[0] not in indexes:
                    connecting_edges.append((vertex, edge[0], edge[1]))
            for edge in self.ingoing_edges_dict.get(vertex):
                if edge[0] not in indexes:
                    connecting_edges.append((edge[0], vertex, edge[1]))
        return connecting_edges

    def remove_subgraph(self, indexes: List[int]):
        for index in indexes:
            self.remove_vertex(index)

    def merge(self, other: Graph) -> Dict[int, int]:
        # next_index = self.next_v_ID
        other_to_self_mapping: Dict[int, int] = {}
        for (other_index, other_label) in other.labels_dict.items():
            other_to_self_mapping[other_index] = self.add_vertex(other_label)

        self.add_edges(list(map(lambda e: (other_to_self_mapping[e[0]],
                                           other_to_self_mapping[e[1]],
                                           e[2]), other.get_edges())))

        return other_to_self_mapping

    def create_new_edges(self, new_edges_def: NewEdgesDefinition, removed_edges: List[Tuple[int, int, str]],
                         rhs_to_self_mapping: Dict[int, int]):
        for removed_edge in removed_edges:
            if removed_edge[2] == new_edges_def.label:
                """if mapping.values doesn't contain a vertex form removed it means it wasn't part of a subgraph,
                (doesn't work opposite way)"""
                if new_edges_def.is_outgoing and not rhs_to_self_mapping.values().__contains__(removed_edge[1]):
                    for rhs_vertex in new_edges_def.rhs_vertices:
                        self.add_edge((rhs_to_self_mapping.get(rhs_vertex), removed_edge[1], new_edges_def.label))
                if not new_edges_def.is_outgoing and not rhs_to_self_mapping.values().__contains__(removed_edge[0]):
                    for rhs_vertex in new_edges_def.rhs_vertices:
                        self.add_edge((removed_edge[0], rhs_to_self_mapping.get(rhs_vertex), new_edges_def.label))

    def apply_production(self, production: Production, lhs_to_self_mapping: Dict[int, int]):
        """lhs - left hand side of the production"""
        if not self.validate(production.left_graph, lhs_to_self_mapping):
            raise ValueError("invalid lhs_to_self_mapping - given subgraph of the start graph not\
                              isomorphic to the left graph")

        removed_edges: List[Tuple[int, int, str]] = self.get_edges_connecting_subgraph(
            set(lhs_to_self_mapping.values()))

        self.remove_subgraph(list(lhs_to_self_mapping.values()))

        rhs_to_self_mapping = self.merge(production.right_graph)

        for new_edges_def in production.new_edges_defs:
            self.create_new_edges(new_edges_def, removed_edges, rhs_to_self_mapping)
        self.save_to_file()

    def print(self):
        for vertex in self.labels_dict:
            print("vertexID: ", vertex, " vertexLabel", self.labels_dict.get(vertex))
            print("Outgoing edges: ", end='')
            for edge in self.outgoing_edges_dict.get(vertex):
                print(edge, end=", ")
            print("\nIngoing edges: ", end='')
            for edge in self.ingoing_edges_dict.get(vertex):
                print(edge, end=", ")
            print()

    def clear(self):
        self.next_v_ID = 0
        self.outgoing_edges_dict: Dict[int, Set[Tuple[int, str]]] = {}
        self.ingoing_edges_dict: Dict[int, Set[Tuple[int, str]]] = {}
        self.labels_dict: Dict[int, str] = {}

    def save_to_file(self, filename='graph.csv'):
        edges = self.get_edges()
        graph_data = [[] for _ in range(2)]
        for (vertex_id, label) in self.labels_dict.items():
            graph_data[0].append(vertex_id)
            graph_data[0].append(label)
        for edge in edges:
            graph_data[1].append(edge[0])
            graph_data[1].append(edge[1])
            graph_data[1].append(edge[2])
        with open(filename, 'w', newline='') as save_file:
            writer = csv.writer(save_file)
            writer.writerows(graph_data)

    @staticmethod
    def parse_file_input(filename) -> Tuple[List[str], List[str]]:
        with open(filename) as save_file:
            graph_data_reader = csv.reader(save_file)
            graph_data = []
            for data_line in graph_data_reader:
                graph_data.append(data_line)
            return graph_data[0], graph_data[1]

    @staticmethod
    def read_from_file(filename='graph.csv') -> Graph:
        new_graph = Graph(['A'], [(0, 0, "asd")])
        new_graph.clear()
        graph_vertices, graph_edges = Graph.parse_file_input(filename)
        for vertex in range(0, len(graph_vertices), 2):
            vertex_id = int(graph_vertices[vertex])
            vertex_label = graph_vertices[vertex + 1]
            new_graph.outgoing_edges_dict.update({vertex_id: set({})})
            new_graph.ingoing_edges_dict.update({vertex_id: set({})})
            new_graph.next_v_ID = max(new_graph.next_v_ID, vertex_id)
            new_graph.labels_dict.update({vertex_id: vertex_label})
        for edge in range(0, len(graph_edges), 3):
            new_graph.add_edge((int(graph_edges[edge]), int(graph_edges[edge + 1]), graph_edges[edge + 2]))
        return new_graph
