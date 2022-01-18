from typing import List
from typing import Tuple


class NewEdgesDefinition:
    def __init__(self, is_outgoing: bool, label: str, rhs_vertices: List[Tuple[int, str]]):
        """for every <is_outgoing> edge with <label> removed during removing
        right graph from the start graph create edges to <rhs_vertices>
        rhs - right hand side of the production"""
        self.is_outgoing = is_outgoing
        self.label = label
        self.rhs_vertices = rhs_vertices
