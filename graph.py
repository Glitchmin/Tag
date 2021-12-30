from __future__ import annotations

from typing import List, Tuple, Dict

from production import Production


class Graph:
    def __init__(self, labels_list: List[str], edges_list: List[Tuple[int, int, str]]):
        """edges_dict - list of 3 element tuples (vertex_begin, vertex_end, label)"""
        self.next_v_ID = 0

        self.outgoing_edges_dict = {}
        self.ingoing_edges_dict = {}

        self.labels_dict = {}
        for label in labels_list:
            self.add_vertex(label)

        self.add_edges(edges_list)

    def add_vertex(self, label: str, edges_list=None):
        if edges_list is None:
            edges_list = []
        self.labels_dict.update({self.next_v_ID: label})
        self.outgoing_edges_dict.update({self.next_v_ID: set({})})
        self.ingoing_edges_dict.update({self.next_v_ID: set({})})
        self.add_edges(edges_list)
        self.next_v_ID += 1

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
            for self_edge in self.outgoing_edges_dict.get(self_ID):
                if not self_to_lhs_mapping.keys().__contains__(self_edge[0]):
                    return False
                left_edge = left.outgoing_edges_dict.get(self_to_lhs_mapping.get(self_ID))
                if left_edge[1] != self_edge[1] or left_edge[0] != self_to_lhs_mapping.get(self_edge[0]):
                    return False
                matched_edges += 1
            if matched_edges != left.outgoing_edges_dict.get(lhs_ID):
                return False


        return True

    def apply_production(self, production: Production, lhs_to_self_mapping: Dict[int, int]):
        """lhs - left hand side of the production"""
        if not self.validate(production.left_graph, lhs_to_self_mapping):
            raise ValueError("invalid lhs_to_self_mapping - given subgraph of the start graph not isomorphic to the left graph")

    def print(self):
        for vertex in self.labels_dict:
            print("vertexID: ", vertex, " vertexLabel",  self.labels_dict.get(vertex))
            for edge in self.outgoing_edges_dict.get(vertex):
                print(edge, end=", ")
            print()
            for edge in self.ingoing_edges_dict.get(vertex):
                print(edge, end=", ")
            print()
