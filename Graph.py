from typing import List, Tuple


class Graph:
    def __init__(self, labels_list: List[str], edges_list: List[Tuple[int, int, str]]):
        # edges_dict - list of 3 element tuples (vertex_begin, vertex_end, label)
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

    def to_string(self):
        for vertex in self.labels_dict:
            print("vertexID: ",vertex, " vertexLabel",  self.labels_dict.get(vertex))
            for edge in self.outgoing_edges_dict.get(vertex):
                print(edge, end=", ")
            print()
            for edge in self.ingoing_edges_dict.get(vertex):
                print(edge, end=", ")
            print()


g = Graph(['A', 'G', 'H'], [(0,1,"asd"), (1,2,"sdf")])
g.add_vertex("U")
g.add_edges([(3, 2, "dfg")])
g.remove_vertex(3)
g.to_string()