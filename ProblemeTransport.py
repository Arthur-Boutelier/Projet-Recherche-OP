from function import *


class ProblemeTransport():
    def __init__(self, nb_ligne, nb_colonne):
        self.cout = [[0 for _ in range(nb_colonne)] for _ in range(nb_ligne)]
        self.prob_transp = [[0 for _ in range(nb_colonne)] for _ in range(nb_ligne)]
        self.provision = [0 for _ in range(nb_ligne)]
        self.commande = [0 for _ in range(nb_colonne)]
        self.nb_ligne = nb_ligne
        self.nb_colonne = nb_colonne


    def __init__(self, doc):
        with open(str("data/" + doc),'r', encoding="utf-8") as fichier:
            tab_ligne = fichier.readlines()
            ligne_0 = tab_ligne[0].strip()
            ligne_0 = ligne_0.split(" ")
            self.nb_ligne = int(ligne_0[0])
            self.nb_colonne = int(ligne_0[1])
            tab_ligne = tab_ligne[1::]
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

    def hammer(self, verbose=False):
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

        
        