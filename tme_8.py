def jeu(n):
    echiquier = []
    for i in range(n):
        echiquier.append(["O"]*n)
    return echiquier

def affiche(echiquier):
    for ligne in echiquier:
        print(ligne)
    print("")
def disponibilite_pos(echiquier, x, y):
    n = len(echiquier)
    for i in range(n):
        #|
        if(echiquier[x][i] == "X"):
            return False
        #--disponibilite_pos
        if(echiquier[i][y] == "X"):
            return False
        #bas droit
        if(x+i < n and y+i < n):
            if(echiquier[x+i][y+i] == "X"):
                # print(x+i, y+i)
                return False
        #haut gauche
        if(x-i >= 0 and y-i >= 0):
            if(echiquier[x-i][y-i] == "X"):
                # print(x-i, y-i)
                return False
        #bas gauche
        if(x+i < n and y-i >= 0):
            if(echiquier[x+i][y-i] == "X"):
                # print(x+i, y-i)
                return False
        #haut droit
        if(x-i >= 0 and y+i < n):
            if(echiquier[x-i][y+i] == "X"):
                # print(x-i, y+i)
                return False
    return True

# def agencement_reine(n):
#     echiquier = jeu(n)
#     a_placer = n
#     placement_ok = False
#     #checkpoint
#     while(a_placer > 0 or ):
#         for i in range(n):
#             for j in range(n):
#                 if(disponibilite_pos(echiquier, i, j)):
#                     echiquier[i][j] = "X"
#                     placement_ok = True
#                     a_placer -= 1
#                     break
#             if(placement_ok):
#                 placement_ok = False
#                 break

def agencement_reine_rec(n, j=0, echiquier=[]):
    affiche(echiquier)
    i = 0
    while(i < n):
        if(disponibilite_pos(echiquier, i, j)):
            echiquier[i][j] = "X"
            print("T")
            agencement_reine_rec(n, j+1, echiquier)
            if(j == n-1):
                return true
        else:
            i += 1
            echiquier[i][j] = "X"
            print("F")
            agencement_reine_rec(n, j+1, echiquier)
    return false

# echec = jeu(5)
# n = len(echec)
# x = 3
# y = 2
# for i in range(len(echec)):
#     # if(x+i < n and y+i < n):
#     #     echec[x+i][y+i] = "X"
#     # if(x-i >= 0 and y-i >= 0):
#     #     echec[x-i][y-i] = "X"
#     if(x+i < n and y-i >= 0):
#         echec[x+i][y-i] = "X"
#     if(x-i >= 0 and y+i < n):
#         echec[x-i][y+i] = "X"
# affiche(echec)
# print(disponibilite_pos(echec,  0, 1))

n=4
echiquier = jeu(n)
agencement_reine_rec(n, 0, echiquier)
