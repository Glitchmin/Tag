import pathlib

from graph import *
from copy import deepcopy
from graph_history import *
from termianl_input import *


def use_production(gh: GraphHistory, productions: List[Production]):
    g = gh.get_current()
    prod = input("enter production id and on which vertices it should be used: ")
    prod = prod.split()
    if len(prod) == 0 or not all(el.isdigit() for el in prod):
        print('wrong input')
        return

    prod = list(map(int, prod))
    prod_id = int(prod[0])
    vertices = prod[1:]
    if prod_id < 0 or prod_id >= len(productions):
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
    g.print()
    # TODO here graph should be painted


def edit_production(productions: List[Production]):
    edited_ix = ""
    while True:
        edited_ix = input("enter the index of the production to be edited: ")
        if not edited_ix.isdigit() or not 0 <= int(edited_ix) < len(productions):
            print("Wrong index: it must be a number between 0 and ", len(productions))
        else:
            break

    edited_ix = int(edited_ix)
    productions[edited_ix] = TerminalInput.input_new_production()
    Production.save_to_file(productions[edited_ix], edited_ix)


def main():
    print("input main graph")
    graph = TerminalInput.graph_terminal_input(True)
    graph.save_to_file()
    graph_history = GraphHistory()
    graph_history.add(graph)
    graph.print()
    productions = TerminalInput.productions_terminal_input()

    for production in productions:
        production.save_to_file()

    while True:
        inp = input("p - apply production, r - restore graph, f - reload productions from files,\n e - edit production, pp - print productions, g - print graph: ")
        if inp == 'p':
            use_production(graph_history, productions)
        if inp == 'r':
            restore_graph(graph_history)
        if inp == 'f':
            productions = Production.read_all_productions()
            # TODO reprint productions
        if inp == 'e':
            edit_production(productions)
            # TODO reprint productions
        if inp == 'pp':
            for i in range(len(productions)):
                print("Production", i, ":")
                productions[i].print()
                print()
        if inp == 'g':
            graph_history.get_current().print()


if __name__ == "__main__":
    main()
