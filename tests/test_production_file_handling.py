import unittest
import graph
from graph import *


class MyTestCase(unittest.TestCase):
    def test_something(self):
        production = Production(graph.Graph(['A'], [(0, 0, "abc")]), graph.Graph(['A'], [(0, 0, "acd")]),
                                [NewEdgesDefinition(True, "a", [(0, "b")])])
        production.file_counter = 0
        production.save_to_file()
        production2 = production.read_from_file(1)
        for i in range(len(production.new_edges_defs)):
            print(production.new_edges_defs[i].is_outgoing, production.new_edges_defs[i].label,
                  production.new_edges_defs[i].rhs_vertices)
            self.assertEqual(production.new_edges_defs[i].is_outgoing, production2.new_edges_defs[i].is_outgoing)
            self.assertEqual(production.new_edges_defs[i].label, production2.new_edges_defs[i].label)
            self.assertEqual(production.new_edges_defs[i].rhs_vertices,
                             production2.new_edges_defs[i].rhs_vertices)
            self.assertEqual(production.new_edges_defs[i].rhs_vertices,
                             production2.new_edges_defs[i].rhs_vertices)


if __name__ == '__main__':
    unittest.main()
