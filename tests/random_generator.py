from graph import *
from copy import deepcopy
from graph_history import *
import random


class RandomGraph:
    @staticmethod
    def generate():
        vertices_quantity = random.randint(1, 20)
        labels_list = []
        edges_list = []
        for i in range(vertices_quantity):
            labels_list.append(chr(random.randint(65, 81)))
        for i in range(random.randint(0, 40)):
            edges_list.append((random.randint(0, vertices_quantity-1),
                               random.randint(0, vertices_quantity-1),
                               chr(random.randint(65, 101))))

        return Graph(labels_list, edges_list)
