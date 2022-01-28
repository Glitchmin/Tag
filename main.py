from graph import *
from copy import deepcopy
from graph_history import *
from termianl_input import *


def use_production(gh: GraphHistory):
    g = gh.get_current()
    prod = input("enter production id and on which vertices it should be used: ")
    prod = prod.split()
    if len(prod) == 0 or not all(el.isdigit() for el in prod):
        print('wrong input')
        return

    prod = list(map(int, prod))
    prod_id = int(prod[0])
    vertices = prod[1:]
    if 0 > prod_id or prod_id >= len(productions):
        print("wrong production id")
        return

    if any(i not in g.labels_dict for i in vertices):
        print("wrong vertex id")
        return

    if len(vertices) != len(productions[prod_id].left_graph.labels_dict):
        print("wrong number of indices for mapping")
        return

    mapping = {}
    for lhs_id, main_id in enumerate(vertices):
        mapping.update({lhs_id: main_id})
    try:
        g.apply_production(productions[prod_id], mapping)
    except ValueError as e:
        print("VALIDATE ERROR!!!")
        return
    gh.add(deepcopy(g))
    g.print()
    # TODO here graph should be painted


def restore_graph(gh: GraphHistory):
    gh.restore_graph()
    g = gh.get_current()
    print(g)


if __name__ == "__main__":
    print("input main graph")
    graph = TerminalInput.graph_terminal_input(True)
    graph.save_to_file()
    graph_history = GraphHistory()
    graph_history.add(graph)
    graph.print()
    productions = TerminalInput.productions_terminal_input()
    print("DEBUG Number of productions: ", len(productions))

    for production in productions:
        production.save_to_file()

    while True:
        use_production(graph_history)
