import networkx as nx
from src.Oublie.huatu import draw_nx

G = nx.read_graphml("condensed_west_europe_delete.graphml")

nolongitude,nolaitude =draw_nx(G,10,40,dlon=2,dlat=50)
print("nolongitude",nolongitude)
print("nolaitude",nolaitude)