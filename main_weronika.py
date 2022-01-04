import sys

from graph import *
import matplotlib.pyplot as plt
import networkx as nx
from production import Production
from new_edges_definition import *
import sys
import time
def paintGraph(g):
    labels_dict = g.labels_dict
 #   labels_dict.update(p.left_graph.labels_dict)
 #   labels_dict.update(p.right_graph.labels_dict)
    edges: List[Tuple[int, int, str]] = []
    edge_labels = {}
    for x in g.get_edges():
        edges.append([labels_dict[x[0]], labels_dict[x[1]]])
        edge_labels[(labels_dict[x[0]], labels_dict[x[1]])] = x[2]
    G = nx.Graph()
    G.add_edges_from(edges)
    return (G,edge_labels)

def paintMainGraph(g):

    G, edge_labels = paintGraph(g)
    pos = nx.planar_layout(G)
    plt.figure()
    nx.draw(
        G, pos, edge_color='black', width=1, linewidths=1,
        node_size=500, node_color='pink', alpha=0.9,
        labels={node: node for node in G.nodes()}

    )
    # edge sa dobrze
    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels=edge_labels,
        font_color='red'
    )

    plt.axis('off')
    plt.show()



def paint(g,productions):

    G,edge_labels=paintGraph(g)
    for production in productions:
        Left,edge_labels2=paintGraph(production.left_graph)
        Right, edge_labels3 = paintGraph(production.left_graph)
        edge_labels.update(edge_labels2)
        edge_labels.update(edge_labels3)
        G.add_nodes_from(Left)
        G.add_nodes_from(Right)

    pos = nx.planar_layout(G)
    plt.figure()
    nx.draw(
        G, pos, edge_color='black', width=1, linewidths=1,
        node_size=500, node_color='pink', alpha=0.9,
        labels={node: node for node in G.nodes()}

    )
    #edge sa dobrze
    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels=edge_labels,
        font_color='red'
    )

    plt.axis('off')
    plt.show()


def input_graph() -> Graph:
    # randomowe dane
    Maing = Graph(['A', 'G', 'H'], [(0, 1, "asd"), (1, 2, "sdf")])
    g = Graph(['A', 'G', 'H'], [(0, 1, "asd"), (1, 2, "sdf")])
    g.add_vertex("U")
    g.add_edges([(3, 2, "dfg")])
    # g.remove_vertex(3)
    left_graph=Graph(['f', 'g', 's'], [(0, 1, "asd"), (1, 2, "sdf")])
    right_graph=Graph(['m', 't', 'r'], [(0, 1, "asd"), (1, 2, "sdf")])

    a=NewEdgesDefinition(1,"hj",[1,2,3])
    p=Production(left_graph,right_graph,a)
    left= Graph(['TAU', 'TEKO', 'TANKO'], [(2, 1, "KRM"), (1, 0, "sdf")])
    right = Graph(['OPO', 'TORO', 'RMO'], [(0, 1, "asd")])
    p2 = Production(left, right, a)




    paint(g,[p,p2])

    paintMainGraph(Maing)


    return g

if __name__ == "__main__":
    graph = input_graph()
    graph.print()
