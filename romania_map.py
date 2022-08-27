import pandas as pd
from graph import Vertex
from graph import Graph

df = pd.read_csv("romania.csv")
vertices = {}

for city in df.columns[1:]:
    v = Vertex(city)
    vertices[city] = v

romania = Graph()
for vertex in vertices.values():
    romania.add_node(vertex)

# pprint(vertices)
for id, row in df.iterrows():
    city = row['city_name']
    for other_city in vertices:
        weight = row[other_city]

        if weight > 0:
            node_a = vertices[city]
            node_b = vertices[other_city]
            romania.add_edge(node_a, node_b, weight, bidirectional=False)
