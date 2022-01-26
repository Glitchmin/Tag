from __future__ import annotations

import platform
from pathlib import Path

import graph
from graph import *
from new_edges_definition import *

import csv


class Production:
    file_counter = -1

    def __init__(self, left_graph: Graph, right_graph: Graph, new_edges_defs: List[NewEdgesDefinition]):
        """rhs - right hand side of the production"""
        self.left_graph = left_graph
        self.right_graph = right_graph
        self.new_edges_defs = new_edges_defs

    def save_to_file(self, file_number=None):
        if file_number is None:
            file_number = Production.file_counter + 1

        directory_name = "productions\\" if ("Windows" in platform.system()) else "productions/"
        Path(directory_name).mkdir(parents=True, exist_ok=True)

        Production.file_counter = max(file_number, Production.file_counter)

        filename = 'productions/production' + str(file_number)
        print("saved", filename)
        self.left_graph.save_to_file(filename + '_left.csv')
        self.right_graph.save_to_file(filename + '_right.csv')

        new_edges_defs_data = [[] for _ in range(len(self.new_edges_defs))]
        for i in range(len(self.new_edges_defs)):
            new_edges_defs_data[i].append(self.new_edges_defs[i].is_outgoing)
            new_edges_defs_data[i].append(self.new_edges_defs[i].label)
            new_edges_defs_data[i].append(self.new_edges_defs[i].lhs_index)
            new_edges_defs_data[i].append(len(self.new_edges_defs[i].new_edges_params))
            for new_edge in self.new_edges_defs[i].new_edges_params:
                for j in range(0, 4):
                    new_edges_defs_data[i].append(new_edge[j])

        with open(filename + '_new_edges_defs.csv', 'w', newline='') as save_file:
            writer = csv.writer(save_file)
            writer.writerows(new_edges_defs_data)
        return file_number

    @staticmethod
    def read_from_file(file_number):

        new_prod = Production(graph.Graph(['A'], [(0, 0, "asd")]), graph.Graph(['A'], [(0, 0, "asd")]), [])

        filename = 'productions/production' + str(file_number)
        print("read", filename)
        new_prod.left_graph = graph.Graph.read_from_file(filename + '_left.csv')
        new_prod.right_graph = graph.Graph.read_from_file(filename + '_right.csv')

        with open(filename + '_new_edges_defs.csv', 'r+', newline='') as save_file:
            new_edges_defs_reader = csv.reader(save_file)
            new_edges_defs_data = []
            for new_edges_line in new_edges_defs_reader:

                a = []

                for i in range(3, 3 + 4 * int(new_edges_line[3]), 4):
                    print(new_edges_line[i + 4])
                    a.append((new_edges_line[i + 1], int(new_edges_line[i + 2]),
                              new_edges_line[i + 3], new_edges_line[i + 4] == 'True'))

                new_edges_defs_data.append(
                    NewEdgesDefinition((new_edges_line[0] == 'True'), new_edges_line[1], int(new_edges_line[2]), a))

            new_prod.new_edges_defs = new_edges_defs_data
        return new_prod

    def print(self):
        print("LHS")
        self.left_graph.print()
        print("RHS")
        self.right_graph.print()
        print("transformacja osadzenia")
        for new_edge_def in self.new_edges_defs:
            new_edge_def.print()
