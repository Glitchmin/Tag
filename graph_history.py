from collections import deque
from graph import *


class GraphHistory:
    def __init__(self):
        self.graph_history = deque()

    def add(self, graph: Graph):
        self.graph_history.append(graph)

    def get_current(self):
        g = self.graph_history.pop()
        self.graph_history.append(g)
        return g

    def restore_graph(self):
        if len(self.graph_history) == 0:
            print('nothing to restore')
            return
        self.graph_history.pop()
