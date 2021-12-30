from typing import List


class NewEdgesDefinition:
    def __init__(self, is_outgoing: bool, label: str, rhs_vertices: List[int]):
        self.is_outgoing = is_outgoing
        self.label = label
        self.rhs_vertices = rhs_vertices
