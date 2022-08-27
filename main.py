from graph import Graph, Vertex, TraversalBot
from romania_map import romania, vertices

if __name__ == "__main__":

    timisoara = vertices["Timisoara"]
    bucharest = vertices['Bucharest']

    bot1 = TraversalBot(graph=romania, starting_vertex=timisoara)
    bot2 = TraversalBot(graph=romania, starting_vertex=timisoara)

    paths = bot1.get_all_paths(bucharest)

    for path in paths:
        weight = 0
        for edge in path:
            weight += edge.weight
            print(edge)
        print("total: ", weight)

    shortest_path = bot2.brute_force_shortest_path(bucharest)
    weight = 0
    for edge in shortest_path:
        weight += edge.weight
        print(edge)

    print("total:", weight)