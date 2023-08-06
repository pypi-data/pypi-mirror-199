import networkx as nx
import json
from networkx.readwrite import json_graph

with open("directed.json", "w") as file:
    G = nx.generators.directed.gn_graph(10)
    data = json_graph.node_link_data(G)
    json.dump(data, file)
