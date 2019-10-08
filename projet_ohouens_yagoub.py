"""
Created on Mon Oct  7 11:25:22 2019

@author: 3521571, 3670015
"""

import networkx as nx
import matplotlib.pyplot as plt

"""import numpy as np
class Graphe():

    def __init__(self, nbSommets, nbArretes):
        self.nbS = nbSommets;
        self.nbA = nbArretes;
        self.listeAdj = np.array()
        
    def estimClass(self, attrs):
        return 1.0
"""

def importGrapheFromTxt(file):
    """
    params : 
        file (string) : nom du fichier texte
    return : nx.Graph() (graphe) avec les sommets et arêtes lus dans le fichier.
    """
    try:
        f = open(file, "r")
        sommets = [] #liste des sommets
        aretes  = [] #liste des couples (sommet, sommet) (arêtes)
        ligne = f.readline()
        checkpoint = "Sommets" #checkpoint initial
        
        while(ligne):
            ligne = ligne.replace("\n", "")
            ligne = ligne.replace("\t", "")
            if(checkpoint != "Aretes"):
                ligne = ligne.replace(" ", "")
                
            if(not str.isnumeric(ligne) and checkpoint != "Aretes"):
                checkpoint = ligne
                
            if(checkpoint == "Sommets"):
                if(str.isnumeric(ligne)):
                    sommets.append(ligne)
                    
            #on a passé "Aretes" mais on n'ajoute pas sa ligne
            elif(checkpoint == "Aretes" and ligne !="Aretes"):
                sommet1, sommet2 = ligne.split() #les s1 et s2 composent l'arete
                aretes.append((int(sommet1), int(sommet2))) #liste string devient couple d'int
                    
            ligne = f.readline()

        #creation du graphe à retourner
        graphe = nx.Graph()
        graphe.add_nodes_from(sommets)
        graphe.add_edges_from(aretes)
        return graphe
    
    finally:
        f.close()

def dessine(G):
    """
    dessine le graphe G
    """
    nx.draw(G, with_labels=True)

#2.1.1
def graphePartiel(G, v):
    """
    retourne un graphe graphe G2 obtenu à partir de G en supprimant le sommet v
    """
    G2 = nx.Graph(G)
    G2.remove_node(v)
    return  G2

graphe = importGrapheFromTxt("exempleinstance.txt")

graphe2 = graphePartiel(graphe, 0)
dessine(graphe2)
