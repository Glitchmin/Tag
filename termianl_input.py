from graph import *
import os


class TerminalInput:
    @staticmethod
    def input_graph() -> Graph:  # do wywalenia soon
        g = Graph(['A', 'G', 'H'], [(0, 1, "asd"), (1, 2, "sdf")])
        g.add_vertex("U")
        g.add_edges([(3, 2, "dfg")])
        g.remove_vertex(3)
        return g

    @staticmethod
    def input_quantity(value_name: str) -> int:
        quantity = "not a quantity"
        while not quantity.isdigit():
            quantity = input("give a quantity of %s (%s are indexed from 0): " % (value_name, value_name))
            if not quantity.isdigit():
                print("%s quantity must be a non negative integer" % value_name)
        return int(quantity)

    @staticmethod
    def input_vertices(terminal_graph: Graph):
        vertices_quantity = TerminalInput.input_quantity("vertices")
        for vertex_nb in range(int(vertices_quantity)):
            terminal_graph.add_vertex(str(input("vertex %d label: " % vertex_nb)))
        return int(vertices_quantity)

    @staticmethod
    def edge_input_parse(edge_input: List[str], vertices_quantity: int) -> bool:
        for label_part in range(3, len(edge_input)):
            edge_input[2] += " " + edge_input[label_part]
        if not edge_input[0].isdigit() or not edge_input[1].isdigit() or int(edge_input[0]) >= vertices_quantity or int(
                edge_input[1]) >= vertices_quantity:
            print("edge must begin and end in a existing vertex")
            return False
        return True

    @staticmethod
    def input_edge(terminal_graph: Graph):
        edge_input = "not end"
        print("input data format: starting_vertex_index ending_vertex_index label\n"
              'to end edges input type "end" ')
        vertices_quantity = len(terminal_graph.labels_dict)
        while edge_input != "end":
            edge_input = input("edge: ")
            if edge_input == "end":
                break
            edge_input = edge_input.split()
            if len(edge_input) < 3:
                print("incomplete data (label is always required)")
            else:
                if edge_input_parse(edge_input, vertices_quantity):
                    terminal_graph.add_edge((int(edge_input[0]), int(edge_input[1]), edge_input[2]))

    @staticmethod
    def choose_graph():
        return input('If you want to enter new productions type "1", if you want to read from file type "0": ')

    @staticmethod
    def graph_terminal_input(is_main=False) -> Graph:
        while True and is_main:
            which_graph = TerminalInput.choose_graph()
            if which_graph == '0':
                return Graph.read_from_file()
            if which_graph == '1':
                break
        terminal_graph = Graph([], [])
        input_vertices(terminal_graph)
        input_edge(terminal_graph)
        terminal_graph.save_to_file()
        return terminal_graph

    @staticmethod
    def input_rhs_vertices(rhs_vertices_quantity: int) -> List[int]:
        invalid_data = True
        rhs_vertices = []
        while invalid_data:
            invalid_data = False
            rhs_vertices_input = input("rhs_vertices_indexes: ")
            rhs_vertices_input = rhs_vertices_input.split()
            rhs_vertices = []
            for rhs_vertex in range(len(rhs_vertices_input)):
                if not rhs_vertices_input[rhs_vertex].isdigit() or int(
                        rhs_vertices_input[rhs_vertex]) >= rhs_vertices_quantity:
                    print("wrong vertices indexes")
                    invalid_data = True
                    break
                else:
                    rhs_vertices.append(int(rhs_vertices_input[rhs_vertex]))
        return rhs_vertices

    @staticmethod
    def input_new_edge(rhs_vertices_quantity: int) -> NewEdgesDefinition:  # TODO change rhs vertices to include labels
        while True:
            is_outgoing = input("is outgoing (0 or 1): ")
            if is_outgoing != '0' and is_outgoing != '1':
                print("wrong is_outgoing value")
                continue
            elif is_outgoing == '1':
                is_outgoing = True
            else:
                is_outgoing = False
            new_edge_label = input("label: ")
            return NewEdgesDefinition(is_outgoing, new_edge_label, input_rhs_vertices(rhs_vertices_quantity))

    @staticmethod
    def input_new_production() -> Production:
        print("lhs")
        lhs = TerminalInput.graph_terminal_input()
        print("rhs")
        rhs = TerminalInput.graph_terminal_input()
        connecting_edges_quantity = TerminalInput.input_quantity("connecting edges")
        connecting_edges = []
        for _ in range(connecting_edges_quantity):
            connecting_edges.append(TerminalInput.input_new_edge(len(rhs.labels_dict)))
        input_production = Production(lhs, rhs, connecting_edges)
        return input_production

    @staticmethod
    def productions_terminal_input() -> List[Production]:
        production_list = []
        while True:
            which_prod = input('If you want to enter new productions type "1", if you want to read from file type "0"')
            if which_prod == '0':
                i = 1
                while os.path.isfile('productions/production' + str(i) + '_left.csv'):
                    print(i, "")
                    production_list.append(Production.read_from_file(i))
                    i += 1
                break

            if which_prod == '1':
                production_quantity = TerminalInput.input_quantity("productions")
                for i in range(production_quantity):
                    production_list.append(TerminalInput.input_new_production())
                break
        return production_list
