from typing import List
from typing import Tuple


class NewEdgesDefinition:
    def __init__(self, is_outgoing: bool, label: str, lhs_index: int, new_edges_params: List[Tuple[str, int, str, bool]]):
        """
        Seating transformation description:
            Find all edges that matches (it can be more than 1) (if matches 0 we just ignore it):
                is_outgoing (direction),
                it's label is label
                it is connected to vertex with index lhs_index in LHS graph
            Let considered_vertices be set of vertices that contains vertices which are connected to lhs_index with matching edges

            Then insert new edges in place of found edges
            Each new edge is described with 4 params:
                it's label is new_edge_label
                it's direction is is_outgoing (in reference to RHS)
                it's ends are:
                    RHS_vertex_index
                    All vertices in rest of graph which met conditions:
                        have label Rest_of_graph_vertex_label
                        vertex ∈ considered_vertices

        rhs - right hand side of the production
        new_edges_params[Tuple[Rest_of_graph_vertex_label, RHS_vertex_index, new_edge_label, is_outgoing]]"""
        self.is_outgoing = is_outgoing
        self.label = label
        self.lhs_index = lhs_index
        self.new_edges_params = new_edges_params

