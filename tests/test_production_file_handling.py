import unittest
import graph
from graph import *


def compare_prods(production1: Production, production2: Production) -> bool:
    answer = (len(production1.new_edges_defs) == len(production2.new_edges_defs))
    answer = answer and production1.left_graph == production2.left_graph
    answer = answer and production1.right_graph == production2.right_graph
    for i in range(len(production1.new_edges_defs)):
        print(production1.new_edges_defs[i].is_outgoing, production1.new_edges_defs[i].label,
              production1.new_edges_defs[i].lhs_index, production1.new_edges_defs[i].new_edges_params, end=' =? ')

        print(production2.new_edges_defs[i].is_outgoing, production2.new_edges_defs[i].label,
              production2.new_edges_defs[i].lhs_index, production2.new_edges_defs[i].new_edges_params)

        answer = answer and (production1.new_edges_defs[i].is_outgoing == production2.new_edges_defs[i].is_outgoing)

        answer = answer and (production1.new_edges_defs[i].label == production2.new_edges_defs[i].label)

        answer = answer and (production1.new_edges_defs[i].lhs_index == production2.new_edges_defs[i].lhs_index)

        answer = answer and (
                production1.new_edges_defs[i].new_edges_params == production2.new_edges_defs[i].new_edges_params)
    return answer


class ProductionFileHandlingTest(unittest.TestCase):
    def test_production_file_handling(self):
        production = Production(graph.Graph(['A'], [(0, 0, "abc")]), graph.Graph(['A'], [(0, 0, "acd")]),
                                [NewEdgesDefinition(True, "a", 0, [("a", 0, "c", True), ("d", 1, "e", False)])])
        file_num = production.save_to_file()
        production2 = Production.read_from_file(file_num)
        self.assertTrue(compare_prods(production, production2))

        print()

        production4 = Production(graph.Graph(['B'], [(0, 0, "ddc")]), graph.Graph(['A'], [(0, 0, "acd")]),
                                 [NewEdgesDefinition(False, "b", 0, [("c", 0, "d", True), ("d", 1, "e", False)])])

        production4.save_to_file(1)
        production3 = Production.read_from_file(1)
        self.assertTrue(compare_prods(production4, production3))

        file_number = production4.save_to_file()
        production3 = Production.read_from_file(file_number)
        self.assertTrue(compare_prods(production4, production3))

        file_number = production4.save_to_file()
        production3 = Production.read_from_file(file_number)
        self.assertTrue(compare_prods(production4, production3))

        file_number = production4.save_to_file()
        production3 = Production.read_from_file(file_number)
        self.assertTrue(compare_prods(production4, production3))

        file_number = production4.save_to_file()
        production3 = Production.read_from_file(file_number)
        self.assertTrue(compare_prods(production4, production3))


if __name__ == '__main__':
    unittest.main()
