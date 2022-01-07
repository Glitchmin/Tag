from graph import *
import os


def input_graph() -> Graph:
    g = Graph(['A', 'G', 'H'], [(0, 1, "asd"), (1, 2, "sdf")])
    g.add_vertex("U")
    g.add_edges([(3, 2, "dfg")])
    g.remove_vertex(3)
    return g


def graph_terminal_input():
    terminal_graph = Graph(['A'], [(0, 0, "asd")])
    terminal_graph.clear()
    vertex_quantity = "not digit"
    while not vertex_quantity.isdigit() or (vertex_quantity.isdigit() and int(vertex_quantity) == 0):
        vertex_quantity = input("give a quantity of vertexes (vertexes are indexed from 0): ")
        if not vertex_quantity.isdigit() or int(vertex_quantity) == 0:
            print("vertex quantity myst be a positive integer")
    vertex_quantity = int(vertex_quantity)

    for i in range(vertex_quantity):
        terminal_graph.add_vertex(str(input("vertex %d label: " % i)))
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
                terminal_graph.add_edge((int(edge_input[0]), int(edge_input[1]), edge_input[2]))
    return terminal_graph


def production_terminal_input():
    print("lhs")
    lhs = graph_terminal_input()
    print("rhs")
    rhs = graph_terminal_input()
    connecting_edges_quantity = int(input("connecting edges quantity: "))
    connecting_edges = []
    for i in range(connecting_edges_quantity):
        while True:
            new_edge_properties = input("is_outgoing label rhs_vertices_indexes: ")
            new_edge_properties = new_edge_properties.split()
            if len(new_edge_properties) < 3:
                print("too few arguments")
            elif new_edge_properties[0] == "0" or new_edge_properties[0] == "1":
                rhs_vertices = []
                correct = True
                for j in range(2, len(new_edge_properties)):
                    if not new_edge_properties[j].isdigit():
                        correct = False
                        break
                    elif int(new_edge_properties[j]) >= len(rhs.labels_dict):
                        correct = False
                        break
                    rhs_vertices.append(int(new_edge_properties[j]))

                if correct:
                    break
                else:
                    print("wrong vertices indexes")
            else:
                print("is outgoing must be 0 or 1")

        is_outgoing = False
        if new_edge_properties[0] == "1":
            is_outgoing = True
        connecting_edges.append(NewEdgesDefinition(is_outgoing, new_edge_properties[1], rhs_vertices))

    input_production = Production(lhs, rhs,connecting_edges)
    return input_production


if __name__ == "__main__":
    # graph = input_graph()
    # graph.print()
    print("input main graph")
    graph = graph_terminal_input()
    production_quantity = int(input("production quantity: "))
    productions = []
    for i in range(production_quantity):
        productions.append(production_terminal_input())
