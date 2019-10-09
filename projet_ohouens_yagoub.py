"""
Created on Mon Oct  7 11:25:22 2019

@author: Bassem Yagoub (3521571), Ryan Ohouens (3670015)
"""

import networkx as nx
import matplotlib.pyplot as plt

def importGrapheFromTxt(file):
    """
    params :
        file (string) : nom du fichier texte
    return : nx.Graph() (graphe) avec les sommets et arêtes lus dans le fichier.
    """
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
                sommets.append(int(ligne))

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

def dessine(G):
    """
    dessine le graphe G
    """
    nx.draw(G, with_labels=True)
    plt.show()

#2.1.1, 2.1.2
def sousGraphe(G, v):
    """
    params:
        G: nx.Graph(), le graphe initial
        v: le(s) sommet(s) à retirer de G

    return : un graphe graphe G2 obtenu à partir de G en supprimant le(s) sommet(s) v (ou de v)
    """
    G2 = nx.Graph(G)
    if(isinstance(v, int)):
        G2.remove_node(v)
    elif(isinstance(v, list)):
        G2.remove_nodes_from(v)
    return  G2

#2.1.3
def degresSommets(G):
    """
    params:
        G: nx.Graph(), le graphe à analyser
    return : liste de degrés de chaque sommet de G
    """
    noeuds_degs = G.degree
    return [noeuds_degs[i] for i in range(len(noeuds_degs))]

def degreMax(G):
    """
    params:
        G: nx.Graph(), le graphe à analyser
    return : indice du sommet de degré max de G
    """
    sommets = degresSommets(G)
    return sommets.index(max(sommets))



#----------------------------------------------------------
#---------------------------MAIN---------------------------
#----------------------------------------------------------

graphe = importGrapheFromTxt("exempleinstance.txt")
dessine(graphe)#ne m'affiche rien

grapheP = sousGraphe(graphe, [0,1,2,8])
dessine(grapheP)#ne m'affiche rien

graphe.add_edges_from([(1, 3), (1, 2)])
dessine(graphe)#m'affiche un chemin 2-1-3

print(degreMax(graphe))
