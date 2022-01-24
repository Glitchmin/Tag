from __future__ import annotations

import platform
from pathlib import Path

import graph
from graph import *
from new_edges_definition import *

import csv


class Production:
    file_counter = 0

    def __init__(self, left_graph: Graph, right_graph: Graph, new_edges_defs: List[NewEdgesDefinition]):
        """rhs - right hand side of the production"""
        self.left_graph = left_graph
        self.right_graph = right_graph
        self.new_edges_defs = new_edges_defs

    def save_to_file(self): # TODO change rhs vertices to include labels
        directory_name = "productions\\" if ("Windows" in platform.system()) else "productions/"
        Path(directory_name).mkdir(parents=True, exist_ok=True)

        Production.file_counter += 1

        filename = 'productions/production' + str(Production.file_counter)
        self.left_graph.save_to_file(filename + '_left.csv')
        self.right_graph.save_to_file(filename + '_right.csv')

        new_edges_defs_data = [[] for _ in range(len(self.new_edges_defs))]
        for i in range(len(self.new_edges_defs)):
            new_edges_defs_data[i].append(self.new_edges_defs[i].is_outgoing)
            new_edges_defs_data[i].append(self.new_edges_defs[i].label)
            new_edges_defs_data[i].append(self.new_edges_defs[i].rhs_vertices)

        with open(filename + '_new_edges_defs.csv', 'w', newline='') as save_file:
            writer = csv.writer(save_file)
            writer.writerow([len(self.new_edges_defs)])
            writer.writerows(new_edges_defs_data)

    @staticmethod
    def read_from_file(file_number): # TODO change rhs vertices to include labels

        new_prod = Production(graph.Graph(['A'], [(0, 0, "asd")]), graph.Graph(['A'], [(0, 0, "asd")]), [])

        filename = 'productions/production' + str(file_number)
        new_prod.left_graph = graph.Graph.read_from_file(filename + '_left.csv')
        new_prod.right_graph = graph.Graph.read_from_file(filename + '_right.csv')

        with open(filename + '_new_edges_defs.csv', 'w', newline='') as save_file:
            new_edges_defs_data = csv.reader(save_file)

        for i in range(len(new_prod.new_edges_defs)):
            new_edges_defs_data[i].append(new_prod.new_edges_defs[i].is_outgoing)
            new_edges_defs_data[i].append(new_prod.new_edges_defs[i].label)
            new_edges_defs_data[i].append(new_prod.new_edges_defs[i].rhs_vertices)
        new_prod.new_edges_defs = new_edges_defs_data
        return new_prod
