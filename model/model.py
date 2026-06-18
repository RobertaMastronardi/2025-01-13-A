import copy
import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._graph=nx.Graph()
        self._classifications=[]
        self._idMapC={}
        self._bestPath=[]
    #PARTE DI RICORSIONE TOSTA, SEGNARSELA!!!
    def getBestPath(self):
        self._bestPath=[]
        for ess in ("Essential", "Non-Essential"):
            candidati=[n for n in self._graph.nodes if n.Essential==ess]
            self._ricorsione([], candidati, 0)
        self._bestPath.sort(key=lambda n:n.GeneID)
        return self._bestPath
    def _ricorsione(self,parziale, candidati, index):
        if self._isMigliore(parziale):
            self._bestPath=copy.deepcopy(parziale)
        if index>=len(candidati):
            return
        #INCLUDO
        parziale.append(candidati[index])
        self._ricorsione(parziale, candidati, index+1)
        parziale.pop()
        #ESCLUDO
        self._ricorsione(parziale, candidati, index + 1)



    def _numComponenti(self, parziale):
        sg=subgraph=self._graph.subgraph(parziale).copy()
        nConn=nx.connected_components(sg)
        return nConn



    def _isMigliore(self, parziale):
        if len(parziale)>len(self._bestPath):
            return True
        if len(parziale)==len(self._bestPath) and len(parziale)>0  :
            return self._numComponenti(parziale)<self._numComponenti(self._bestPath)
        return False





    def buildGraph(self, localization):
        self._graph.clear()
        self._classifications=DAO.get_all_nodes(localization)
        for c in self._classifications:
            self._idMapC[c.GeneID]=c

        self._graph.add_nodes_from(self._classifications)
        edges=DAO.get_all_interactions(localization)
        peso=None
        for e in edges:
            if e[2]!=e[3]:
                peso=e[2]+e[3]
                self._graph.add_edge(self._idMapC[e[0]], self._idMapC[e[1]], weight=peso)
            else:
                peso=e[2]
                self._graph.add_edge(self._idMapC[e[0]], self._idMapC[e[1]], weight=peso)

    def getInfoConnessa(self):
        components=list(nx.connected_components(self._graph))
        components_max=[]
        for c in components:
            if len(c)>1:
                components_max.append((list(c), len(c)))
        components_max.sort(key=lambda x: x[1], reverse=True)
        return components_max


    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)




    def getAllLocalizations(self):
        self._localizations=DAO.get_all_localizations()
        return self._localizations

    def getAllEdges(self):
        edges=sorted(self._graph.edges(data=True), key=lambda x: x[2]['weight'])
        return edges
