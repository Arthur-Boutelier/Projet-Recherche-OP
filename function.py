from collections import deque

def somme_ligne(matrice,indice):
    resultat = 0
    for nombre in matrice[indice]:
        resultat += nombre
    return resultat
    
def somme_colonne(matrice,indice):
    resultat = 0
    for ligne in matrice:
        resultat += ligne[indice]
    return resultat 

def est_connexe(graphe, verbose=True):
    nb_ligne = len(graphe)
    nb_colonne = len(graphe[0])
    liste_graphes = []
    sommets_restant = {(i, "ligne") for i in range(nb_ligne)} | {(j, "col") for j in range(nb_colonne)}
    while sommets_restant:
        sommet_depart = sommets_restant.pop()
        sous_graphe_en_cours = {sommet_depart}
        sommets_en_cours = deque([sommet_depart])
        while sommets_en_cours:
            sommet, type_sommet = sommets_en_cours.popleft()
            if type_sommet == "ligne":
                for ind in range(nb_colonne):
                    if graphe[sommet][ind] != 0 and (ind, "col") not in sous_graphe_en_cours:                            
                        sommets_en_cours.append((ind, "col"))
                        sous_graphe_en_cours.add((ind, "col"))
                        sommets_restant.discard((ind, "col"))
            else:
                for ind in range(nb_ligne):
                    if graphe[ind][sommet] != 0 and (ind, "ligne") not in sous_graphe_en_cours:
                        sommets_en_cours.append((ind, "ligne"))
                        sous_graphe_en_cours.add((ind, "ligne"))
                        sommets_restant.discard((ind, "ligne"))
        liste_graphes.append(sous_graphe_en_cours)
    if verbose:
        affichage_sous_graphe(liste_graphes)
    return len(liste_graphes) == 1, liste_graphes
            
        
    
def detection_cycle(graphe, verbose = True):
    nb_ligne = len(graphe)
    nb_colonne = len(graphe[0])
    parents = {(0, "ligne") : None}
    sommets_en_cours = deque([(0, "ligne", None)])
    while sommets_en_cours:
        sommet, type_sommet, parent = sommets_en_cours.popleft()
        if type_sommet == "ligne":
            for ind in range(nb_colonne):
                if ind != parent and graphe[sommet][ind] != 0:
                    voisin = (ind, "col")
                    if voisin in parents:
                        cycle = recreation_cycle(parents, (sommet,type_sommet), voisin)
                        if verbose:
                            affichage_cycle(cycle)
                        return True, cycle
                    parents[voisin] = (sommet,type_sommet)
                    sommets_en_cours.append((ind, "col", sommet))
        else:
            for ind in range(nb_ligne):
                if ind != parent and graphe[ind][sommet] != 0:
                    voisin = (ind, "ligne")
                    if voisin in parents:
                        cycle = recreation_cycle(parents, (sommet,type_sommet), voisin)
                        if verbose:
                            affichage_cycle(cycle)
                        return True, cycle
                    parents[voisin] = (sommet,type_sommet)
                    sommets_en_cours.append((ind, "ligne", sommet))
    return False, []
                    
def recreation_cycle(parents, noeud_fin, noeud_boucle):
    chemin_fin = [noeud_fin]
    chemin_boucle = [noeud_boucle]
    # on fait le chemin depuis le noeud de fin
    courant = noeud_fin
    while parents[courant] != None:
        courant = parents[courant]
        chemin_fin.append(courant)
           # on fait le chemin pour le noeud de boucle    
    courant = noeud_boucle
    while parents[courant] != None:
        courant = parents[courant]
        chemin_boucle.append(courant)
    
    while len(chemin_boucle) > 1 and len(chemin_fin) > 1 and chemin_fin[-2] == chemin_boucle[-2]:
        chemin_boucle.pop()
        chemin_fin.pop()
    
    chemin_fin.reverse()
    return chemin_fin + chemin_boucle[:-1]

def affichage_cycle(cycle):
    print("Le cycle est composé de :")
    for element in cycle:
        if element[1] == "ligne":
            print("La ligne", element[0])
        else:
            print("La colonne", element[0])

def affichage_sous_graphe(tab_graphe):
    print(f"Dans ce graphe on observe {len(tab_graphe)} sous-graphes connexe :\n")
    for ind in range(len(tab_graphe)):
        print(f"sous-graphe {ind + 1} :")
        print("Il contient les lignes :")
        lignes = sorted({s[0] for s in tab_graphe[ind] if s[1] == "ligne"})
        colonnes = sorted({s[0] for s in tab_graphe[ind] if s[1] == "col"})
        for ligne in lignes:
            print(ligne)
        print("\nEt les colonnes :")
        for colonne in colonnes:
            print(colonne)
        print("\n")
        
        