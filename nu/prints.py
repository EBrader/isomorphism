from nu.nugraph_io import *


def dotGraph(g: "Graph", filename="print"):
    with open(f'dot/{filename}.dot', 'w') as f:
        write_dot(g, f)


def getGraphGr(filename="examplegraph"):
    with open(f'examples/{filename}.gr') as f:
        return load_graph(f)


def getGraphGrl(filename="colorref_smallexample_6_15"):
    with open(f'examples/{filename}.grl') as f:
        return load_graph(f)


def getGraphGrls(filename="colorref_smallexample_6_15"):
    with open(f'examples/{filename}.grl') as f:
        return load_graph(f, read_list=True)[0]
