from typing import List
from typing import Tuple


class NewEdgesDefinition:
    def __init__(self, is_outgoing: bool, label: str, lhs_index: int, new_edges_params: List[Tuple[int, int, str, bool]]):
        """
        Seating transformation description:
            Find all edges that matches (it can be more than 1) (if matches 0 we just ignore it):
                is_outgoing (direction),
                it's label is label
                it is connected to vertex with index lhs_index in LHS graph
            Let V be set of vertices that contains vertices which are connected to lhs_index with matching edges

            Then insert new edges in place of found edges
            Each new edge is described with 4 params:
                it's ends are:
                    RHS_vertex_label(all in RHS with same label)
                    All vertices in rest of graph which met conditions:
                        have label Rest_of_graph_vertex_label
                        vertex ∈ V

        rhs - right hand side of the production
        rhs_vertices[Tuple[Rest_of_graph_vertex_label, RHS_vertex_label, new_edge_label, new_edge_direction]]"""
        self.is_outgoing = is_outgoing
        self.label = label
        self.lhs_index = lhs_index
        self.new_edges_params = new_edges_params

