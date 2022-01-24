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
from termianl_input import *


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
