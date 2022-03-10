from nu.prints import *

color_num = {}  # set([neighs], str_color)
color_neighs = {}  # {int, str_color}

colors = set()
count = 0


# def newColor() -> str:
#     global count
#     first = min(255, count % 255 * 2)
#     second = min(255, count % 255 * 1)
#     third = min(255, count)
#     count += 100
#     return hex(first)[-2::] + hex(second)[-2::] + hex(third)[-2::]


# def randColor() -> str:
#     global colors
#     first = np.random.randint(low=0, high=255 * 3)
#     second = np.random.randint(low=0, high=255 * 3)
#     third = np.random.randint(low=0, high=255 * 3)
#     x = hex(first)[-2::] + hex(second)[-2::] + hex(third)[-2::]
#     while x in colors:
#         first = np.random.randint(low=0, high=255 * 3)
#         second = np.random.randint(low=0, high=255 * 3)
#         third = np.random.randint(low=0, high=255 * 3)
#         x = hex(first)[-2::] + hex(second)[-2::] + hex(third)[-2::]
#     colors.add(x)
#     return x


def colorNeighs(g_1: "Graph", g_2: "Graph") -> "Graph":
    global color_num
    global color_neighs
    global count
    g = g_1 + g_2
    for v in g.vertices:
        neighs = len(v.neighbours)
        if neighs in color_neighs.keys():
            v.colornum = color_neighs.get(neighs)
        else:
            count += 1
            color_neighs[neighs] = count
            v.colornum = count
    color_neighs = {}
    return g


def tempor(g: "Graph"):
    t = {}
    for v in g.vertices:
        t[v] = tuple(sorted([n.colornum for n in v.neighbours]))
    return t


def colorIter(g: "Graph") -> Graph:
    global color_num
    global color_neighs
    global count
    changed = True
    while changed:
        temp = tempor(g)
        changed = False
        for v in g.vertices:
            neighs = temp.get(v)
            if color_num.get(neighs):
                v.colornum = color_num.get(neighs)
            elif v.colornum not in color_num.values():
                color_num[neighs] = v.colornum
            else:
                changed = True
                count += 1
                color_num[neighs] = count
                v.colornum = count
        color_num = {}
    count = 0
    #       dotGraph(g, "isomorph_f")
    return g


def isDiscrete(g: "Graph") -> bool:
    cols = set()
    for v in g.vertices:
        cols.add(v.colornum)
    return len(cols) == len(g.vertices)


def isIsomorphic(g_1: "Graph", g_2: "Graph", first: bool = False):
    g = colorIter(colorNeighs(g_1, g_2))
    g_1_cnum = tuple(sorted([v.colornum for v in g.find_vertices(g_1)]))
    g_2_cnum = tuple(sorted([v.colornum for v in g.find_vertices(g_2)]))
    if first:
        return g_1_cnum == g_2_cnum, isDiscrete(g_1)
    return g_1_cnum == g_2_cnum, False
