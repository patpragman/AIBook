from collections import defaultdict

class Node:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def is_same_as(self, other):
        return self.name == other.name

    def __eq__(self, other):
        return self.is_same_as(other)



class Edge:

    def __init__(self, node_a, node_b, weight=0):
        self.node_a = node_a
        self.node_b = node_b
        self.weight = weight

    def __str__(self):
        return f"{self.node_a} -> {self.node_b} {self.weight}"

    def __contains__(self, item):
        return item in [self.node_a, self.node_b]


class UGraph:

    def __init__(self):
        self.edges = {}

    def add_node(self, *nodes):
        for node in nodes:
            self.edges[node] = []

    def remove_node(self, node):
        del self.nodes[node]

    def add_edge(self, node_a, node_b, weight=0, bidirectional=True):

        self.edges[node_a].append((node_b, weight))
        if bidirectional:
            self.edges[node_b].append((node_a, weight))

    def remove_edge(self, node_a, node_b, biderectional=True):

        remove_indices = []
        for i in range(0, len(self.edges[node_a])):
            node, weight = self.edges[node_a][i]
            if node.is_same_as(node_b):
                remove_indices.append(i)

        for i in remove_indices:
            self.edges[node_a].pop(i)

        if biderectional:
            self.remove_edge(node_b, node_a, biderectional=False)

    def has_edge(self, node_a, node_b):
        return node_a in self.edges[node_b] or node_b in self.edges[node_a]

    def neighbors(self, node):
        return set(self.edges[node])

    def find_path(self, node_a):
        pass

    def __str__(self):
        output = []
        for node_a in self.edges:
            edges = self.edges[node_a]
            for node_b, weight in edges:
                output.append(f"{node_a} -> {node_b} {weight}")
        return "\n".join(str(edge) for edge in output)

    def clone(self):
        g = UGraph()
        g.edges = {key: g.edges[key].copy() for key in g.edges}  # copy the dictionary with all the info

        return g


def find_path(graph: UGraph, a: Node, b: Node, been_to=[]) -> list:
    """
    takes a graph object and two nodes, returns the first path it finds as a list of tuples with
    weights, returns an empty tuple if nothing found
    """
    subgraph = graph.clone()

    edges = subgraph.edges[a]
    for edge in edges:
        node, weight = edge
        been_to.append(node)
        if node.is_same_as(b):
            return been_to  # base case
        elif been_to.count(node) > 1:
            return None  # if it's a cycle break off the recursion
        else:
            # go ahead and remove that edge from consideration
            subgraph.remove_edge(a, node)
            return find_path(subgraph, node, b, been_to)


def find_all_paths(graph: UGraph, a: Node, b: Node) -> list[list]:

    paths = []
    g = graph.clone()
    print(graph.edges)
    print(g.edges)
    edges = g.edges[a]
    for edge in edges:
        node, weight = edge
        paths.append(find_path(g, a, b))
        g.remove_edge(g, a, node)
        a = node

    return paths






if __name__ == "__main__":
    arad = Node("arad")
    sibbiu = Node("sibbiu")
    oradea = Node("oradea")
    zerind = Node("zerind")
    timisoara = Node("timisoara")

    g = UGraph()
    g.add_node(arad, sibbiu, oradea, zerind, timisoara)
    g.add_edge(arad, sibbiu, 140)
    g.add_edge(sibbiu, oradea, 151)
    g.add_edge(oradea, zerind, 71)
    g.add_edge(zerind, arad, 75)
    g.add_edge(arad, timisoara, 118)

    path = find_path(g, timisoara, oradea)
    paths = find_all_paths(g, timisoara, oradea)
    for node in path:
        print(node)

    for path in paths:
        for node in paths:
            print(node)