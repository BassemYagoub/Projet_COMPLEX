"""
Created on Mon Oct  7 11:25:22 2019
@author: Bassem Yagoub (3521571), Ryan Ohouens (3670015)
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import time
import math

"""import numpy as np
class Graphe():
    def __init__(self, nbSommets, nbArretes):
        self.nbS = nbSommets;
        self.nbA = nbArretes;
        self.listeAdj = np.array()

    def estimClass(self, attrs):
        return 1.0
"""

def importGrapheFromTxt(file, show=False):
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
        if(show):
            dessine(graphe)
        return graphe

    finally:
        f.close()

def dessine(G):
    """
    dessine le graphe G
    """
    nx.draw(G, with_labels=True)
    plt.show()

#2.1.1, 2.1.2
def sousGraphe(G, v, show=False):
    """
    params:
        G: nx.Graph(), le graphe initial
        v: le(s) sommet(s) à retirer de G

    return : un graphe graphe G2 obtenu à partir de G en supprimant le(s) sommet(s) v (ou de v)
    """
    G2 = nx.Graph(G)
    if(isinstance(v, int)):
        G2.remove_node(v)
    if(isinstance(v, list)):
        G2.remove_nodes_from(v)
    if(show):
        dessine(G2)
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

#2.2
def creerInstance(n, p, show=False):
    """
    params:
        n: int>0, nombre de sommets
        p: float ]0,1[, probabilité d'existence de chaque arête
    return : nx.Graph() avec n sommets et m<=n arêtes
    ----------
    stats temps: n=2500, p=0.5 : 10s
    """
    if(n < 0 or (p < 0.0 or p > 1.0)):
        raise Exception("n < 0 ou bien p n'est pas une probabilité")

    graphe = nx.Graph()
    graphe.add_nodes_from([i for i in range(n)]) #on a le graphe avec n noeuds

    if(n == 1):
        if(show):
            dessine(graphe)
        return graphe

    for i in range(n-1):
        for j in range(i+1, n): #début=i+1 pour ne pas etre redondant
            areteOk = np.random.binomial(1, p)
            if(areteOk == 1):
                graphe.add_edge(i,j)
    if(show):
        dessine(graphe)
    return graphe

#3.2
def algo_couplage(G):
    """
    params:
        G: nx.Graph()
    return: Une couverture de G
    """
    c_aretes = []
    c = [] #sommets visites
    for arete in (G.edges):
        if(arete[0] not in c and arete[1] not in c):
            c_aretes.append(arete)
            c.extend([arete[0], arete[1]]) #ajout des sommets exclus par la suite
    return c#, c_aretes

def algo_glouton(G):
    """
    Version glouton de algo_couplage
    params:
        G: nx.Graph()
    return: Une couverture de G
    """
    c = []
    E = G.edges #tableau des aretdees modifié dynamiquement dans la boucle
    #aretes_couvs = []
    #print("e", E)
    while(len(E) > 0):
        v = degreMax(G) #sommet de degre max
        #print(v)
        c.append(v)
        aretes_suppr = [arete for arete in E if( (arete[0]==v) or (arete[1]==v) )] #liste d'aretes de v à supprimer
        """
        print("suppr", aretes_suppr)

        i=0
        while(aretes_suppr[i][0] in aretes_couvs or aretes_suppr[i][1] in aretes_couvs):
            i+=1
        aretes_couvs.append(aretes_suppr[i]) #premiere arete qu'on va supprimer sera dans les aretes couvertes
        #print(aretes_couvs)
        """
        G.remove_edges_from(aretes_suppr)
        #dessine(G)
        #plt.show()
    return c

def compare_couvs(n_min, n_max, nb_ites=20, nb_moys=5, dessin=False):
    """
    Compare les durées d'exéc de algo_couplage et algo_glouton en fonction de n, p via les courbes (n en fonction du temps)
    params:
        n_min: int>0, nombre de sommets min
        n_min: int>0, nombre de sommets max
        p: float ]0,1[, probabilité d'existence de chaque arête
        dessin: boolean, affiche le graphe ou non
    return: (algo_couplage(graphe), algo_glouton(graphe))
    """

    #pour chaque p
    for p in np.arange(0.25, 1.01, 0.25): #1.01 permet que le graphe à p=1 soit effectué
        nb_sommets_iteres = []

        temps_couplages = []
        card_moy_sols_couplage = 0

        temps_gloutons  = []
        card_moy_sols_glouton = 0

        #pour chaque n
        for n in range(n_min, n_max, int(n_max/nb_ites)):
            t_couplage_i, t_glouton_i = 0, 0 #sommes des temps pour chaque algo, pour chaque n
            card_moy_couplage_i, card_moy_glouton_i = 0, 0

            #permet d'avoir une moyenne via differents graphes pour un même n
            for i in range(nb_moys):
                graphe = creerInstance(n, p)
                if(dessin == True):
                    dessine(graphe)

                #couplage
                start = time.time()
                couplage = algo_couplage(graphe)
                t_couplage_i += time.time() - start
                card_moy_couplage_i += len(couplage)
                #print("couplage : \n", couplage, "\nDurée Exec :", (end - start))

                #glouton
                start = time.time()
                glouton = algo_glouton(graphe)
                t_glouton_i += time.time() - start
                card_moy_glouton_i += len(glouton)
                #print("\nglouton : \n", glouton, "\nDurée Exec : ", (end - start))

            #on divise la somme des temps par nb_repets pour avoir une moyenne pour chaque n
            temps_couplages.append(t_couplage_i/nb_moys)
            temps_gloutons.append(t_glouton_i/nb_moys)

            card_moy_sols_couplage += card_moy_couplage_i/nb_moys
            card_moy_sols_glouton += card_moy_glouton_i/nb_moys

            nb_sommets_iteres.append(n)

        """ plot de courbes """
        plt.title("Durée des algos en fonction du nombre de sommets avec p={:.2f}".format(p))
        plt.plot(nb_sommets_iteres, temps_couplages, 'r', label="Algo Couplage")
        plt.plot(nb_sommets_iteres, temps_gloutons, 'b', label="Algo Glouton")
        plt.legend(loc='best')
        plt.ylabel('Temps (en s)')
        plt.xlabel('Nombre de sommets (n)')
        plt.show()
        print("cardinalité moyenne de la couverture via couplage : ", card_moy_sols_couplage/nb_ites, "\n")
        print("cardinalité moyenne de la couverture via glouton : ", card_moy_sols_glouton/nb_ites, "\n")

    return couplage, glouton


#---------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------4.1 & 4.2------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
def bound(G, c, showSteps=False):
    n = len(G)
    m = G.number_of_edges()
    delta = 1
    for noeud, deg in G.degree:
        if deg > delta:
            delta = deg
    b1 = m/delta
    b2 = len(algo_couplage(G))/2
    b3 = (2*n-1-math.sqrt((2*n-1)**2-8*m))/2
    b = max(b1, b2, b3)
    if(showSteps):
        print("n", n)
        print("m", m)
        print("delta", delta)
        print("b1", b1)
        print("b2", b2)
        print("b3", b3)
        print("bound", b)
        print("c", c)
    return  b

def amelioration(G, u, v, showSteps=False):
    voisins = []
    if(showSteps):
        print("u", u)
        print("v", v)
    for arete in G.edges:
        if(u in arete and v not in arete):
            if(u == arete[0]):
                voisins.append(arete[1])
            else:
                voisins.append(arete[2])
    if(showSteps):
        print("voisins de u", voisins)
    return sousGraphe(G, voisins, showSteps), voisins

total = 0
def branchbound(G, c=[], avecCoupe=False, showSteps=False, epsilon=0, coupe=[], optmized=False):
    global total
    total += 1
    if(showSteps):
        print("total des noeuds parcourues", total)

    if(len(G.edges) == 0):
        if(showSteps):
            print("-----feuille atteinte-----")
            dessine(G)
        return c

    if(avecCoupe):
        borneInf = bound(G, c, showSteps)
        if(showSteps):
            print("---borne---", borneInf)
        if(len(c) >= borneInf+epsilon):
            if(showSteps):
                print("-----Elagage!-----")
                dessine(G)
            return coupe

    u, v = [arete for arete in G.edges][0]
    if(showSteps):
        print("-------DESCENTE GAUCHE--------")
        dessine(G)
    g_u = branchbound(sousGraphe(G, u), c+[u], avecCoupe, showSteps, epsilon, coupe, optmized)
    if(showSteps):
        print("-------REMONTEE GAUCHE--------\n\n")
        print("-------DESCENTE DROITE--------")
        dessine(G)
    if(not optmized):
        g_v = branchbound(sousGraphe(G, v), c+[v], avecCoupe, showSteps, epsilon, coupe, optmized)
    else:
        GSu, cSu = amelioration(G, u, v, showSteps)
        g_v = branchbound(sousGraphe(GSu, v), c+cSu+[v], avecCoupe, showSteps, epsilon, coupe, optmized)
    if(showSteps):
        print("-------REMONTEE DROITE--------\n\n")
        print("::::Choix entre", g_u, "et", g_v, "::::")
    if(len(g_u) > len(g_v)):
        if(showSteps):
            print("-----branche droite choisie-----")
            print(g_v)
            dessine(G)
        return g_v
    else:
        if(showSteps):
            print("-----branche gauche choisie-----")
            print(g_u)
            dessine(G)
        return g_u
#----------------------------------------------------------------------------------------------------------------
#------------------------------------------------------MAIN------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------
# graphe = importGrapheFromTxt("exempleinstance2.txt")
nbV = 5
E = 2
beta = [1 for k in range(nbV+1)]
p = 1/math.sqrt(nbV)
if(nbV < 7):
    p = 0.7
graphe = creerInstance(nbV, p, True)
# compare_couvs(10, 200)
#graphe = importGrapheFromTxt("exemple_branchbound.txt")
print("b&b sans borne inferieur sans optimisation donne le resultat", branchbound(graphe, []), "avec un total de noeuds parcourues de", total)
total = 0
print("b&b avec borne inferieur sans optimisation donne le resultat", branchbound(graphe, [], True, False, E, beta), "avec un total de noeuds parcourues de", total)
total = 0
print("b&b sans borne inferieur avec optimisation donne le resultat", branchbound(graphe, [], False, False, E, beta, True), "avec un total de noeuds parcourues de", total)
