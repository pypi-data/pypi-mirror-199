import networkx as nx
import matplotlib.pyplot as plt

G = nx.read_graphml("AttMpls.graphml")

pos = {}

for node in G.nodes():
    longitude = G.nodes[node].get('Longitude')
    if longitude == None:
        longitude = 1
    latitude = G.nodes[node].get('Latitude')
    if latitude == None:
        latitude = 1
    pos[node]=[longitude,latitude]


nx.draw_networkx(G, pos, node_size=160, node_color='#1E90FF', font_size=20)

plt.show()
