from graph import *


def input_graph() -> Graph:
    g = Graph(['A', 'G', 'H'], [(0, 1, "asd"), (1, 2, "sdf")])
    g.add_vertex("U")
    g.add_edges([(3, 2, "dfg")])
    g.remove_vertex(3)
    return g


if __name__ == "__main__":
    graph = input_graph()
