import unittest

from graph import Graph
from production import Production


class GraphTest(unittest.TestCase):

    def test_validate(self):
        graph1 = Graph(['A'], [])
        self.assertTrue(graph1.validate(Graph(['A'], []), {0: 0}))
        self.assertFalse(graph1.validate(Graph(['B'], []), {0: 0}))

        graph2 = Graph(['A', 'B'], [(0, 1, 'ab')])
        self.assertTrue (graph2.validate(Graph(['A'], []), {0: 0}))
        self.assertFalse(graph2.validate(Graph(['A', 'B'], [(0, 1, "different")]), {0: 0, 1: 1}))
        self.assertFalse(graph2.validate(Graph(['A', 'B'], [(1, 0, "ab")]), {0: 0, 1: 1}))
        self.assertFalse(graph2.validate(Graph(['A', 'B'], []), {0: 0, 1: 1}))
        self.assertTrue (graph2.validate(Graph(['B'], []), {0: 1}))
        self.assertFalse(graph2.validate(Graph(['B'], []), {0: 0}))
        self.assertFalse(graph2.validate(Graph(['A'], []), {0: 1}))



if __name__ == '__main__':
    unittest.main()
