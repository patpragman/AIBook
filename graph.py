from copy import deepcopy
from geopy.distance import geodesic

class Vertex:

    def __init__(self, name="V", data={}, latitude=None, longitude=None):
        self.name = name
        self.data = data
        self.latitude = latitude
        self.longitude = longitude


    def __eq__(self, other):
        if isinstance(other, Vertex):
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

    def __init__(self,
                 starting_vertex: Vertex,
                 ending_vertex: Vertex,
                 weight: float):

        self.starting_vertex = starting_vertex
        self.ending_vertex = ending_vertex
        self.weight = weight

    def __eq__(self, other):
        return (self.starting_vertex == other.starting_vertex) \
            and (self.ending_vertex == other.ending_vertex) \
            and (self.weight == other.weight)

    def __ne__(self, other):
        return (self.starting_vertex != other.starting_vertex) \
               or (self.ending_vertex != other.ending_vertex) \
               or (self.weight != other.weight)

    def __str__(self):
        return f"{self.starting_vertex} -> {self.ending_vertex} (weight:{self.weight})"

    def __contains__(self, item):
        return item.name in [self.starting_vertex.name, self.ending_vertex.name]


class Graph:

    def __init__(self, vertices: list[Vertex] = []):
        self.vertices = {}
        self.add_node(*vertices)

    def add_node(self, *nodes):
        for node in nodes:
            self.vertices[node] = []

    def remove_node(self, node):
        del self.vertices[node]

    def add_edge(self,vertex_a: Vertex, vertex_b: Vertex, weight=0, bidirectional=True):
        # we don't want there to be more than one edge with the same vertex in this graph
        if self.get_edge(vertex_a, vertex_b):
            raise Exception("Edge already exists!")


        edge_there = Edge(vertex_a, vertex_b, weight)
        self.vertices[vertex_a].append(edge_there)

        if bidirectional:
            self.add_edge(vertex_b, vertex_a, weight, bidirectional=False)

    def remove_edges(self, node_a, node_b, biderectional=True):
        """
        remove all edges between two nodes

        iterate through the vertices, get the indices of those vertices, then pop those off the appropriate
        edge list

        if you're bidirectional do that again in the other direction
        """
        remove_indices = []
        for i, edge in enumerate(self.vertices[node_a]):
            node = edge.ending_vertex
            if node == node_b:
                remove_indices.append(i)

        for i in remove_indices:
            self.vertices[node_a].pop(i)

        if biderectional:
            self.remove_edges(node_b, node_a, biderectional=False)

    def get_edges(self, vertex: Vertex) -> list[Edge]:
        """
        takes a vertex, returns the list of edges associated with that vertex

        be careful... lists are mutable
        """
        return self.vertices[vertex]

    def get_edge(self, vertex_a: Vertex, vertex_b: Vertex):
        """
        takes two specific vertices and returns the edge between them, returns None otherwise
        """
        edges_returned = [edge for edge in self.vertices[vertex_a] if edge.ending_vertex == vertex_b]
        if edges_returned:
            # there should only be one thing in this list...
            return edges_returned[0]
        else:
            return None

class TraversalBotExection(Exception):

    def __init__(self, what):
        super().__init__(f"Traversal Bot Exception! {what}")

class TraversalBot:

    def __init__(self, graph: Graph, starting_vertex: Vertex):
        self.graph = graph
        self.current_vertex = starting_vertex
        self.available_edges = self.graph.get_edges(self.current_vertex)
        self.continue_looking = True
        self.edge_history = []

    def teleport(self, vertex: Vertex):
        self.current_vertex = vertex
        self.available_edges = self.graph.get_edges(self.current_vertex)

    def move_along(self, edge: Edge):
        if edge not in self.available_edges:
            # if you can't move along that edge, raise an exception
            raise TraversalBotExection("Edge isn't available!")
        else:
            # otherwise, reposition
            self.current_vertex = edge.ending_vertex
            self.available_edges = self.graph.get_edges(edge.ending_vertex)

    def brute_force_shortest_path(self, goal: Vertex):
        path_table = {sum([edge.weight for edge in path]):path for path in self.get_all_paths(goal)}
        return path_table[min(path_table)]



    def heuristic(self, edge, goal_vertex):
        """
        straight line distance from the end of the edge to the goal
        """
        point_b = edge.ending_vertex.latitude, edge.ending_vertex.longitude
        return geodesic(point_b, goal_vertex).km

    def a_star(self, goal: Vertex):
        pass


    def breadth_first(self, goal: Vertex, collector=[], visited_edges=[]):


        searching = True
        layers = []
        while searching:


            sublist = []
            nodes = []
            for edge in self.available_edges:
                starting_vertex = edge.starting_vertex
                ending_vertex = edge.ending_vertex
                nodes.append(ending_vertex)

                visited_edges.append(edge)
                visited_edges.append(self.graph.get_edges(ending_vertex, starting_vertex))
                sublist.append(edge)

                if edge in visited_edges:
                    continue

                if ending_vertex == goal:
                    searching = False
                    break

            # make our available edges populated by the nodes we just visited
            self.available_edges = []
            for node in nodes:
                self.available_edges.extend(self.graph.get_edges(node))

            # now push the new layer onto the layer list
            layers.append(sublist)


        """
        now we're out of the layer construction, so reverse the layer list
        """
        layers.reverse()
        final_edge_list = []

        target_vertex = goal
        while layers:
            layer = layers.pop()
            while layer:
                edge = layer.pop()
                if edge.ending_vertex == target_vertex:
                    target_vertex = edge.starting_vertex
                    final_edge_list.append(edge)

        return final_edge_list.reverse()

    def get_all_paths(self, goal: Vertex):
        collector = []
        self._get_all_paths(goal, collector=collector)

        # reset the bot!
        self.edge_history = []
        self.continue_looking = True
        self.available_edges = self.graph.get_edges(self.current_vertex)
        return collector

    def _get_all_paths(self, goal: Vertex, collector=[],
                       current_path_history=[],
                       visited=[],
                       ):

        # very similar to getting _find_any_path
        if self.current_vertex == goal:
            collector.append(current_path_history)
        else:
            for edge in self.available_edges:
                current_vertex = self.current_vertex

                if edge in visited:
                    # don't need to go down paths we've already gone down
                    continue

                self.move_along(edge)

                # record the edges you're going along, and which edges you've traveled on
                current_path_history.append(edge)
                visited.append(edge)
                visited.append(self.graph.get_edge(edge.ending_vertex, edge.starting_vertex))

                # recursively execute the same find any path
                self._get_all_paths(goal,
                                    collector=collector,
                                    current_path_history=deepcopy(current_path_history),
                                    visited=deepcopy(visited))

                # we should pop off the current visited and path history lists
                current_path_history.pop()
                visited.pop()
                visited.pop()
                # now we need to reposition the bot to the vertex we were at!
                self.teleport(current_vertex)


    def find_any_path(self, goal: Vertex):
        # helper method that runs _find_any_path then returns the results
        self._find_any_path(goal)
        any_path = deepcopy(self.edge_history)
        self.edge_history = []
        self.continue_looking = True
        self.available_edges = self.graph.get_edges(self.current_vertex)
        return any_path

    def _find_any_path(self, goal: Vertex, current_path_history=[], visited=[]):
        # this method returns the first path it finds
        if self.current_vertex == goal:
            self.continue_looking = False
            self.edge_history = current_path_history


        edge_index = 0
        while self.continue_looking:
            edge = self.available_edges[edge_index]
            edge_index += 1
            if edge in visited:
                continue

            if not self.continue_looking:
                break

            self.move_along(edge)  # move along the edge

            current_path_history.append(edge)  # add the pathway to the current path history
            # add the edge you went over, and it's reciprocal to the visited list
            visited.append(edge)
            visited.append(self.graph.get_edge(edge.ending_vertex, edge.starting_vertex))

            # recursively execute the same find any path
            self._find_any_path(goal, current_path_history=current_path_history, visited=deepcopy(visited))

