from nu.nugraph import *
from nu.nugraph_io import *

stack = []  # Vertex_parent_old, Vertex_parent_new, Vertex_child_old, distance from root to child
visited = {}  # Vertex_old, Vertex_new
start = None


def labelling(o: str, n: int, dist: int, g: "Graph") -> "Vertex":
    global start
    if start is None:
        start = Vertex(g, "start - d: 0", colortext="White", rgb="ff0fff")
        return start
    return Vertex(g, f'o: {o} - n: {n} - d: {dist}')


def stackChild(vp_old: "Vertex", vp_new: "Vertex", g: "Graph"):
    for c in vp_old.neighbours:
        if not isEdge(vp_new, c, g):
            stack.append((vp_old, vp_new, c, getDistance(vp_new.label) + 1))
            return
    if len(stack) > 2:
        stack.pop()


def isEdge(vp_new: "Vertex", vc_old: "Vertex", g: "Graph"):
    if isVisited(vc_old):
        global visited
        vc_new = visited[vc_old]
        for e in g.edges:
            if ((e.tail.label == vp_new.label and e.head.label == vc_new.label) or
                    (e.tail.label == vc_new.label and e.head.label == vp_new.label)):
                return True
    return False


def getDistance(v_new_label: str) -> int:
    v_new_label = v_new_label[v_new_label.rfind(":") + 2::]
    return int(v_new_label)


def isConnected(g: "Graph"):
    return (len(g.vertices) - 1) == len(g.edges)


def isVisited(v: "Vertex") -> bool:
    return v in visited.keys()


def getVisited(v: "Vertex") -> "Vertex":
    return visited.get(v)


def isFinished(v_new: "Vertex", v_old: "Vertex", g_old: "Graph", g_new: "Graph") -> bool:
    return v_new.degree == v_old.degree and len(g_old.edges) == len(g_new.edges)


def visitStack(g_old: "Graph", g_new: "Graph", n: int):
    global stack
    global start
    if not g_new.vertices or not isFinished(start, stack[1][1], g_old, g_new):
        q = stack[len(stack) - 1]
        vp_new = q[1]
        vc_old = q[2]
        dist = q[3]
        if isVisited(vc_old):
            vc_new = getVisited(vc_old)
            n -= 1
        else:
            vc_new = labelling(vc_old.label, n, dist, g_new)
            global visited
            visited[vc_old] = vc_new
        if vp_new != "null" and not isEdge(vp_new, vc_old, g_new):
            g_new.add_edge(Edge(vp_new, vc_new))
        stackChild(vc_old, vc_new, g_new)
        visitStack(g_old, g_new, n + 1)
    return g_new


def DFS(file: str):
    with open(f'examples/{file}') as f1:
        g_old = load_graph(f1)
    g_new = Graph(False)
    global stack
    stack.append(("null", "null", g_old.vertices[0], 0))
    g_new = visitStack(g_old, g_new, 0)
    with open('../dot/dfs_output.dot', 'w') as f2:
        write_dot(g_new, f2)
    if isConnected(g_new):
        print(f'The graph in {file} is INDEED connected')
    else:
        print(f'The graph in {file} is NOT connected')


DFS("examplegraph.gr")


def sortEdges(g: "Graph"):
    return sorted(list(g.edges), key=lambda x: (x.tail.label, x.head.label))
