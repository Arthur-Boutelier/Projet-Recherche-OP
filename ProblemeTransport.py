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
        while (ligne != self.nb_ligne - 1) or (colonne != self.nb_colonne - 1 ):
            print(ligne, self.nb_ligne, colonne, self.nb_colonne)
            if ligne < self.nb_ligne:
                lim_ligne = self.provision[ligne] - somme_ligne(self.prob_transp, ligne)
            else:
                lim_ligne = float('inf')
            if colonne < self.nb_colonne:
                lim_colonne = self.commande[colonne] - somme_colonne(self.prob_transp, colonne)
            else:
                lim_colonne = float('inf')
            if lim_colonne < lim_ligne:
                self.prob_transp[ligne][colonne] = lim_colonne
                colonne +=1
            elif lim_colonne > lim_ligne:
                self.prob_transp[ligne][colonne] = lim_ligne
                ligne += 1
            elif lim_colonne == lim_ligne:
                self.prob_transp[ligne][colonne] = lim_colonne
                if ligne < self.nb_ligne:
                    ligne += 1
                if colonne < self.nb_colonne:
                    colonne += 1

    def hammer(self):
        self.prob_transp = [[0 for _ in range(self.nb_colonne)] for _ in range(self.nb_ligne)]
        tab_ind_ligne_poss = [i for i in range(self.nb_ligne)]
        tab_ind_col_poss = [i for i in range(self.nb_colonne)]
        while len(tab_ind_ligne_poss) != 0 and len(tab_ind_col_poss) != 0:
            delta_ligne = []
            delta_colonne = []
            for ind_ligne in tab_ind_ligne_poss:
                delta_ligne.append(self.calcul_delta_hammer_ligne(tab_ind_col_poss, ind_ligne))
            for ind_col in tab_ind_col_poss:
                delta_colonne.append(self.calcul_delta_hammer_colonne(tab_ind_ligne_poss, ind_col))
            min_delta = (float('inf'),)
            for delta in delta_ligne:
                if delta[0] < min_delta[0]:
                    min_delta = delta
                elif delta[0] == min_delta[0]:
                    if self.cout[min_delta[1]][min_delta[2]] > self.cout[delta[1]][delta[2]]:
                        min_delta = delta
            for delta in delta_colonne:
                if delta[0] < min_delta[0]:
                    min_delta = delta
                elif delta[0] == min_delta[0]:
                    if self.cout[min_delta[1]][min_delta[2]] > self.cout[delta[1]][delta[2]]:
                        min_delta = delta
            prov_poss = self.provision[min_delta[1]] - somme_ligne(self.prob_transp, min_delta[1])
            com_poss = self.commande[min_delta[2]] - somme_colonne(self.prob_transp, min_delta[2])
            print("passage\nmin_delta :", min_delta,"\nligne_poss : ", tab_ind_ligne_poss, "\ncol_poss : ", tab_ind_col_poss)
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
        print(self.prob_transp)
                
            
        
    
    
    def calcul_delta_hammer_ligne(self,tab_ind_poss, ligne):
        if len(tab_ind_poss) == 1:
            return self.cout[ligne][tab_ind_poss[0]], ligne, tab_ind_poss[0]
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
        return self.cout[ligne][tab_ind_poss[ind_min_2]] - self.cout[ligne][tab_ind_poss[ind_min_1]], ligne ,tab_ind_poss[ind_min_1]
        
    
    def calcul_delta_hammer_colonne(self,tab_ind_poss, colonne):
        if len(tab_ind_poss) == 1:
            return self.cout[tab_ind_poss[0]][colonne], tab_ind_poss[0], colonne
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
        return self.cout[tab_ind_poss[ind_min_2]][colonne] - self.cout[tab_ind_poss[ind_min_1]][colonne], tab_ind_poss[ind_min_1], colonne
        