from function import *
from collections import deque
from random import randint
import heapq
import gc


class ProblemeTransport():
    def __init__(self, nb_ligne, nb_colonne):
        self.cout = [[0 for _ in range(nb_colonne)] for _ in range(nb_ligne)]
        self.provision = [0 for _ in range(nb_ligne)]
        self.commande = [0 for _ in range(nb_colonne)]
        self.nb_ligne = nb_ligne
        self.nb_colonne = nb_colonne
        self.dico_cout_pot = {}
        self.init_prob_transp()


    @staticmethod
    def charger_fichier(doc):
        with open(str("data/" + doc),'r', encoding="utf-8") as fichier:
            tab_ligne = fichier.readlines()
            ligne_0 = tab_ligne[0].strip()
            ligne_0 = ligne_0.split(" ")
            Pb = ProblemeTransport(int(ligne_0[0]), int(ligne_0[1]))
            tab_ligne = tab_ligne[1:]
            for indice_ligne in range(len(tab_ligne)):
                tab_ligne[indice_ligne] = tab_ligne[indice_ligne].strip()
                tab_ligne[indice_ligne] = tab_ligne[indice_ligne].split()
                tab_ligne[indice_ligne] = [int(element) for element in tab_ligne[indice_ligne]]
            Pb.cout = tab_ligne[:Pb.nb_ligne]
            Pb.cout = [element[:Pb.nb_colonne] for element in Pb.cout]
            Pb.commande = tab_ligne[-1]
            Pb.provision = [element[-1] for element in tab_ligne[:-1]]
            Pb.init_prob_transp()
            return Pb

    def init_prob_transp(self):
        self.prob_transp = {}
        for ind_ligne in range(self.nb_ligne):
            self.prob_transp[(ind_ligne, "ligne")] = {}
        for ind_colonne in range(self.nb_colonne):
            self.prob_transp[(ind_colonne, "col")] = {}
        
    def nord_west(self):
        self.init_prob_transp()
        ligne = 0
        colonne = 0
        restant_ligne = self.provision.copy()
        restant_colonne = self.commande.copy()
        while (ligne < self.nb_ligne) and (colonne < self.nb_colonne):
            if restant_colonne[colonne] < restant_ligne[ligne]:
                valeur = restant_colonne[colonne]
                self.prob_transp[(colonne, "col")][ligne] = valeur
                self.prob_transp[(ligne, "ligne")][colonne] = valeur
                restant_colonne[colonne] -= valeur
                restant_ligne[ligne] -= valeur
                colonne +=1
            elif restant_colonne[colonne] > restant_ligne[ligne]:
                valeur = restant_ligne[ligne]
                self.prob_transp[(colonne, "col")][ligne] = valeur
                self.prob_transp[(ligne, "ligne")][colonne] = valeur
                restant_colonne[colonne] -= valeur
                restant_ligne[ligne] -= valeur
                ligne += 1
            elif restant_ligne[ligne] == restant_colonne[colonne]:
                valeur = restant_ligne[ligne]
                self.prob_transp[(colonne, "col")][ligne] = valeur
                self.prob_transp[(ligne, "ligne")][colonne] = valeur
                restant_colonne[colonne] -= valeur
                restant_ligne[ligne] -= valeur
                ligne += 1
                colonne+=1

    def hammer(self, verbose=True):
        if verbose:
            print("Résolution avec Balas-Hammer")
        self.init_prob_transp()
        set_ind_ligne_poss = {i for i in range(self.nb_ligne)}
        set_ind_col_poss = {j for j in range(self.nb_colonne)}
        heaps_lignes = {}
        for i in range(self.nb_ligne):
            ligne_donnees = [(self.cout[i][j], j) for j in range(self.nb_colonne)]
            ligne_donnees.sort()
            ligne_donnees = ligne_donnees[:self.nb_ligne//10]
            heapq.heapify(ligne_donnees)
            heaps_lignes[i] = ligne_donnees
            del ligne_donnees
            if i%1000 ==0:
                gc.collect
        heaps_colonnes = {}
        for j in range(self.nb_colonne):
            ligne_donnees = [(self.cout[i][j], i) for i in range(self.nb_ligne)]
            ligne_donnees.sort()
            ligne_donnees = ligne_donnees[:self.nb_colonne//10]
            heapq.heapify(ligne_donnees)
            heaps_colonnes[j] = ligne_donnees
            del ligne_donnees
            if j%1000 == 0:
                gc.collect
        gc.collect
        iteration = 1
        restant_ligne = self.provision.copy()
        restant_colonne = self.commande.copy()
        type_last = None
        while len(set_ind_ligne_poss) != 0 and len(set_ind_col_poss) != 0:
            if type_last is None or type_last == "col":
                delta_ligne = []
                for ind_ligne in set_ind_ligne_poss:
                    delta_ligne.append(self.calcul_delta_hammer_ligne(ind_ligne, set_ind_col_poss, heaps_lignes))
            if type_last is None or type_last == "ligne":
                delta_colonne = []  
                for ind_col in set_ind_col_poss:
                    delta_colonne.append(self.calcul_delta_hammer_colonne(ind_col, set_ind_ligne_poss, heaps_colonnes))
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
            prov_poss = restant_ligne[min_delta[1]]
            com_poss = restant_colonne[min_delta[2]]
            if prov_poss < com_poss:
                self.prob_transp[(min_delta[1], "ligne")][min_delta[2]] = prov_poss
                self.prob_transp[(min_delta[2], "col")][min_delta[1]] = prov_poss
                set_ind_ligne_poss.remove(min_delta[1])
                restant_ligne[min_delta[1]] -= prov_poss
                restant_colonne[min_delta[2]] -= prov_poss
                type_last = "ligne"
            elif prov_poss > com_poss:
                self.prob_transp[(min_delta[1], "ligne")][min_delta[2]] = com_poss
                self.prob_transp[(min_delta[2], "col")][min_delta[1]] = com_poss
                set_ind_col_poss.remove(min_delta[2])
                restant_ligne[min_delta[1]] -= com_poss
                restant_colonne[min_delta[2]] -= com_poss
                type_last = "col"
            else:
                self.prob_transp[(min_delta[1], "ligne")][min_delta[2]] = prov_poss
                self.prob_transp[(min_delta[2], "col")][min_delta[1]] = prov_poss
                set_ind_ligne_poss.remove(min_delta[1])
                set_ind_col_poss.remove(min_delta[2])
                restant_ligne[min_delta[1]] -= prov_poss
                restant_colonne[min_delta[2]] -= prov_poss
                type_last = None
            if type_last is None or type_last == "ligne":
                delta_ligne = [element for element in delta_ligne if element[1] != min_delta[1]]
            if type_last is None or type_last == "col":
                delta_colonne = [element for element in delta_colonne if element[2] != min_delta[2]]
                
            
        
    
    
    def calcul_delta_hammer_ligne(self, ligne, colonnes_poss, heaps_lignes):
        heap = heaps_lignes[ligne]
        while heap and heap[0][1] not in colonnes_poss:
            heapq.heappop(heap)
        if not heap:
            self.recharger_heap_ligne(ligne, heaps_lignes, colonnes_poss)
            heap = heaps_lignes[ligne]
        cout_min_1, ind_min_1 = heapq.heappop(heap)
        while heap and heap[0][1] not in colonnes_poss:
            heapq.heappop(heap)
        if not heap:
            if len(colonnes_poss) == 1:
                heapq.heappush(heap, (cout_min_1, ind_min_1))
                return cout_min_1, ligne, ind_min_1, "ligne"
            else:
                self.recharger_heap_ligne(ligne, heaps_lignes, colonnes_poss)
                heap = heaps_lignes[ligne]
                heap.pop()
        cout_min_2, ind_min_2 = heapq.heappop(heap)
        heapq.heappush(heap, (cout_min_1, ind_min_1))
        heapq.heappush(heap, (cout_min_2, ind_min_2))
        delta = cout_min_2 - cout_min_1
        return delta, ligne, ind_min_1, "ligne"
                
    
    def calcul_delta_hammer_colonne(self, colonne, lignes_poss, heaps_colonnes):
        heap = heaps_colonnes[colonne]
        while heap and heap[0][1] not in lignes_poss:
            heapq.heappop(heap)
        if not heap:
            self.recharger_heap_colonne(colonne, heaps_colonnes, lignes_poss)
            heap = heaps_colonnes[colonne]
        cout_min_1, ind_min_1 = heapq.heappop(heap)
        while heap and heap[0][1] not in lignes_poss:
            heapq.heappop(heap)
        if not heap:
            if len(lignes_poss) == 1:
                heapq.heappush(heap, (cout_min_1, ind_min_1))
                return cout_min_1, ind_min_1 ,colonne, "col"
            else:
                self.recharger_heap_colonne(colonne, heaps_colonnes, lignes_poss)
                heap = heaps_colonnes[colonne]
                heap.pop()
        cout_min_2, ind_min_2 = heapq.heappop(heap)
        heapq.heappush(heap, (cout_min_1, ind_min_1))
        heapq.heappush(heap, (cout_min_2, ind_min_2))
        delta = cout_min_2 - cout_min_1
        return delta, ind_min_1, colonne, "col"
    
    def recharger_heap_ligne(self, ligne, heaps_lignes, colonnes_poss):
        nouvelle_liste = []
        for j in range(self.nb_colonne):
            if j in colonnes_poss:
                nouvelle_liste.append((self.cout[ligne][j], j))
        nouvelle_liste.sort()
        nouveau_heap = nouvelle_liste[:500]
        heapq.heapify(nouveau_heap)
        heaps_lignes[ligne] = nouveau_heap
    
    def recharger_heap_colonne(self, colonne, heaps_colonnes, lignes_poss):
        nouvelle_liste = []
        for i in range(self.nb_ligne):
            if i in lignes_poss:
                nouvelle_liste.append((self.cout[i][colonne], i))
        nouvelle_liste.sort()
        nouveau_heap = nouvelle_liste[:500]
        heapq.heapify(nouveau_heap)
        heaps_colonnes[colonne] = nouveau_heap
        
        
    def calcul_cout_tot(self):
        cout_tot = 0
        for ligne in range(self.nb_ligne):
            for colonne, valeur in self.prob_transp[(ligne, "ligne")].items():
                cout_tot += valeur * self.cout[ligne][colonne]
        return cout_tot
    
    def detection_cycle(self, verbose = True):
        parents = {(0, "ligne") : None}
        sommets_en_cours = deque([(0, "ligne", None)])
        while sommets_en_cours:
            sommet, type_sommet, parent = sommets_en_cours.popleft()
            for sommet_suivant in self.prob_transp[(sommet, type_sommet)]:
                if sommet_suivant != parent:
                    if type_sommet == "ligne":
                        voisin = (sommet_suivant, "col")
                    else:
                        voisin = (sommet_suivant, "ligne")
                    if voisin in parents:
                        cycle = ProblemeTransport.recreation_cycle(parents, (sommet,type_sommet), voisin)
                        if verbose:
                            ProblemeTransport.affichage_cycle(cycle)
                        return True, cycle
                    parents[voisin] = (sommet,type_sommet)
                    sommets_en_cours.append((voisin[0], voisin[1], sommet))
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
        chemin_tot = chemin_fin + chemin_boucle[:-1]
        chemin_point = []
        precedent = None
        for sommet in chemin_tot:
            if precedent is not None:
                if sommet[1] == "ligne":
                    chemin_point.append((sommet[0],precedent[0]))
                else:
                    chemin_point.append((precedent[0],sommet[0]))
            precedent = sommet
        if chemin_tot[0][1] == "ligne":
            chemin_point.append((chemin_point[0][0], chemin_point[-1][1]))
        else:
            chemin_point.append((chemin_point[-1][0], chemin_point[0][1]))
        return chemin_point
    
    @staticmethod
    def affichage_cycle(cycle):
        print("Le cycle est composé des points :")
        print(cycle[0], end=" ")
        for element in cycle[1:]:
            print(f"=> {element}", end= " ")
        print()
                
                
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
                    type_suivant = "col"
                else:
                    type_suivant = "ligne"
                for sommet_suivant in self.prob_transp[(sommet, type_sommet)]:
                    if (sommet_suivant, type_suivant) not in sous_graphe_en_cours:
                        sommets_en_cours.append((sommet_suivant, type_suivant))
                        sous_graphe_en_cours.add((sommet_suivant, type_suivant))
                        sommets_restant.discard((sommet_suivant, type_suivant))
            liste_graphes.append(sous_graphe_en_cours)
        if verbose:
            ProblemeTransport.affichage_sous_graphe(liste_graphes)
        return len(liste_graphes) == 1, liste_graphes
            
            
    def calcul_cout_potentiel(self, verbose = True):
        if verbose:
            print("On initialise le cout potentielle de la ligne 0 à 0")
        self.dico_cout_pot = {(0, "ligne"): 0}
        en_cours = deque([(0, "ligne")])
        while len(self.dico_cout_pot) != (self.nb_colonne + self.nb_ligne) and en_cours:
            sommet, type_sommet = en_cours.popleft()
            type_suivant = "ligne" if type_sommet == "col" else "col"
            for sommet_suivant in self.prob_transp[(sommet, type_sommet)]:
                if (sommet_suivant, type_suivant) not in self.dico_cout_pot:
                    if type_sommet == "ligne":
                        self.dico_cout_pot[(sommet_suivant, type_suivant)] = self.cout[sommet][sommet_suivant] - self.dico_cout_pot[(sommet, type_sommet)]
                    else:
                        self.dico_cout_pot[(sommet_suivant, type_suivant)] = self.cout[sommet_suivant][sommet] - self.dico_cout_pot[(sommet, type_sommet)]
                    en_cours.append((sommet_suivant, type_suivant))
        if verbose:
            self.affichage_cout_potentiel()
            
    def affichage_cout_potentiel(self):
        pass
    
    def calcul_min_cout_marginaux(self, ligne_start = 0, verbose = True, partial = False):
        min_marg = (float("inf"), (None,None))
        pot_cols = [self.dico_cout_pot[(j, "col")] for j in range(self.nb_colonne)]
        if ligne_start is None:
            ligne_start = 0
        for offset in range(self.nb_ligne):
            ind_ligne = (offset + ligne_start) % self.nb_ligne
            pot_ligne = self.dico_cout_pot[(ind_ligne, "ligne")]
            couts_ligne = self.cout[ind_ligne]
            for ind_colonne in range(self.nb_colonne):
                cout_marg = couts_ligne[ind_colonne] - (pot_ligne + pot_cols[ind_colonne])
                if cout_marg < min_marg[0]:
                    min_marg = (cout_marg,(ind_ligne,ind_colonne))
                    if partial and self.lim_partial is not None and min_marg[0] < self.lim_partial:
                        return min_marg
        if partial:
            self.lim_partial = min_marg[0]//2
        return min_marg
    
    def affichage_cout_marginaux(self):
        pass
    
    @staticmethod
    def create_random_pb(nb_ligne, nb_colonne):
        Pb = ProblemeTransport(nb_ligne, nb_colonne)
        for ind_ligne in range(nb_ligne):
            for ind_colonne in range(nb_colonne):
                val_cout = randint(1,100)
                val_temp = randint(1,100)
                Pb.cout[ind_ligne][ind_colonne] = val_cout
                Pb.commande[ind_colonne] += val_temp
                Pb.provision[ind_ligne] += val_temp
        return Pb
    
    def marche_pied_potentiel(self, verbose = True, partial = False):
        marg_min = (-float("inf"), (None,None))
        self.lim_partial = None
        while marg_min[0] < 0:
            presence_cycle, cycle = self.detection_cycle(verbose = verbose)
            if presence_cycle:
                self.maximisation_cycle(cycle, marg_min[1], verbose = verbose)
            if marg_min[1][0] is None:
                est_connexe, tab_sous_graphe = self.est_connexe(verbose = verbose)
                if not est_connexe:
                    self.rendre_connexe(tab_sous_graphe)
            self.calcul_cout_potentiel(verbose = verbose)
            marg_min = self.calcul_min_cout_marginaux(ligne_start = marg_min[1][0],verbose = verbose, partial = partial)
            if marg_min[0] < 0:
                self.prob_transp[(marg_min[1][0], "ligne")][marg_min[1][1]] = 0
                self.prob_transp[(marg_min[1][1], "col")][marg_min[1][0]] = 0
                if verbose:
                    print(f"On ajoute l'arêtes {marg_min[1]} car elle possède un coût potentielle de {marg_min[0]}")

        

    def maximisation_cycle(self, cycle, arete_depart, verbose = True):
        i = 0
        tab_del = []
        i = cycle.index(arete_depart)
        cycle = cycle[i:] + cycle[:i]
        delta = float("inf")
        for j in range(len(cycle)//2):
            sommet = cycle[j*2+1]
            cout_sommet = self.prob_transp[(sommet[0], "ligne")][sommet[1]]
            if delta > cout_sommet:
                tab_del = [sommet]
                delta = cout_sommet
            elif delta == cout_sommet:
                tab_del.append(sommet)
        if verbose:
            print("Début de la maximisation du cycle :")
        for ind_sommet in range(len(cycle)):
            sommet = cycle[ind_sommet]
            if ind_sommet % 2:
                self.prob_transp[(sommet[0], "ligne")][sommet[1]] -= delta
                self.prob_transp[(sommet[1], "col")][sommet[0]] -= delta
                if verbose:
                    print(f"{sommet} (-{delta})", end=" ")
            else:
                self.prob_transp[(sommet[0], "ligne")][sommet[1]] += delta
                self.prob_transp[(sommet[1], "col")][sommet[0]] += delta
                if verbose:
                    print(f"{sommet} (+{delta})", end=" ")
            if ind_sommet != len(cycle)-1:
                if verbose:
                    print(f"=>", end=" ")
 
        sommet = tab_del[0]
        if verbose:
            print(f"\nOn supprime donc l'arête' : {tab_del[0]}")
        del self.prob_transp[(sommet[0], "ligne")][sommet[1]]
        del self.prob_transp[(sommet[1], "col")][sommet[0]] 
        

    def rendre_connexe(self, tab_sous_graphe):
        graphe_construit = set(tab_sous_graphe.pop(0))
        lignes_restantes = {i for i in range(self.nb_ligne) if (i, "ligne") not in graphe_construit}
        cols_restantes = {j for j in range(self.nb_colonne) if (j, "col") not in graphe_construit}
        while tab_sous_graphe:
            min_arete = (float("inf"), None)
            for sommet in graphe_construit:
                if sommet[1] == "ligne":
                    for ind_colonne in cols_restantes:
                        cout = self.cout[sommet[0]][ind_colonne]
                        if cout < min_arete[0]:
                            min_arete = (cout,(sommet[0], ind_colonne))
                else:
                    for ind_ligne in lignes_restantes:
                        cout = self.cout[ind_ligne][sommet[0]]
                        if cout < min_arete[0]:
                            min_arete = (cout,(ind_ligne, sommet[0]))
            self.prob_transp[(min_arete[1][0],"ligne")][min_arete[1][1]] = 0
            self.prob_transp[(min_arete[1][1],"col")][min_arete[1][0]] = 0
            nouveau_sommet = (min_arete[1][0], "ligne") if (min_arete[1][0], "ligne") not in graphe_construit else (min_arete[1][1], "col")
            for i in range(len(tab_sous_graphe)):
                if nouveau_sommet in tab_sous_graphe[i]:
                    sous_graphe_trouve = tab_sous_graphe[i]      
                    graphe_construit.update(sous_graphe_trouve)
                    lignes_restantes -= {s[0] for s in sous_graphe_trouve if s[1] == "ligne"}
                    cols_restantes -= {s[0] for s in sous_graphe_trouve if s[1] == "col"}
                    tab_sous_graphe.pop(i)
                    break
         
        
        