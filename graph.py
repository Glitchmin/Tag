from __future__ import annotations

from typing import List, Tuple, Dict, Set

from new_edges_definition import NewEdgesDefinition
from production import Production


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
        return self.next_v_ID-1

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
            self.outgoing_edges_dict.get(e[0]).add((e[1], e[2]))
            self.ingoing_edges_dict.get(e[1]).add((e[0], e[2]))

    def remove_edges(self, edges_list: List[Tuple[int, int, str]]):
        for edge in edges_list:
            self.outgoing_edges_dict.get(edge[0]).remove((edge[1], edge[2]))
            self.ingoing_edges_dict.get(edge[1]).remove((edge[0], edge[2]))

    def validate(self, left: Graph, lhs_to_self_mapping: Dict[int, int]) -> bool:
        self_to_lhs_mapping = {v: k for k, v in lhs_to_self_mapping.items()}
        for lhs_ID, self_ID in lhs_to_self_mapping.items():
            if self.labels_dict.get(self_ID) != left.labels_dict.get(lhs_ID):
                return False
            matched_edges = 0
            for self_edge, left_edge in zip(self.outgoing_edges_dict.get(self_ID), left.outgoing_edges_dict.get(self_to_lhs_mapping.get(self_ID))):
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

    def merge(self, other: Graph):
        # next_index = self.next_v_ID
        other_to_self_mapping: Dict[int, int] = {}
        for (other_index, other_label) in other.labels_dict.items():
            other_to_self_mapping[other_index] = self.add_vertex(other_label)

        #add edges mapped via other_to_self

    def create_new_edges(self, new_edges_def: NewEdgesDefinition, removed_edges:List[Tuple[int, int, str]]):
        pass

    def apply_production(self, production: Production, lhs_to_self_mapping: Dict[int, int]):
        """lhs - left hand side of the production"""
        if not self.validate(production.left_graph, lhs_to_self_mapping):
            raise ValueError("invalid lhs_to_self_mapping - given subgraph of the start graph not\
                              isomorphic to the left graph")

        removed_edges: List[Tuple[int, int, str]] = self.get_edges_connecting_subgraph(set(lhs_to_self_mapping.values()))

        self.remove_subgraph(list(lhs_to_self_mapping.values()))

        self.merge(production.right_graph)

        for new_edges_def in production.new_edges_defs:
            self.create_new_edges(new_edges_def, removed_edges)

    def print(self):
        for vertex in self.labels_dict:
            print("vertexID: ", vertex, " vertexLabel",  self.labels_dict.get(vertex))
            for edge in self.outgoing_edges_dict.get(vertex):
                print(edge, end=", ")
            print()
            for edge in self.ingoing_edges_dict.get(vertex):
                print(edge, end=", ")
            print()
