from graph import *
from copy import deepcopy
from graph_history import *


def input_graph() -> Graph:  # do wywalenia soon
    g = Graph(['A', 'G', 'H'], [(0, 1, "asd"), (1, 2, "sdf")])
    g.add_vertex("U")
    g.add_edges([(3, 2, "dfg")])
    g.remove_vertex(3)
    return g


def input_quantity(value_name: str) -> int:
    quantity = "not a quantity"
    while not quantity.isdigit() or (quantity.isdigit() and int(quantity) == 0):
        quantity = input("give a quantity of %s (%s are indexed from 0): " % (value_name, value_name))
        if not quantity.isdigit() or int(quantity) == 0:
            print("%s quantity must be a positive integer" % value_name)
    return int(quantity)


def input_vertices(terminal_graph: Graph):
    vertices_quantity = input_quantity("vertices")
    for vertex_nb in range(int(vertices_quantity)):
        terminal_graph.add_vertex(str(input("vertex %d label: " % vertex_nb)))
    return int(vertices_quantity)


def edge_input_parse(edge_input: List[str], vertices_quantity: int) -> bool:
    for label_part in range(3, len(edge_input)):
        edge_input[2] += " " + edge_input[label_part]
    if not edge_input[0].isdigit() or not edge_input[1].isdigit() or int(edge_input[0]) >= vertices_quantity or int(
            edge_input[1]) >= vertices_quantity:
        print("edge must begin and end in a existing vertex")
        return False
    return True


def input_edge(terminal_graph: Graph):
    edge_input = "not end"
    print("input data format: starting_vertex_index ending_vertex_index label\n"
          'to end edges input type "end" ')
    vertices_quantity = len(terminal_graph.labels_dict)
    while edge_input != "end":
        edge_input = input("edge: ")
        if edge_input == "end":
            break
        edge_input = edge_input.split()
        if len(edge_input) < 3:
            print("incomplete data (label is always required)")
        else:
            if edge_input_parse(edge_input, vertices_quantity):
                terminal_graph.add_edge((int(edge_input[0]), int(edge_input[1]), edge_input[2]))


def graph_terminal_input(is_main=False) -> Graph:
    while True and is_main:
        which_graph = input('If you want to enter new graph type "1", if you want to read from file type "0"')
        if which_graph == '0':
            return Graph.read_from_file()
        if which_graph == '1':
            break
    terminal_graph = Graph([], [])
    input_vertices(terminal_graph)
    input_edge(terminal_graph)
    terminal_graph.save_to_file()
    return terminal_graph


def input_rhs_vertices(rhs_vertices_quantity: int) -> List[int]:
    invalid_data = True
    rhs_vertices = []
    while invalid_data:
        invalid_data = False
        rhs_vertices_input = input("rhs_vertices_indexes: ")
        rhs_vertices_input = rhs_vertices_input.split()
        rhs_vertices = []
        for rhs_vertex in range(len(rhs_vertices_input)):
            if not rhs_vertices_input[rhs_vertex].isdigit() or int(
                    rhs_vertices_input[rhs_vertex]) >= rhs_vertices_quantity:
                print("wrong vertices indexes")
                invalid_data = True
                break
            else:
                rhs_vertices.append(int(rhs_vertices_input[rhs_vertex]))
    return rhs_vertices


def input_new_edge(rhs_vertices_quantity: int) -> NewEdgesDefinition:
    while True:
        is_outgoing = input("is outgoing (0 or 1): ")
        if is_outgoing != '0' and is_outgoing != '1':
            print("wrong is_outgoing value")
            continue
        elif is_outgoing == '1':
            is_outgoing = True
        else:
            is_outgoing = False
        new_edge_label = input("label: ")
        return NewEdgesDefinition(is_outgoing, new_edge_label, input_rhs_vertices(rhs_vertices_quantity))


def input_new_production() -> Production:
    print("lhs")
    lhs = graph_terminal_input()
    print("rhs")
    rhs = graph_terminal_input()
    connecting_edges_quantity = input_quantity("connecting edges")
    connecting_edges = []
    for _ in range(connecting_edges_quantity):
        connecting_edges.append(input_new_edge(len(rhs.labels_dict)))
    input_production = Production(lhs, rhs, connecting_edges)
    return input_production


def productions_terminal_input() -> List[Production]:
    while True:
        which_graph = input('If you want to enter new productions type "1", if you want to read from file type "0"')
        if which_graph == '0':
            return []  # TODO productions read from file
        if which_graph == '1':
            break
    production_quantity = input_quantity("productions")
    production_list = []
    for i in range(production_quantity):
        production_list.append(input_new_production())
    return production_list


if __name__ == "__main__":
    print("input main graph")
    graph = graph_terminal_input(True)
    graph_history = GraphHistory()
    graph_history.add(graph)
    graph.print()
    productions = productions_terminal_input()

    while True:
        graph = graph_history.get_current()
        graph.print()
        # TODO here graph should be painted
        prod = input("enter production id and on which vertices it should be used")
        prod = prod.split(" ")
        prod_id = int(prod[0])
        vertices = prod[1:]
        if 0 > prod_id or prod_id >= len(productions):
            print("wrong production id")
            continue
        mapping = {}
        for lhs_id, main_id in enumerate(vertices):
            mapping.update({lhs_id: main_id})
        graph_history.add(deepcopy(graph))
        try:
            graph.apply_production(productions[prod_id], mapping)
        except ValueError:
            continue
