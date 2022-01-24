from graph import *
from copy import deepcopy
from graph_history import *
from termianl_input import *
import os.path


def input_graph() -> Graph:  # do wywalenia soon
    g = Graph(['A', 'G', 'H'], [(0, 1, "asd"), (1, 2, "sdf")])
    g.add_vertex("U")
    g.add_edges([(3, 2, "dfg")])
    g.remove_vertex(3)
    return g


if __name__ == "__main__":
    print("input main graph")
    graph = TerminalInput.graph_terminal_input(True)
    graph_history = GraphHistory()
    graph_history.add(graph)
    graph.print()
    productions = TerminalInput.productions_terminal_input()

    for production in productions:
        production.save_to_file()

    while True:
        graph = graph_history.get_current()
        graph.print()
        # TODO here graph should be painted
        prod = input("enter production id and on which vertices it should be used: ")
        prod = prod.split()
        if len(prod) == 0 or not all(el.isdigit() for el in prod):
            print('wrong input')
            continue

        prod = list(map(int, prod))
        prod_id = int(prod[0])
        vertices = prod[1:]
        if 0 > prod_id or prod_id >= len(productions):
            print("wrong production id")
            continue

        if any(not (0 <= i < graph.vertices_number()) for i in prod):
            print("wrong vertex id")
            continue

        mapping = {}
        for lhs_id, main_id in enumerate(vertices):
            mapping.update({lhs_id: main_id})
        graph_history.add(deepcopy(graph))
        try:
            graph.apply_production(productions[prod_id], mapping)
        except ValueError as e:
            print(e)
            continue
