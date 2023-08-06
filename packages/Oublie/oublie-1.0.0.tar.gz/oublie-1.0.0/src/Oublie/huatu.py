import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap as Basemap


def draw_nx(G, llon=10, llat=40, ulon=30, ulat=55, dlon=1, dlat=1, ns=10, nc='red', fs=10):
    m = Basemap(
        projection='merc',
        llcrnrlon=-llon,
        llcrnrlat=llat,
        urcrnrlon=ulon,
        urcrnrlat=ulat,
        lat_ts=0,
        resolution='i',
        suppress_ticks=True)

    lats = []
    lons = []
    nolongitude = []
    nolatitude = []

    for node in G.nodes():
        longitude = G.nodes[node].get('Longitude')

        if longitude == None:
            nolongitude.append(node)
            longitude = dlon
        latitude = G.nodes[node].get('Latitude')
        if latitude == None:
            nolatitude.append(node)
            latitude = dlat
        lats.append(latitude)
        lons.append(longitude)

    mx, my = m(lons, lats)

    pos = {}
    i = 0

    for node in G.nodes():
        pos[node] = [mx[i], my[i]]
        i += 1

    nx.draw_networkx(G, pos, node_size=ns, node_color=nc, font_size=fs)

    m.drawcountries()
    m.drawstates()
    m.bluemarble()

    plt.show()

    return nolongitude,nolatitude
