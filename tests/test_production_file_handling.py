import unittest
from production import Production
import graph


class MyTestCase(unittest.TestCase):
    def test_something(self):
        production = Production(graph.Graph(['A'], [(0, 0, "abc")]), graph.Graph(['A'], [(0, 0, "acd")]), [])
        file_num = production.save_to_file()
        production2 = production.read_from_file(file_num)
        self.assertTrue(production.new_edges_defs == production2.new_edges_defs)


if __name__ == '__main__':
    unittest.main()
