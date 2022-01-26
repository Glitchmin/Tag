import unittest
import graph
from graph import *


class production_file_handling_test(unittest.TestCase):
    def test_production_file_handling(self):
        production = Production(graph.Graph(['A'], [(0, 0, "abc")]), graph.Graph(['A'], [(0, 0, "acd")]),
                                [NewEdgesDefinition(True, "a", 0, [("a", 0, "c", True), ("d", 1, "e", False)])])
        production.file_counter = 0
        production.save_to_file()
        production2 = production.read_from_file(1)

        for i in range(len(production.new_edges_defs)):
            print(production.new_edges_defs[i].is_outgoing, production.new_edges_defs[i].label,
                  production.new_edges_defs[i].lhs_index, production.new_edges_defs[i].new_edges_params)

            print(production2.new_edges_defs[i].is_outgoing, production2.new_edges_defs[i].label,
                  production2.new_edges_defs[i].lhs_index, production2.new_edges_defs[i].new_edges_params)

            self.assertEqual(production.new_edges_defs[i].is_outgoing, production2.new_edges_defs[i].is_outgoing)

            self.assertEqual(production.new_edges_defs[i].label, production2.new_edges_defs[i].label)

            self.assertEqual(production.new_edges_defs[i].lhs_index,
                             production2.new_edges_defs[i].lhs_index)

            self.assertEqual(production.new_edges_defs[i].new_edges_params,
                             production2.new_edges_defs[i].new_edges_params)


if __name__ == '__main__':
    unittest.main()
