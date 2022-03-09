import numpy as np

from prints import *

color_num = {}  # set([neighs], str_color)
color_neighs = {}  # {int, str_color}

colors = set()
count = 0


def newColor() -> str:
    global count
    first = min(255, count % 255 * 2)
    second = min(255, count % 255 * 1)
    third = min(255, count)
    count += 100
    return hex(first)[-2::] + hex(second)[-2::] + hex(third)[-2::]


def randColor() -> str:
    global colors
    first = np.random.randint(low=0, high=255 * 3)
    second = np.random.randint(low=0, high=255 * 3)
    third = np.random.randint(low=0, high=255 * 3)
    x = hex(first)[-2::] + hex(second)[-2::] + hex(third)[-2::]
    while x in colors:
        first = np.random.randint(low=0, high=255 * 3)
        second = np.random.randint(low=0, high=255 * 3)
        third = np.random.randint(low=0, high=255 * 3)
        x = hex(first)[-2::] + hex(second)[-2::] + hex(third)[-2::]
    colors.add(x)
    return x


def colorNeighs(g_1: "Graph", g_2: "Graph") -> "Graph":
    global color_num
    global color_neighs
    global count
    g = g_1 + g_2
    for v in g.vertices:
        neighs = len(v.neighbours)
        if neighs in color_neighs.keys():
            v.rgb = color_neighs.get(neighs)
        else:
            ncolor = randColor()
            color_neighs[neighs] = ncolor
            v.rgb = ncolor
    color_neighs = {}
    return g


def tempor(g: "Graph"):
    t = {}
    for v in g.vertices:
        t[v] = tuple(sorted([n.rgb for n in v.neighbours]))
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
                v.rgb = color_num.get(neighs)
            elif v.rgb not in color_num.values():
                color_num[neighs] = v.rgb
            else:
                changed = True
                ncolor = randColor()
                color_num[neighs] = ncolor
                v.rgb = ncolor
        color_num = {}
        dotGraph(g, "isomorph_f")
    return g


def isDiscrete(g: "Graph") -> bool:
    cols = set()
    verts = g.find_vertices(1)
    for v in verts:
        cols.add(v.rgb)
    return len(cols) == len(verts)


def isIsomorphic(g_1: "Graph", g_2: "Graph"):
    g = colorIter(colorNeighs(g_1, g_2))
    g_1_rgb = tuple(sorted([v.rgb for v in g.find_vertices(1)]))
    g_2_rgb = tuple(sorted([v.rgb for v in g.find_vertices(2)]))
    result = (g_1_rgb == g_2_rgb, isDiscrete(g))
    # if result:
    #     print('Graph 1 and 2 are INDEED isomorphic')
    # else:
    #     print('Graph 1 and 2 are NOT isomorphic')
    return result
