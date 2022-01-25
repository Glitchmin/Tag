import unittest

from graph import Graph
from production import Production


class GraphProductionTest(unittest.TestCase):

    def test_validate(self):
        graph1 = Graph(['A'], [])
        self.assertTrue(graph1.validate(Graph(['A'], []), {0: 0}))
        self.assertFalse(graph1.validate(Graph(['B'], []), {0: 0}))

        graph2 = Graph(['A', 'B'], [(0, 1, 'ab')])
        self.assertTrue(graph2.validate(Graph(['A'], []), {0: 0}))
        self.assertFalse(graph2.validate(Graph(['A', 'B'], [(0, 1, "different")]), {0: 0, 1: 1}))
        self.assertFalse(graph2.validate(Graph(['A', 'B'], [(1, 0, "ab")]), {0: 0, 1: 1}))
        self.assertFalse(graph2.validate(Graph(['A', 'B'], []), {0: 0, 1: 1}))
        self.assertTrue(graph2.validate(Graph(['B'], []), {0: 1}))
        self.assertFalse(graph2.validate(Graph(['B'], []), {0: 0}))
        self.assertFalse(graph2.validate(Graph(['A'], []), {0: 1}))

    def test_find_considered_vertices(self):
        graph = Graph(['A', 'B', 'C', 'D', 'E'], [(0, 2, 'yes'), (1, 2, 'yes'), (3, 2, 'no'), (2, 3, 'yes'), (2, 4, 'no')])
        outgoing_set = graph.find_considered_vertices(True, 'yes', 2)
        ingoing_set = graph.find_considered_vertices(False, 'yes', 2)
        correct_outgoing_set = {3}
        correct_ingoing_set = {0, 1}
        self.assertEqual(correct_outgoing_set, outgoing_set)
        self.assertEqual(correct_ingoing_set, ingoing_set)


if __name__ == '__main__':
    unittest.main()
