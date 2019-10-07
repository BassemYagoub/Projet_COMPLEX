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
        checkpoint = "Sommets"
        while(ligne):
            ligne = ligne.replace("\n", "")
            ligne = ligne.replace("\t", "")
            ligne = ligne.replace(" ", "")
            #print(checkpoint)
            print(str.isnumeric(ligne))
            if(not str.isnumeric(ligne)):
                checkpoint = ligne
                #print(checkpoint)
            if(checkpoint == "Sommets"):
                if(not str.isnumeric(ligne)):
                    sommets.append(ligne)
                    print("sommets", sommets)
            elif(checkpoint == "Aretes"):
                pass
            ligne = f.readline()
    finally:
        f.close()
    
importGrapheFromTxt("exempleinstance.txt")
    
graphe = nx.Graph()
graphe.add_nodes_from([i for i in range (0,4)])
graphe.add_edges_from([(0,1), (3,2)])
#nx.draw(graphe, with_labels=True)
