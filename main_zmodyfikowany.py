
import os.path
from copy import deepcopy
from graph_history import *
from tkinter import *
from graph import *
import pygraphviz as pgv
from production import Production
from new_edges_definition import *
from PIL import Image, ImageFont, ImageDraw
import pygame


def paintLabel(g, labels_dict):
    pygame.init()
    i = 0
    img = Image.open('productions.jpg', "r")
    font = ImageFont.truetype("Arial", 15)
    for key, value in labels_dict.items():
        text = ("  " + str(key) + " -> " + value)
        image_edible = ImageDraw.Draw(img)
        image_edible.text((520, 50 * i), text, (0, 0, 0), font=font)
        i += 1
        img.save(r'productions.jpg')
    img.close()


def paintg(g, name, name2):
    labels_dict = g.labels_dict
    D = {}
    edges = []
    edge_labels = {}
    print(labels_dict)
    for x in g.get_edges():
        a = x[0]
        dicta = {}
        for y in g.get_edges():
            if y[0] == a:
                dicta[y[1]] = y[2]
            if y[1] == a:
                dicta[y[0]] = y[2]
        D[a] = dicta
    A = pgv.AGraph(D, directed="True")
    for i in g.get_edges():
        edge = A.get_edge(i[0], i[1])
        edge.attr['label'] = i[2]
    A.edge_attr.update(forcelabels=True)
    A.write(name)
    A.layout(prog="dot")
    A.draw(name2)


def paint(g, productions):
    paintg(g, "file.dot", "file.png")
    i = 0
    new_image = Image.new('RGB', (2300, 2000), (500, 500, 500))
    name = Image.open('napis.png')
    labels_dict = g.labels_dict
    new_image.paste(name, (0, 0))
    name.close()
    for production in productions:
        Left = production.right_graph
        paintg(Left, "left" + str(i) + ".dot", "left" + str(i) + ".png")
        Right = production.left_graph
        paintg(Right, "right" + str(i) + ".dot", "right" + str(i) + ".png")
        imageR = Image.open("right" + str(i) + ".png")
        imageL = Image.open("left" + str(i) + ".png")
        imageR = imageR.resize((300, 200))
        imageL = imageL.resize((300, 200))
        new_image.paste(imageL, (0, 0 + 240 * i + 120))
        new_image.paste(imageR, (300, 0 + 240 * i + 120))
        i += 1
        imageL.close()
        imageR.close()

    graph = pgv.AGraph("file.dot")
    graph.layout(prog='dot')
    graph.draw("file.png")
    graph = Image.open("file.png")
    graph = graph.resize((1520, 1800))
    new_image.paste(graph, (600, 0))
    new_image = new_image.resize((600, 600))
    new_image.save(r'productions.jpg')
    paintLabel(g, labels_dict)
    new_image.close()
    graph.close()


def repaint(g, display_surface):
    paintg(g, 'file.dot', 'file.png')
    graph = Image.open('file.png')
    new = Image.open("productions.jpg")
    new = new.resize((2300, 2000))
    graph = graph.resize((1520, 1800))
    new.paste(graph, (400, 0))
    new = new.resize((600, 600))
    new.save(r'update.jpg')
    display_surface.blit(new, (0, 0))
    labels = g.labels_dict
    paintLabel(g, labels, display_surface, True)
    pygame.display.set_caption('Image')
    pygame.display.update()


def input_graph() -> Graph:  # do wywalenia soon
    g = Graph(['A', 'G', 'H'], [(0, 1, "asd"), (1, 2, "sdf")])
    g.add_vertex("U")
    g.add_edges([(3, 2, "dfg")])
    g.remove_vertex(3)
    return g


def input_quantity(value_name: str) -> int:
    quantity = "not a quantity"
    while not quantity.isdigit():
        quantity = input("give a quantity of %s (%s are indexed from 0): " % (value_name, value_name))
        if not quantity.isdigit() or int(quantity) == 0:
            print("%s quantity must be a non negative integer" % value_name)
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
    production_list = []
    while True:
        which_prod = input('If you want to enter new productions type "1", if you want to read from file type "0"')
        if which_prod == '0':
            i = 1
            while os.path.isfile('productions/production' + str(i) + '_left.csv'):
                print(i, "")
                production_list.append(Production.read_from_file(i))
                i += 1
            break

        if which_prod == '1':
            production_quantity = input_quantity("productions")
            for i in range(production_quantity):
                production_list.append(input_new_production())
            break
    return production_list


if __name__ == "__main__":
    print("input main graph")
    graph = graph_terminal_input(True)
    graph_history = GraphHistory()
    graph_history.add(graph)
    graph.print()
    productions = productions_terminal_input()

    for production in productions:
        production.save_to_file()

    while True:
        graph = graph_history.get_current()
        graph.print()
        pygame.init()
        display_surface = pygame.display.set_mode((600, 600))
        paint(graph, productions)
        img = pygame.image.load("productions.jpg")

        display_surface.blit(img, (0, 0))
        pygame.display.set_caption('Image')
        pygame.display.update()
        # TODO here graph should be painted

        prod = input("enter production id and on which vertices it should be used,if you wan a previous graph type: p")
        while prod == 'p':
            g = graph_history.get_current()
            paint(g, productions)
            img = pygame.image.load("productions.jpg")
            display_surface.blit(img, (0, 0))
            pygame.display.set_caption('Image')
            pygame.display.update()
            prod = input(
                "enter production id and on which vertices it should be used,if you wan a previous graph type: p")
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
