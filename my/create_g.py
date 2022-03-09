from ut.graph import *
from ut.graph_io import *


def createPath(n):
    G = Graph(False)
    G.add_vertex(Vertex(G, f'v1'))
    for i in range(2, n + 1):
        G.add_vertex(Vertex(G, f'v{i}'))
        G.add_edge(Edge(G.vertices[i - 2], G.vertices[i - 1]))
    return G


def createCycle(n):
    G = createPath(n)
    G.add_edge(Edge(G.vertices[0], G.vertices[-1]))
    return G


def createConnected(n):
    G = Graph(False)
    G.add_vertex(Vertex(G, f'v1'))
    for i in range(1, n):
        G.add_vertex(Vertex(G, f'v{i + 1}'))
        for e in range(0, len(G.vertices) - 1):
            G.add_edge(Edge(G.vertices[i], G.vertices[e]))
    return G


def createComplement(path: str, g: "Graph" = "null") -> "Graph":
    if path != "null":
        with open(path) as i:
            G = load_graph(i)
    else:
        path = "examples/complement"
        G = g
    C = Graph(False)
    handleGraph(C, createCDict(G))
    with open(f'{path}_C', 'w') as o:
        save_graph(C, o)
    return C


def getDisjoint(g1, g2):
    return g1 + g2


with open('../dot/mygraph_f1.dot', 'w') as f1:
    write_dot(createPath(3), f1)

with open('../dot/mygraph_f2.dot', 'w') as f2:
    write_dot(createCycle(5), f2)

with open('../dot/mygraph_f3.dot', 'w') as f3:
    write_dot(createConnected(5), f3)

with open('../dot/mygraph_d.dot', 'w') as d:
    write_dot(getDisjoint(createPath(3), createCycle(5)), d)
