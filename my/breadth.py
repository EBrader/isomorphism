from ut.graph import *
from ut.graph_io import *

queue = []
visited = {}


def labelling(n: int, dist: int, g: "Graph") -> "Vertex":
    return Vertex(g, f'n: {n} - d - {dist}')


def queueChildren(edges: list["Edge"], v_old: "Vertex", v_new: "Vertex", dist: int):
    for e in edges:
        if e.tail.label == v_old.label:
            queue.append((v_new, e.head, dist + 1))


def isConnected(g: "Graph"):
    return (len(g.vertices) - 1) == len(g.edges)


def isVisited(v: "Vertex") -> bool:
    return v in visited.keys()


def getVisited(v: "Vertex") -> "Vertex":
    return visited.get(v)


def visitQueue(g_old: "Graph", g_new: "Graph", n: int):
    if queue:
        q = queue.pop(0)
        vp_new = q[0]
        vc_old = q[1]
        if isVisited(vc_old):
            vc_new = getVisited(vc_old)
            dist = 1
            n -= 1
        else:
            global visited
            dist = q[2]
            vc_new = labelling(n, dist, g_new)
            visited[vc_old] = vc_new
            queueChildren(g_old.edges, vc_old, vc_new, dist)
        if dist > 0:
            g_new.add_edge(Edge(vp_new, vc_new))
        visitQueue(g_old, g_new, n + 1)
    return g_new


def BFS(file: str):
    with open(f'examples/{file}') as f1:
        g_old = load_graph(f1)
    g_new = Graph(False)
    global queue
    queue.append(("null", g_old.vertices[0], 0))
    g_new = visitQueue(g_old, g_new, 1)
    with open('../dot/bfs_output.dot', 'w') as f2:
        write_dot(g_new, f2)
    if isConnected(g_new):
        print(f'The graph in {file} is INDEED connected')
    else:
        print(f'The graph in {file} is NOT connected')


BFS("examplegraph.gr")


def sortEdges(g: "Graph"):
    return sorted(list(g.edges), key=lambda x: (x.tail.label, x.head.label))
