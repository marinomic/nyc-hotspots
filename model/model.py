import copy
import random

import networkx as nx
from database.DAO import DAO
from geopy.distance import distance


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._nodes = []

    def creaGrafo(self, provider, soglia):
        self._nodes = DAO.getAllObjLocationForProvider(provider)
        self._grafo.add_nodes_from(self._nodes)

        # Add edges
        # Metodo 1
        # allEdges = DAO.getAllEdges(provider)
        # for edge in allEdges:  # edge = (loc1,loc2) 2 oggetti Location
        #     l1 = edge[0]
        #     l2 = edge[1]
        #     # distance di geopy vuole come argomento una coppia di tuple
        #     dist = distance((l1.Latitude, l1.Longitude), (l2.Latitude, l2.Longitude))
        #     if dist <= soglia:
        #         self._grafo.add_edge(l1, l2, weight=dist)
        #
        # print(f"Modo 1: N nodes:  {len(self._grafo.nodes)} - N edges: {len(self._grafo.edges)}")

        # Metodo 2
        # modifico il metodo del dao che legge i nodi, e ci aggiungo le coordinate di ogni location
        # Dopo, doppio ciclo sui nodi e mi calcolo la distanza tra ogni coppia di nodi in python
        for u in self._nodes:
            for v in self._nodes:
                if u != v:
                    # calcolo la distanza tra u e v
                    dist = distance((u.Latitude, u.Longitude), (v.Latitude, v.Longitude))
                    if dist <= soglia:
                        self._grafo.add_edge(u, v, weight=dist)
        print(f"Modo 2: N nodes:  {len(self._grafo.nodes)} - N edges: {len(self._grafo.edges)}")

        # Metodo 3: Doppio ciclo sui nodi, e per ogni "possibile" arco, faccio una query.

    def getProviders(self):
        return DAO.getAllProviders()

    def getGraphDetails(self):
        return self._grafo.number_of_nodes(), self._grafo.number_of_edges()

    def getNodesMostVicini(self):
        listTuples = []
        for node in self._nodes:
            totVicini = len(list(self._grafo.neighbors(node)))
            listTuples.append((node, totVicini))
        listTuples.sort(key=lambda x: x[1], reverse=True)

        # result1 = filter(lambda x: x[1] == listTuples[0][1], listTuples)
        # oppure
        result2 = [x for x in listTuples if x[1] == listTuples[0][1]]

        return result2

    def getCammino(self, target, substring):
        sources = self.getNodesMostVicini()
        source = sources[random.randint(0, len(sources) - 1)][0]

        if nx.has_path(self._grafo, source, target):
            print(f"Cammino tra {source} e {target} esiste")
        else:
            print(f"Cammino tra {source} e {target} NON esiste")
            return [], source

        self._bestPath = []
        self._bestLength = 0
        parziale = [source]
        self._ricorsione(parziale, target, substring)

        return self._bestPath, source

    def _ricorsione(self, parziale, target, substring):
        if parziale[-1] == target:
            if len(parziale) > len(self._bestPath):
                self._bestPath = copy.deepcopy(parziale)
                self._bestLength = len(parziale)
            return

        for v in self._grafo.neighbors(parziale[-1]):
            if v not in parziale and v.Location.find(substring) != -1:
                parziale.append(v)
                self._ricorsione(parziale, target, substring)
                parziale.pop()

