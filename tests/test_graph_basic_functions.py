import os
import unittest

from graph import Graph
from production import Production
from random_generator import RandomGraph


class GraphBasicFunctionTest(unittest.TestCase):
    def test_add_vertex(self):
        graph = Graph(['A'], [])
        correct_graph = Graph([], [])
        correct_graph.labels_dict.update({0: 'A'})
        correct_graph.ingoing_edges_dict.update({0: set({})})
        correct_graph.outgoing_edges_dict.update({0: set({})})
        correct_graph.next_v_ID = 1
        self.assertEqual(correct_graph, graph)

    def test_remove_vertex(self):
        graph = Graph(['A', 'G', 'H'], [(0, 1, 'knowledge'), (1, 2, 'passion'), (2, 0, 'bond')])
        graph.remove_vertex(2)
        correct_graph = Graph(['A', 'G'], [(0, 1, 'knowledge')])
        self.assertEqual(correct_graph, graph)


if __name__ == '__main__':
    unittest.main()
