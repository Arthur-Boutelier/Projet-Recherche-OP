from function import *
from collections import deque


class ProblemeTransport():
    def __init__(self, nb_ligne, nb_colonne):
        self.cout = [[0 for _ in range(nb_colonne)] for _ in range(nb_ligne)]
        self.prob_transp = [[0 for _ in range(nb_colonne)] for _ in range(nb_ligne)]
        self.provision = [0 for _ in range(nb_ligne)]
        self.commande = [0 for _ in range(nb_colonne)]
        self.nb_ligne = nb_ligne
        self.nb_colonne = nb_colonne
        self.dico_cout_pot = {}
        self.mat_cout_pot = [[0 for _ in range(nb_colonne)] for _ in range(nb_ligne)]
        self.mat_cout_marg = [[0 for _ in range(nb_colonne)] for _ in range(nb_ligne)]

    def __init__(self, doc):
        with open(str("data/" + doc),'r', encoding="utf-8") as fichier:
            tab_ligne = fichier.readlines()
            ligne_0 = tab_ligne[0].strip()
            ligne_0 = ligne_0.split(" ")
            self.nb_ligne = int(ligne_0[0])
            self.nb_colonne = int(ligne_0[1])
            tab_ligne = tab_ligne[1:]
            self.dico_cout_pot = {}
            self.mat_cout_pot = [[0 for _ in range(self.nb_colonne)] for _ in range(self.nb_ligne)]
            self.mat_cout_marg = [[0 for _ in range(self.nb_colonne)] for _ in range(self.nb_ligne)]
            for indice_ligne in range(len(tab_ligne)):
                tab_ligne[indice_ligne] = tab_ligne[indice_ligne].strip()
                tab_ligne[indice_ligne] = tab_ligne[indice_ligne].split()
                tab_ligne[indice_ligne] = [int(element) for element in tab_ligne[indice_ligne]]
            self.cout = tab_ligne[:self.nb_ligne]
            self.cout = [element[:self.nb_colonne] for element in self.cout]
            self.commande = tab_ligne[-1]
            self.provision = [element[-1] for element in tab_ligne[:-1]]
            self.prob_transp = [[0 for _ in range(self.nb_colonne)] for _ in range(self.nb_ligne)]
            
    def nord_west(self):
        self.prob_transp = [[0 for _ in range(self.nb_colonne)] for _ in range(self.nb_ligne)]
        ligne = 0
        colonne = 0
        while (ligne < self.nb_ligne) and (colonne < self.nb_colonne):
            lim_ligne = self.provision[ligne] - somme_ligne(self.prob_transp, ligne)
            lim_colonne = self.commande[colonne] - somme_colonne(self.prob_transp, colonne)
            if lim_colonne < lim_ligne:
                self.prob_transp[ligne][colonne] = lim_colonne
                colonne +=1
            elif lim_colonne > lim_ligne:
                self.prob_transp[ligne][colonne] = lim_ligne
                ligne += 1
            elif lim_colonne == lim_ligne:
                self.prob_transp[ligne][colonne] = lim_colonne
                ligne += 1
                colonne+=1

    def hammer(self, verbose=True):
        if verbose:
            print("Résolution avec Balas-Hammer")
        self.prob_transp = [[0 for _ in range(self.nb_colonne)] for _ in range(self.nb_ligne)]
        tab_ind_ligne_poss = [i for i in range(self.nb_ligne)]
        tab_ind_col_poss = [i for i in range(self.nb_colonne)]
        iteration = 1
        while len(tab_ind_ligne_poss) != 0 and len(tab_ind_col_poss) != 0:
            delta_ligne = []
            delta_colonne = []
            for ind_ligne in tab_ind_ligne_poss:
                delta_ligne.append(self.calcul_delta_hammer_ligne(tab_ind_col_poss, ind_ligne))
            for ind_col in tab_ind_col_poss:
                delta_colonne.append(self.calcul_delta_hammer_colonne(tab_ind_ligne_poss, ind_col))
            tab_min_delta = [(-float('inf'),)]
            for delta in delta_ligne:
                if delta[0] > tab_min_delta[0][0]:
                    tab_min_delta = [delta]
                elif delta[0] == tab_min_delta[0][0]:
                    if self.cout[tab_min_delta[0][1]][tab_min_delta[0][2]] > self.cout[delta[1]][delta[2]]:
                        tab_min_delta.insert(0, delta)
                    else:
                        tab_min_delta.append(delta)
            for delta in delta_colonne:
                if delta[0] > tab_min_delta[0][0]:
                    tab_min_delta = [delta]
                elif delta[0] == tab_min_delta[0][0]:
                    if self.cout[tab_min_delta[0][1]][tab_min_delta[0][2]] > self.cout[delta[1]][delta[2]]:
                        tab_min_delta.insert(0, delta)
                    else:
                        tab_min_delta.append(delta)
            min_delta = tab_min_delta[0]
            if verbose:
                print(f"Itération {iteration} :")
                print(f"Colonne/Ligne de pénalité maximale avec une pénalité de {tab_min_delta[0][0]} :")
                for delta in tab_min_delta:
                    if delta[3] == "ligne":
                        print(f"La ligne d'indice {delta[1]}")
                    else:
                        print(f"La colonne d'indice {delta[2]}")
                print(f"On choisit maintenant l'arête ({min_delta[1]},{min_delta[2]}) car elle possède le coût minimum qui est de {self.cout[min_delta[1]][min_delta[2]]}\n\n")
                iteration += 1
            prov_poss = self.provision[min_delta[1]] - somme_ligne(self.prob_transp, min_delta[1])
            com_poss = self.commande[min_delta[2]] - somme_colonne(self.prob_transp, min_delta[2])
            if prov_poss < com_poss:
                self.prob_transp[min_delta[1]][min_delta[2]] = prov_poss
                tab_ind_ligne_poss.remove(min_delta[1])
            elif prov_poss > com_poss:
                self.prob_transp[min_delta[1]][min_delta[2]] = com_poss
                tab_ind_col_poss.remove(min_delta[2])
            else:
                self.prob_transp[min_delta[1]][min_delta[2]] = prov_poss
                tab_ind_ligne_poss.remove(min_delta[1])
                tab_ind_col_poss.remove(min_delta[2])
                
            
        
    
    
    def calcul_delta_hammer_ligne(self,tab_ind_poss, ligne):
        if len(tab_ind_poss) == 1:
            return self.cout[ligne][tab_ind_poss[0]], ligne, tab_ind_poss[0], "ligne"
        ind_min_1 = 0
        ind_min_2 = 1
        if self.cout[ligne][tab_ind_poss[0]] > self.cout[ligne][tab_ind_poss[1]]:
            ind_min_1 = 1
            ind_min_2 = 0
        for ind in range(2, len(tab_ind_poss)):
            if self.cout[ligne][tab_ind_poss[ind]] < self.cout[ligne][tab_ind_poss[ind_min_1]]:
                ind_min_2 = ind_min_1
                ind_min_1 = ind
            elif self.cout[ligne][tab_ind_poss[ind]] < self.cout[ligne][tab_ind_poss[ind_min_2]]:
                ind_min_2 = ind
        return self.cout[ligne][tab_ind_poss[ind_min_2]] - self.cout[ligne][tab_ind_poss[ind_min_1]], ligne ,tab_ind_poss[ind_min_1], "ligne"
        
    
    def calcul_delta_hammer_colonne(self,tab_ind_poss, colonne):
        if len(tab_ind_poss) == 1:
            return self.cout[tab_ind_poss[0]][colonne], tab_ind_poss[0], colonne, "colonne"
        ind_min_1 = 0
        ind_min_2 = 1
        if self.cout[tab_ind_poss[0]][colonne] > self.cout[tab_ind_poss[1]][colonne]:
            ind_min_1 = 1
            ind_min_2 = 0
        for ind in range(2, len(tab_ind_poss)):
            if self.cout[tab_ind_poss[ind]][colonne] < self.cout[tab_ind_poss[ind_min_1]][colonne]:
                ind_min_2 = ind_min_1
                ind_min_1 = ind
            elif self.cout[tab_ind_poss[ind]][colonne] < self.cout[tab_ind_poss[ind_min_2]][colonne]:
                ind_min_2 = ind
        return self.cout[tab_ind_poss[ind_min_2]][colonne] - self.cout[tab_ind_poss[ind_min_1]][colonne], tab_ind_poss[ind_min_1], colonne, "colonne"

    def calcul_cout_tot(self):
        cout_tot = 0
        for i in range(self.nb_ligne):
            for j in range(self.nb_colonne):
                cout_tot += self.cout[i][j] * self.prob_transp[i][j]
        return cout_tot
    
    def detection_cycle(self, verbose = True):
        parents = {(0, "ligne") : None}
        sommets_en_cours = deque([(0, "ligne", None)])
        while sommets_en_cours:
            sommet, type_sommet, parent = sommets_en_cours.popleft()
            if type_sommet == "ligne":
                for ind in range(self.nb_colonne):
                    if ind != parent and self.prob_transp[sommet][ind] != 0:
                        voisin = (ind, "col")
                        if voisin in parents:
                            cycle = ProblemeTransport.recreation_cycle(parents, (sommet,type_sommet), voisin)
                            if verbose:
                                ProblemeTransport.affichage_cycle(cycle)
                            return True, cycle
                        parents[voisin] = (sommet,type_sommet)
                        sommets_en_cours.append((ind, "col", sommet))
            else:
                for ind in range(self.nb_ligne):
                    if ind != parent and self.prob_transp[ind][sommet] != 0:
                        voisin = (ind, "ligne")
                        if voisin in parents:
                            cycle = ProblemeTransport.recreation_cycle(parents, (sommet,type_sommet), voisin)
                            if verbose:
                                ProblemeTransport.affichage_cycle(cycle)
                            return True, cycle
                        parents[voisin] = (sommet,type_sommet)
                        sommets_en_cours.append((ind, "ligne", sommet))
        return False, []
    
    @staticmethod
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
    
    @staticmethod
    def affichage_cycle(cycle):
        print("Le cycle est composé de :")
        for element in cycle:
            if element[1] == "ligne":
                print("La ligne", element[0])
            else:
                print("La colonne", element[0])
                
                
    @staticmethod
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
    
    def est_connexe(self, verbose=True):
        liste_graphes = []
        sommets_restant = {(i, "ligne") for i in range(self.nb_ligne)} | {(j, "col") for j in range(self.nb_colonne)}
        while sommets_restant:
            sommet_depart = sommets_restant.pop()
            sous_graphe_en_cours = {sommet_depart}
            sommets_en_cours = deque([sommet_depart])
            while sommets_en_cours:
                sommet, type_sommet = sommets_en_cours.popleft()
                if type_sommet == "ligne":
                    for ind in range(self.nb_colonne):
                        if self.prob_transp[sommet][ind] != 0 and (ind, "col") not in sous_graphe_en_cours:                            
                            sommets_en_cours.append((ind, "col"))
                            sous_graphe_en_cours.add((ind, "col"))
                            sommets_restant.discard((ind, "col"))
                else:
                    for ind in range(self.nb_ligne):
                        if self.prob_transp[ind][sommet] != 0 and (ind, "ligne") not in sous_graphe_en_cours:
                            sommets_en_cours.append((ind, "ligne"))
                            sous_graphe_en_cours.add((ind, "ligne"))
                            sommets_restant.discard((ind, "ligne"))
            liste_graphes.append(sous_graphe_en_cours)
        if verbose:
            ProblemeTransport.affichage_sous_graphe(liste_graphes)
        return len(liste_graphes) == 1, liste_graphes
    
    def calcul_cout_potentiel(self, verbose = True):
        if verbose:
            print("On initialise le cout potentielle de la ligne 0 à 0")
            print(self.mat_cout_pot)
        self.dico_cout_pot = {(0, "ligne"): 0}
        en_cours = deque([(0, "ligne")])
        while len(self.dico_cout_pot) != (self.nb_colonne + self.nb_ligne) and en_cours:
            sommet, type_sommet = en_cours.popleft()
            if type_sommet == "ligne":
                for ind in range(self.nb_colonne):
                    if (ind, "col") not in self.dico_cout_pot and self.prob_transp[sommet][ind] != 0:
                        self.dico_cout_pot[(ind, "col")] = self.cout[sommet][ind] - self.dico_cout_pot[(sommet, type_sommet)]
                        en_cours.append((ind, "col"))
            else:
                for ind in range(self.nb_ligne):
                    if (ind, "ligne") not in self.dico_cout_pot and self.prob_transp[ind][sommet] != 0:
                        self.dico_cout_pot[(ind, "ligne")] = self.cout[ind][sommet] - self.dico_cout_pot[(sommet, type_sommet)]
                        en_cours.append((ind, "ligne"))
        for ind_ligne in range(self.nb_ligne):
            for ind_col in range(self.nb_colonne):
                self.mat_cout_pot[ind_ligne][ind_col] = self.dico_cout_pot[(ind_ligne, "ligne")] + self.dico_cout_pot[(ind_col, "col")]
        if verbose:
            self.affichage_cout_potentiel()
    
    def affichage_cout_potentiel(self):
        pass
    
    def calcul_cout_marginaux(self, verbose = True):
        for ind_ligne in range(self.nb_ligne):
            for ind_colonne in range(self.nb_colonne):
                self.mat_cout_marg[ind_ligne][ind_colonne] = self.cout[ind_ligne][ind_colonne] - self.mat_cout_pot[ind_ligne][ind_colonne]
        if verbose:
            self.affichage_cout_marginaux()
            print(self.mat_cout_marg)  
    
    def affichage_cout_marginaux(self):
        pass    
        
        