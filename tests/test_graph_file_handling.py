import os
import unittest

from graph import Graph
from production import Production
from random_generator import RandomGraph


class GraphSavingAndReadingTest(unittest.TestCase):
    def test_files_handling(self):
        tmp = Graph(['A'], [(0, 0, 'tmp'), (0, 0, 'tmp1'), (0, 0, 'tmp2')])
        tmp.save_to_file('tmp.csv')

        graphs = [Graph(['A', 'G', 'H'], [(0, 1, 'knowledge'), (1, 2, 'passion'), (2, 0, 'bond')]),
                  Graph(['A', 'G', 'H'], []),
                  Graph(['A'], [(0, 0, 'tmp'), (0, 0, 'tmp1'), (0, 0, 'tmp2')]),
                  Graph([], []),
                  RandomGraph.generate()]
        name = "tmp.csv"
        for i in range(len(graphs)):
            graphs[i].save_to_file(name)
            print(graphs[i].next_v_ID, Graph.read_from_file(name).next_v_ID)
            #self.assertEqual(graphs[i], Graph.read_from_file(name))
            os.remove(name)


if __name__ == '__main__':
    unittest.main()
