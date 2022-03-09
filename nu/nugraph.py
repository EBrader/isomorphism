"""
This is a module for working with directed and undirected multigraphs.
"""
# version: 29-01-2015, Paul Bonsma
# version: 01-02-2017, Pieter Bos, Tariq Bontekoe
from typing import List, Union, Set


class GraphError(Exception):
    """
    An error that occurs while manipulating a `Graph`
    """

    def __init__(self, message: str):
        """
        Constructor
        :param message: The error message
        :type message: str
        """
        super(GraphError, self).__init__(message)


class Vertex(object):
    """
    `Vertex` objects have a property `graph` pointing to the graph they are part of,
    and an attribute `label` which can be anything: it is not used for any methods,
    except for `__str__`.
    """

    def __init__(self, graph: "Graph", label=None, num: int = 0, rgb: str = None):
        """
        Creates a vertex, part of `graph`, with optional label `label`.
        (Labels of different vertices may be chosen the same; this does
        not influence correctness of the methods, but will make the string
        representation of the graph ambiguous.)
        :param graph: The graph that this `Vertex` is a part of
        :param label: Optional parameter to specify a label for the
        """
        if label is None:
            label = graph._next_label()

        self._graph = graph
        self.label = label
        self._num = num
        self._rgb = rgb
        self._incidence = {}

    def __repr__(self):
        """
        A programmer-friendly representation of the vertex.
        :return: The string to approximate the constructor arguments of the `Vertex'
        """
        return 'Vertex(label={}, colortext={}, #incident={})'.format(self.label, self.colortext, len(self._incidence))

    def __str__(self) -> str:
        """
        A user-friendly representation of the vertex, that is, its label.
        :return: The string representation of the label.
        """
        return str(self.label)

    def is_adjacent(self, other: "Vertex") -> bool:
        """
        Returns True iff `self` is adjacent to `other` vertex.
        :param other: The other vertex
        """
        return other in self._incidence

    def _add_incidence(self, edge: "Edge"):
        """
        For internal use only; adds an edge to the incidence map
        :param edge: The edge that is used to add the incidence
        """
        other = edge.other_end(self)

        if other not in self._incidence:
            self._incidence[other] = set()

        self._incidence[other].add(edge)

    @property
    def rgb(self) -> str:
        return self._rgb

    @rgb.setter
    def rgb(self, rgb: str):
        self._rgb = rgb

    @property
    def num(self):
        return self._num

    @property
    def graph(self) -> "Graph":
        """
        The graph of this vertex
        :return: The graph of this vertex
        """
        return self._graph

    @property
    def incidence(self) -> List["Edge"]:
        """
        Returns the list of edges incident with the vertex.
        :return: The list of edges incident with the vertex
        """
        result = set()

        for edge_set in self._incidence.values():
            result |= edge_set

        return list(result)

    @property
    def neighbours(self) -> List["Vertex"]:
        """
        Returns the list of neighbors of the vertex.
        """
        return list(self._incidence.keys())

    @property
    def degree(self) -> int:
        """
        Returns the degree of the vertex
        """
        return sum(map(len, self._incidence.values()))


class Edge(object):
    """
    Edges have properties `tail` and `head` which point to the end vertices
    (`Vertex` objects). The order of these matters when the graph is directed.
    """

    def __init__(self, tail: Vertex, head: Vertex, weight=None):
        """
        Creates an edge between vertices `tail` and `head`
        :param tail: In case the graph is directed, this is the tail of the arrow.
        :param head: In case the graph is directed, this is the head of the arrow.
        :param weight: Optional weight of the vertex, which can be any type, but usually is a number.
        """
        if tail.graph != head.graph:
            raise GraphError("Can only add edges between vertices of the same graph")

        self._tail = tail
        self._head = head
        self._weight = weight

    def __repr__(self):
        """
        A programmer-friendly representation of the edge.
        :return: The string to approximate the constructor arguments of the `Edge'
        """
        return 'Edge(head={}, tail={}, weight={})'.format(self.head.label, self.tail.label, self.weight)

    def __str__(self) -> str:
        """
        A user friendly representation of this edge
        :return: A user friendly representation of this edge
        """
        return '({}, {})'.format(str(self.tail), str(self.head))

    @property
    def tail(self) -> "Vertex":
        """
        In case the graph is directed, this represents the tail of the arrow.
        :return: The tail of this edge
        """
        return self._tail

    @property
    def head(self) -> "Vertex":
        """
        In case the graph is directed, this represents the head of the arrow.
        :return: The head of this edge
        """
        return self._head

    @property
    def weight(self):
        """
        The weight of this edge, which can also just be used as a generic label.
        :return: The weight of this edge
        """
        return self._weight

    def other_end(self, vertex: "Vertex") -> "Vertex":
        """
        Given one end `vertex` of the edge, this returns
        the other end vertex.
        :param vertex: One end
        :return: The other end
        """
        if self.tail == vertex:
            return self.head
        elif self.head == vertex:
            return self.tail

        raise GraphError(
            'edge.other_end(vertex): vertex must be head or tail of edge')

    def incident(self, vertex: Vertex) -> bool:
        """
        Returns True iff the edge is incident with the
        vertex.
        :param vertex: The vertex
        :return: Whether the vertex is incident with the edge.
        """
        return self.head == vertex or self.tail == vertex


def fillDict(d: dict, head: str, tail: str):
    if head not in d:
        d[head] = [tail]
    else:
        d[head].append(tail)


def createDict(source: "Graph") -> dict:
    d = dict()
    edges = source.edges
    while edges:
        edge = edges.pop(0)
        fillDict(d, edge.head.label, edge.tail.label)
        fillDict(d, edge.tail.label, edge.head.label)
    return d


def createCDict(g: "Graph"):
    dd = createDict(g)
    ls = toLabels(g)
    cd = dict()
    for i in ls:
        if i not in dd.keys():
            cd[i] = toLabels(g, i)
        else:
            cd[i] = []
            vl = dd[i]
            for ll in ls:
                if ll != i and ll not in vl:
                    cd[i].append(ll)
    return cd


def findVert(name: str, num: int, new: "Graph") -> "Vertex":
    for i in new.vertices:
        if name == i.label and num == i.num:
            return i
    return Vertex(new, label=name, num=num)


def isEdge(hl: str, tl: str, num: int, g: "Graph"):
    for e in g.edges:
        ehl = e.head.label
        etl = e.tail.label
        if (ehl == hl and etl == tl) or (etl == hl and ehl == tl) and e.head.num == num:
            return True
    return False


def handleGraph(new: "Graph", d: dict, num: int) -> "Graph":
    for k in d.keys():
        for v in d[k]:
            if not isEdge(k, v, num, new):
                new.add_edge(Edge(findVert(k, num, new), findVert(v, num, new)))
    return new


def toLabels(g: "Graph", ex: str = "null"):
    vls = []
    for v in g.vertices:
        if ex != v.label:
            vls.append(v.label)
    return vls


def find_neighs(v: "Vertex", v_old: List[Vertex]):
    neighs = [v_old.neighbours for v_old in v_old if v_old.label is v.label and v_old.num == v.num][0]
    return tuple(sorted([n.rgb for n in neighs]))


class Graph(object):
    def __init__(self, directed: bool, num: int = 0, n: int = 0, simple: bool = False):
        """
        Creates a graph.
        :param directed: Whether the graph should behave as a directed graph.
        :param simple: Whether the graph should be a simple graph, that is, not have multi-edges or loops.
        :param n: Optional, the number of vertices the graph should create immediately
        """
        self._num = num
        self._v = list()
        self._e = list()
        self._simple = simple
        self._directed = directed
        self._next_label_value = 0

        for i in range(n):
            self.add_vertex(Vertex(self))

    def __repr__(self):
        """
        A programmer-friendly representation of the Graph.
        :return: The string to approximate the constructor arguments of the `Graph'
        """
        return f'Graph #{self._num}'

    def __str__(self) -> str:
        """
        A user-friendly representation of this graph
        :return: A textual representation of the vertices and edges of this graph
        """
        return 'V=[' + ", ".join(map(str, self._v)) + ']\nE=[' + ", ".join(map(str, self._e)) + ']'

    def _next_label(self) -> int:
        """
        Generates unique labels for vertices within the graph
        :return: A unique label
        """
        result = self._next_label_value
        self._next_label_value += 1
        return result

    @property
    def num(self):
        return self._num

    @num.setter
    def num(self, num: int = 0):
        self._num = num

    @property
    def simple(self) -> bool:
        """
        Whether the graph is a simple graph, that is, it does not have multi-edges or loops.
        :return: Whether the graph is simple
        """
        return self._simple

    @property
    def directed(self) -> bool:
        """
        Whether the graph behaves as a directed graph
        :return: Whether the graph is directed
        """
        return self._directed

    @property
    def vertices(self) -> List["Vertex"]:
        """
        :return: The `set` of vertices of the graph
        """
        return list(self._v)

    @property
    def edges(self) -> List["Edge"]:
        """
        :return: The `set` of edges of the graph
        """
        return list(self._e)

    def __iter__(self):
        """
        :return: Returns an iterator for the vertices of the graph
        """
        return iter(self._v)

    def __len__(self) -> int:
        """
        :return: The number of vertices of the graph
        """
        return len(self._v)

    def add_vertex(self, vertex: "Vertex"):
        """
        Add a vertex to the graph.
        :param vertex: The vertex to be added.
        """
        if vertex.graph != self:
            raise GraphError("A vertex must belong to the graph it is added to")

        self._v.append(vertex)

    def add_edge(self, edge: "Edge"):
        """
        Add an edge to the graph. And if necessary also the vertices.
        Includes some checks in case the graph should stay simple.
        :param edge: The edge to be added
        """

        if self._simple:
            if edge.tail == edge.head:
                raise GraphError('No loops allowed in simple graphs')

            if self.is_adjacent(edge.tail, edge.head):
                raise GraphError('No multiedges allowed in simple graphs')

        if edge.tail not in self._v:
            self.add_vertex(edge.tail)
        if edge.head not in self._v:
            self.add_vertex(edge.head)

        self._e.append(edge)

        edge.head._add_incidence(edge)
        edge.tail._add_incidence(edge)

    def __add__(self, other: "Graph") -> "Graph":
        """
        Make a disjoint union of two graphs.
        :param other: Graph to add to `self'.
        :return: New graph which is a disjoint union of `self' and `other'.
        """
        G = Graph(False)
        handleGraph(G, createDict(self), 1)
        handleGraph(G, createDict(other), 2)

        return G

    def __iadd__(self, other: Union[Edge, Vertex]) -> "Graph":
        """
        Add either an `Edge` or `Vertex` with the += syntax.
        :param other: The object to be added
        :return: The modified graph
        """
        if isinstance(other, Vertex):
            self.add_vertex(other)

        if isinstance(other, Edge):
            self.add_edge(other)

        return self

    def del_edge(self, edge: "Edge"):
        u = edge.head
        v = edge.tail
        result = u._incidence.get(v, set())
        if result:
            try:
                u._incidence.pop(v)
                self._e.remove(result.pop())
            except ValueError:
                pass

    def del_vertex(self, v: "NUVertex"):
        for n in v.neighbours:
            for e in self.find_edge(v, n):
                self.del_edge(e)
        self._v.remove(v)

    def find_vertices(self, num: int = 0, rgb: str = None) -> List["Vertex"]:
        if int == 0 and rgb is None:
            return self._v
        elif int == 0:
            return [v for v in self._v if v.rgb is rgb]
        elif rgb is None:
            return [v for v in self._v if v.num == num]
        else:
            return [v for v in self._v if v.num == num and v.rgb is rgb]

    def find_edge(self, u: "Vertex", v: "Vertex") -> Set["Edge"]:
        """
        Tries to find edges between two vertices.
        :param u: One vertex
        :param v: The other vertex
        :return: The set of edges incident with both `u` and `v`
        """
        result = u._incidence.get(v, set())

        if not self._directed:
            result |= v._incidence.get(u, set())

        return set(result)

    def is_adjacent(self, u: "Vertex", v: "Vertex") -> bool:
        """
        Returns True iff vertices `u` and `v` are adjacent. If the graph is directed, the direction of the edges is
        respected.
        :param u: One vertex
        :param v: The other vertex
        :return: Whether the vertices are adjacent
        """
        return v in u.neighbours and (not self.directed or any(e.head == v for e in u.incidence))


class UnsafeGraph(Graph):
    @property
    def vertices(self) -> List["Vertex"]:
        return self._v

    @property
    def edges(self) -> List["Edge"]:
        return self._e

    def add_vertex(self, vertex: "Vertex"):
        self._v.append(vertex)

    def add_edge(self, edge: "Edge"):
        self._e.append(edge)

        edge.head._add_incidence(edge)
        edge.tail._add_incidence(edge)

    def find_edge(self, u: "Vertex", v: "Vertex") -> Set["Edge"]:
        left = u._incidence.get(v, None)
        right = None

        if not self._directed:
            right = v._incidence.get(u, None)

        if left is None and right is None:
            return set()

        if left is None:
            return right

        if right is None:
            return left

        return left | right

    def is_adjacent(self, u: "Vertex", v: "Vertex") -> bool:
        return v in u._incidence or (not self._directed and u in v._incidence)
