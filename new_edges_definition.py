from typing import List
from typing import Tuple


class NewEdgesDefinition:
    def __init__(self, is_outgoing: bool, label: str, lhs_index: int, rhs_vertices: List[Tuple[int, str, bool]]):
        """for every <is_outgoing> edge with <label> removed during removing
        right graph from the start graph create edges to <rhs_vertices>
        rhs - right hand side of the production
        rhs_vertices[Tuple[RHS_vertex_index, new_edge_label, new_edge_direction]]"""
        self.is_outgoing = is_outgoing
        self.label = label
        self.rhs_vertices = rhs_vertices
