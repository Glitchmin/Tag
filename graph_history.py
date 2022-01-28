from collections import deque
from graph import *
from copy import deepcopy


class GraphHistory:
    def __init__(self):
        self.graph_history = deque()

    def add(self, graph: Graph):
        self.graph_history.append(graph)

    def get_current(self) -> Graph:
        g = self.graph_history.pop()
        self.graph_history.append(g)
        return deepcopy(g)

    def restore_graph(self):
        if len(self.graph_history) == 1:
            print('nothing to restore')
            return
        self.graph_history.pop()
