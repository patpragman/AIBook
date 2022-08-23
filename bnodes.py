import itertools

class Node:

    def __init__(self, name):
        self.name = name
        self.visited = False

    def __eq__(self, other):
        if isinstance(other, Node):
            return self._key() == other._key()
        else:
            return NotImplemented

    def _key(self):
        return (self.name, )

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self._key())

class Edge:

    def __init__(self, a, b, weight):
        self.point_a = a
        self.point_b = b
        self.weight = weight
        self.traveled_on = False

    def __eq__(self, other):

        return (self.point_a == other.point_a) \
            and (self.point_b == other.point_b) \
            and (self.weight == other.weight)

    def __ne__(self, other):
        return (self.point_a != other.point_a) \
               or (self.point_b != other.point_b) \
               or (self.weight != other.weight)

    def __str__(self):
        return f"{self.point_a} -> {self.point_b} {self.weight}"

    def __contains__(self, item):
        return item.name in [self.point_a.name, self.point_b.name]


class Graph:

    def __init__(self, *nodes):
        self.edges = {node: [] for node in nodes}

    def add_node(self, *nodes):
        for node in nodes:
            self.edges[node] = []

    def remove_node(self, node):
        del self.nodes[node]

    def add_edge(self, node_a, node_b, weight=0, bidirectional=True):
        edge_there = Edge(node_a, node_b, weight)
        self.edges[node_a].append(edge_there)
        if bidirectional:
            edge_back = Edge(node_b, node_a, weight)
            self.edges[node_b].append(edge_back)

    def get_edge(self, node_a, node_b):
        return [edge for edge in self.edges[node_a] if edge.point_b == node_b]

    def remove_edge(self, node_a, node_b, biderectional=True):

        remove_indices = []
        for i, edge in enumerate(self.edges[node_a]):
            node = edge.point_b
            if node == node_b:
                remove_indices.append(i)

        for i in remove_indices:
            self.edges[node_a].pop(i)

        if biderectional:
            self.remove_edge(node_b, node_a, biderectional=False)

    def has_edge(self, node_a, node_b):
        return node_a in self.edges[node_b] or node_b in self.edges[node_a]

    def neighbors(self, node):
        return self.edges[node]

    def find_paths(self, node_a, target_node, all_paths=[], visited=[]):
        visited.append(node_a)
        edges = self.neighbors(node_a)

        if node_a is target_node:
            all_paths.append(visited)
        else:
            # loop through the edges and make a copy of the graph omitting the other edges
            for target_edge in edges:
                g = self.clone()
                deletable_edges = [edge for edge in edges if edge == target_edge]

                for d in deletable_edges:
                    a = d.point_a
                    b = d.point_b
                    g.remove_edge(a, b)

                g.find_paths(target_edge.point_b, target_node, all_paths, visited.copy())

    def find_all_paths_by_edge(self, node_a, target_node):
        node_path_lists = []
        self.find_paths(node_a, target_node, node_path_lists)


        path_holder = []
        for node_path_list in node_path_lists:
            editable_node_list = node_path_list.copy()
            edges = []
            while len(editable_node_list) > 1:
                point_a = editable_node_list.pop(0)
                point_b = editable_node_list[0]
                edge = [edge for edge in self.edges[point_a] if edge.point_a == point_a and edge.point_b == point_b]
                edges.append(edge)

            path_holder.append(edges)

        return path_holder


    def __str__(self):
        output = []
        for node_a in self.edges:
            edges = self.edges[node_a]
            for edge in edges:
                node_b, weight = edge.point_b, edge.weight
                output.append(f"{node_a} -> {node_b} {weight}")
        return "\n".join(str(edge) for edge in output)

    def clone(self):
        g = Graph()
        g.edges = {key: self.edges[key].copy() for key in self.edges}  # copy the dictionary with all the info
        return g


def get_shortest_paths(graph: Graph, starting_node, target_node) -> tuple:
    all_paths = graph.find_all_paths_by_edge(starting_node, target_node).copy()
    shortest_distance = 100_000  # way bigger than anything else...
    path_number = 0
    for i, path in enumerate(all_paths):
        unbounded_path = list(itertools.chain(*path))
        cost = sum([edge.weight for edge in unbounded_path])
        if cost < shortest_distance:
            shortest_distance = cost
            path_number = i

    return all_paths[path_number], shortest_distance

if __name__ == "__main__":
    arad = Node("arad")
    sibbiu = Node("sibbiu")
    oradea = Node("oradea")
    zerind = Node("zerind")
    timisoara = Node("timisoara")
    lugoy = Node('lugoy')
    mehadia = Node('Mehadia')
    Drobeta = Node('drobeta')
    craiova = Node('Craiova')
    rimnicu_vilcea = Node("Rimnicu Vilcea")


    g = Graph()
    g.add_node(arad, sibbiu, oradea, zerind, timisoara, lugoy, mehadia, Drobeta, craiova, rimnicu_vilcea)
    g.add_edge(arad, sibbiu, 140)
    g.add_edge(sibbiu, oradea, 151)
    g.add_edge(oradea, zerind, 71)
    g.add_edge(zerind, arad, 75)
    g.add_edge(arad, timisoara, 118)
    g.add_edge(timisoara, lugoy, 111)
    g.add_edge(lugoy, mehadia, 70)
    g.add_edge(mehadia, Drobeta, 75)
    g.add_edge(Drobeta, craiova, 120)
    g.add_edge(craiova, rimnicu_vilcea, 146)
    g.add_edge(rimnicu_vilcea, sibbiu, 80)


    container = g.find_all_paths_by_edge(craiova, oradea)
    fastest_path, shortest_distance = get_shortest_paths(g.clone(), craiova, oradea)

    for path in container:
        print("PATH:>>>")
        for edge in path:
            print(*[str(e) for e in edge])

    print("Fastest PATH:>>>")
    for edge in fastest_path:
        print(*edge)
    print(shortest_distance)