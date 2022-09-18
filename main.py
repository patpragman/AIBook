from graph import Graph, Vertex, TraversalBot
from romania_map import romania, vertices
from datetime import datetime, timedelta

if __name__ == "__main__":

    timisoara = vertices["Timisoara"]
    bucharest = vertices['Bucharest']
    arad = vertices['Arad']

    bot1 = TraversalBot(graph=romania, starting_vertex=timisoara)
    bot2 = TraversalBot(graph=romania, starting_vertex=timisoara)
    bot3 = TraversalBot(graph=romania, starting_vertex=timisoara)
    bot4 = TraversalBot(graph=romania, starting_vertex=timisoara)
    bot5 = TraversalBot(graph=romania, starting_vertex=timisoara)

    print('All possible paths:')
    start = datetime.utcnow()
    paths = bot1.get_all_paths(bucharest)
    stop = datetime.utcnow()
    time_to_get_all_paths = stop - start
    for path in paths:
        weight = 0
        for edge in path:
            weight += edge.weight
            print(edge)
        print("total: ", weight)
        print("---------------------")
    print(f"{time_to_get_all_paths.microseconds} microseconds to get all the paths")
    print(4*"\n")

    print('Brute force ')
    start = datetime.utcnow()
    shortest_path = bot2.brute_force_shortest_path(bucharest)
    stop = datetime.utcnow()
    brute_force_time = stop - start
    weight = 0
    for edge in shortest_path:
        weight += edge.weight
        print(edge)
    print("total:", weight)
    print(f"{brute_force_time.microseconds} microseconds to brute force the quickest path")
    print(4*"\n")

    print("Breadth first search!")
    start = datetime.utcnow()
    bfs = bot3.brute_force_shortest_path(bucharest)
    stop = datetime.utcnow()
    bfs_time = stop - start
    weight = 0
    for edge in bfs:
        weight += edge.weight
        print(edge)
    print("total:", weight)
    print(f"{bfs_time.microseconds} microseconds to get the quickest path with breadth first search")
    print(4*"\n")


    print("A*")
    start = datetime.utcnow()
    a_star = bot4.a_star(bucharest)
    stop = datetime.utcnow()
    astar_time = stop - start
    weight = 0
    for edge in a_star:
        weight += edge.weight
        print(edge)
    print("total:", weight)
    print(f"{astar_time.microseconds} microseconds to get the quickest path with A*")
    print(4*"\n")

    print("Greedy Best First")
    start = datetime.utcnow()
    greedy_bfs = bot4.greedy_bfs(bucharest)
    stop = datetime.utcnow()
    greedy_bfs_time = stop - start
    weight = 0
    for edge in a_star:
        weight += edge.weight
        print(edge)
    print("total:", weight)
    print(f"{greedy_bfs_time.microseconds} microseconds to get the quickest path with Greedy BFS")
    print(4*"\n")



