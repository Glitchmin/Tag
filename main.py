from graph import *


def input_graph() -> Graph:
    g = Graph(['A', 'G', 'H'], [(0, 1, "asd"), (1, 2, "sdf")])
    g.add_vertex("U")
    g.add_edges([(3, 2, "dfg")])
    g.remove_vertex(3)
    return g


def terminal_input():
    graph = Graph(['A'], [(0, 0, "asd")])
    graph.clear()
    vertex_quantity = "not digit"
    while not vertex_quantity.isdigit() or (vertex_quantity.isdigit() and int(vertex_quantity) == 0):
        vertex_quantity = input("give a quantity of vertexes (vertexes are indexed from 0): ")
        if not vertex_quantity.isdigit() or int(vertex_quantity) == 0:
            print("vertex quantity myst be a positive integer")
    vertex_quantity = int(vertex_quantity)

    for i in range(vertex_quantity):
        graph.add_vertex(str(input("vertex %d label: " % i)))
    edge_input = "not end"
    print("input data format: starting_vertex_index ending_vertex_index label\n"
          'to end edges input type "end" ')

    while edge_input != "end":
        edge_input = input("edge: ")
        if edge_input == "end":
            break
        edge_input = edge_input.split()
        if len(edge_input) < 3:
            print("incomplete data (label is always requierd)")
        else:
            for i in range(3, len(edge_input)):
                edge_input[2] += " " + edge_input[i]
            if not edge_input[0].isdigit() or not edge_input[1].isdigit() or int(edge_input[0]) >= vertex_quantity or int(edge_input[1]) >= vertex_quantity:
                print("edge must begin and end in a existing vertex")
            else:
                graph.add_edge((int(edge_input[0]), int(edge_input[1]), edge_input[2]))
    return graph


if __name__ == "__main__":
    graph = input_graph()
    graph.print()
    graph = terminal_input()
    graph.print()
