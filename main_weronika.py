from tkinter import *
from graph import *
import time
import pygraphviz as pgv
from production import Production
from new_edges_definition import *
from PIL import Image
import pygame

def paintLabel(g, labels_dict, display_surface, repaint):
    pygame.init()
    if not repaint:
        pygame.display.set_caption('Image')
        image = pygame.image.load(r'productions.jpg')
        display_surface.blit(image, (0, 0))
    background = pygame.Surface((80, 600))
    background.fill((172, 255, 175))
    display_surface.blit(background, (520, 0))
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    i = 0
    for key, value in labels_dict.items():
        textsurface = myfont.render("  " + str(key) + " -> " + value, False, (0, 0, 0))
        display_surface.blit(textsurface, (520, 50 * i))
        i += 1
    pygame.display.update()


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
    print(g.get_edges())
    A = pgv.AGraph(D)
    for i in g.get_edges():
        edge = A.get_edge(i[0], i[1])
        edge.attr['label'] = i[2]
    A.edge_attr.update(forcelabels=True)
    A.write(name)
    A.layout(prog="dot")
    A.draw(name2)


def paint(g, productions, display_surface):
    paintg(g, "file.dot", "file.png")
    i = 0
    new_image = Image.new('RGB', (2300, 2000), (500, 500, 500))
    name = Image.open('napis.png')
    labels_dict = g.labels_dict
    paintLabel(g, labels_dict, display_surface, False)
    new_image.paste(name, (0, 0))
    for production in productions:
        Left = production.right_graph
        paintg(Left, "left" + str(i) + ".dot", "left" + str(i) + ".png")
        Right = production.right_graph
        paintg(Right, "right" + str(i) + ".dot", "right" + str(i) + ".png")
        imageR = Image.open("right" + str(i) + ".png")
        imageL = Image.open("left" + str(i) + ".png")
        imageR = imageR.resize((200, 200))
        imageL = imageL.resize((200, 200))
        new_image.paste(imageL, (0, 0 + 240 * i + 120))
        new_image.paste(imageR, (200, 0 + 240 * i + 120))
        i += 1

    graph = Image.open("file.png")
    graph = graph.resize((1520, 1800))
    new_image.paste(graph, (400, 0))
    new_image = new_image.resize((600, 600))
    new_image.save(r'productions.jpg')
    img = pygame.image.load("productions.jpg")
    display_surface.blit(img, (0, 0))


def repaint(g, display_surface):
    paintg(g, 'file.dot', 'file.png')
    graph = Image.open('file.png')
    new = Image.open("productions.jpg")
    new = new.resize((2300, 2000))
    graph = graph.resize((1520, 1800))
    new.paste(graph, (400, 0))
    new = new.resize((600, 600))
    new.save(r'update.jpg')
    i = pygame.image.load('update.jpg')
    display_surface.blit(i, (0, 0))
    labels = g.labels_dict
    paintLabel(g, labels, display_surface, True)
    pygame.display.set_caption('Image')
    pygame.display.update()


def input_graph() -> Graph:
    Maing = Graph(['A', 'G', 'H'], [(0, 1, "asd"), (1, 2, "sdf")])
    g = Graph(['A', 'G', 'H'], [(0, 1, "asd"), (1, 2, "sdf")])
    g.add_vertex("U")
    g.add_edges([(3, 2, "dfg")])
    left_graph = Graph(['f', 'g', 's'], [(0, 1, "asd"), (1, 2, "sdf")])
    right_graph = Graph(['m', 't', 'r'], [(0, 1, "asd"), (1, 2, "sdf")])

    a = NewEdgesDefinition(1, "hj", [1, 2, 3])
    p = Production(left_graph, right_graph, a)
    left = Graph(['TAU', 'TEKO', 'TANKO'], [(2, 1, "KRM"), (1, 0, "sdf")])
    right = Graph(['OPO', 'TORO', 'RMO'], [(0, 1, "asd")])
    p2 = Production(left, right, a)

    pygame.init()
    display_surface = pygame.display.set_mode((600, 600))
    paint(g, [p, p2], display_surface)
    time.sleep(2)
    a = Graph(['A', 'G', 'H'], [(0, 1, "asd"), (1, 2, "sdf"), (2, 0, "elo")])
    repaint(a, display_surface)
    time.sleep(2)
    a = Graph(['daw', 'te', 'na', 'dz', 'za'],
              [(0, 1, "asd"), (1, 2, "sdf"), (2, 0, "elo"), (1, 4, "sdf"), (1, 3, "sdf"), (3, 2, "sdf"), (4, 2, "sdf")])
    repaint(a, display_surface)
    time.sleep(2)

if __name__ == "__main__":
    graph = input_graph()
    # graph.print()
