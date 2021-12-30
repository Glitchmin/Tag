from __future__ import annotations

from graph import *
from new_edges_definition import *


class Production:
    def __init__(self, left_graph: Graph, right_graph: Graph, new_edges_defs: List[NewEdgesDefinition]):
        """rhs - right hand side of the production"""
        self.left_graph = left_graph
        self.right_graph = right_graph
        self.new_edges_defs = new_edges_defs
