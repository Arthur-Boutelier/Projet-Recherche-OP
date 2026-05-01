from collections import deque
from random import randint
import heapq
import gc
from tabulate import tabulate

class ProblemeTransport():
    """
    Classe représentant un problème de transport.
    Contient les données (coûts, provisions, commandes) et les algorithmes de résolution.
    """
    def __init__(self, nb_ligne, nb_colonne):
        """Initialisation des structures de données de base."""
        # Matrice des coûts de transport de la source i vers la destination j
        self.cout = [[0 for _ in range(nb_colonne)] for _ in range(nb_ligne)]
        # Stocks disponibles pour chaque source
        self.provision = [0 for _ in range(nb_ligne)]
        # Besoins exprimés par chaque destination
        self.commande = [0 for _ in range(nb_colonne)]
        self.nb_ligne = nb_ligne
        self.nb_colonne = nb_colonne
        # Dictionnaire pour stocker les potentiels duaux (u_i et v_j)
        self.dico_cout_pot = {}
        self.init_prob_transp()

    @staticmethod
    def charger_fichier(doc):
        """Méthode statique pour charger un problème à partir d'un fichier texte."""
        with open(str("data/" + doc),'r', encoding="utf-8") as fichier:
            tab_ligne = fichier.readlines()
            # La première ligne contient les dimensions N M
            ligne_0 = tab_ligne[0].strip().split(" ")
            Pb = ProblemeTransport(int(ligne_0[0]), int(ligne_0[1]))
            tab_ligne = tab_ligne[1:]
            
            # Nettoyage et conversion des données du fichier en entiers
            for indice_ligne in range(len(tab_ligne)):
                tab_ligne[indice_ligne] = tab_ligne[indice_ligne].strip().split()
                tab_ligne[indice_ligne] = [int(element) for element in tab_ligne[indice_ligne]]
            
            # Extraction des coûts (lignes 0 à N-1)
            Pb.cout = tab_ligne[:Pb.nb_ligne]
            Pb.cout = [element[:Pb.nb_colonne] for element in Pb.cout]
            # La dernière ligne contient les commandes
            Pb.commande = tab_ligne[-1]
            # La dernière colonne de chaque ligne de coût contient la provision associée
            Pb.provision = [element[-1] for element in tab_ligne[:-1]]
            
            Pb.init_prob_transp()
            return Pb

    def init_prob_transp(self):
        """Initialise le dictionnaire de graphe biparti pour stocker les flux."""
        self.prob_transp = {}
        # Création des entrées pour chaque ligne et chaque colonne
        for ind_ligne in range(self.nb_ligne):
            self.prob_transp[(ind_ligne, "ligne")] = {}
        for ind_colonne in range(self.nb_colonne):
            self.prob_transp[(ind_colonne, "col")] = {}

    def affichage_initial(self, max_cols=20):
        """Affiche les données d'entrée sous forme de grille tabulée."""
        # Gestion de l'affichage tronqué si trop de colonnes
        if self.nb_colonne <= max_cols:
            cols_indices = list(range(self.nb_colonne))
            headers = [f"C{j}" for j in cols_indices]
        else:
            demi = max_cols // 2
            cols_indices = list(range(demi)) + ["..."] + list(range(self.nb_colonne - demi, self.nb_colonne))
            headers = [f"C{j}" if j != "..." else "..." for j in cols_indices]
        
        headers = ["Source"] + headers + ["Prov."]
        table = []
        # Construction des lignes de la table
        for i in range(self.nb_ligne):
            row = [f"L{i}"]
            if self.nb_colonne <= max_cols:
                row.extend(self.cout[i])
            else:
                demi = max_cols // 2
                row.extend(self.cout[i][:demi])
                row.append("...")
                row.extend(self.cout[i][-demi:])
            row.append(self.provision[i])
            table.append(row)
            
        # Ajout de la ligne des commandes (besoins)
        cmd_row = ["Cmd"]
        if self.nb_colonne <= max_cols:
            cmd_row.extend(self.commande)
        else:
            demi = max_cols // 2
            cmd_row.extend(self.commande[:demi])
            cmd_row.append("...")
            cmd_row.extend(self.commande[-demi:])
        cmd_row.append(sum(self.provision)) # Affichage du total
        table.append(cmd_row)
        print(tabulate(table, headers=headers, tablefmt="grid"))
    
    def affichage_solution(self, max_cols=10):
        """Affiche les affectations de flux et calcule le coût total de la solution."""
        if self.nb_colonne <= max_cols:
            cols_indices = list(range(self.nb_colonne))
        else:
            demi = max_cols // 2
            cols_indices = list(range(demi)) + ["..."] + list(range(self.nb_colonne - demi, self.nb_colonne))
            
        headers = ["Source"] + [f"Dest {j}" if j != "..." else "..." for j in cols_indices] + ["Total Ligne"]
        table = []
        for i in range(self.nb_ligne):
            row = [f"Source {i}"]
            total_ligne_calcule = 0
            for j in cols_indices:
                if j == "...":
                    row.append("...")
                    continue
                # Récupération de la quantité affectée dans le graphe biparti
                quantite = self.prob_transp[(i, "ligne")].get(j, ".")
                if quantite != ".":
                    total_ligne_calcule += quantite
                    if quantite > 0:
                        row.append(f"{quantite} (c={self.cout[i][j]})")
                    else:
                        row.append(f"ε (c={self.cout[i][j]})")
                else:
                    row.append(".")
            row.append(total_ligne_calcule)
            table.append(row)
            
        # Pied de tableau avec les totaux par colonnes
        footer = ["Total Col"]
        for j in cols_indices:
            if j == "...":
                footer.append("...")
                continue
            total_col = sum(self.prob_transp[(j, "col")].values())
            footer.append(total_col)
        footer.append("-")
        table.append(footer)
        print(tabulate(table, headers=headers, tablefmt="grid"))
        print(f"\nCoût total de cette solution : {self.calcul_cout_tot()}\n\n")
        
    def nord_west(self):
        """Algorithme du Coin Nord-Ouest : affectation séquentielle de haut en bas et de gauche à droite."""
        self.init_prob_transp()
        ligne = 0
        colonne = 0
        restant_ligne = self.provision.copy()
        restant_colonne = self.commande.copy()
        
        while (ligne < self.nb_ligne) and (colonne < self.nb_colonne):
            # On affecte le maximum possible entre l'offre (provision) et la demande (commande)
            if restant_colonne[colonne] < restant_ligne[ligne]:
                valeur = restant_colonne[colonne]
                self.prob_transp[(colonne, "col")][ligne] = valeur
                self.prob_transp[(ligne, "ligne")][colonne] = valeur
                restant_colonne[colonne] -= valeur
                restant_ligne[ligne] -= valeur
                colonne +=1 # Demande saturée, on passe à la destination suivante
            elif restant_colonne[colonne] > restant_ligne[ligne]:
                valeur = restant_ligne[ligne]
                self.prob_transp[(colonne, "col")][ligne] = valeur
                self.prob_transp[(ligne, "ligne")][colonne] = valeur
                restant_colonne[colonne] -= valeur
                restant_ligne[ligne] -= valeur
                ligne += 1 # Offre épuisée, on passe à la source suivante
            elif restant_ligne[ligne] == restant_colonne[colonne]:
                valeur = restant_ligne[ligne]
                self.prob_transp[(colonne, "col")][ligne] = valeur
                self.prob_transp[(ligne, "ligne")][colonne] = valeur
                restant_colonne[colonne] -= valeur
                restant_ligne[ligne] -= valeur
                ligne += 1
                colonne += 1

    def hammer(self, verbose=True):
        """Algorithme de Balas-Hammer (Approximation de Vogel) : minimise les coûts en priorisant les pénalités."""
        if verbose:
            print("Résolution avec Balas-Hammer")
        self.init_prob_transp()
        
        # Ensembles pour suivre les lignes et colonnes non encore saturées
        set_ind_ligne_poss = {i for i in range(self.nb_ligne)}
        set_ind_col_poss = {j for j in range(self.nb_colonne)}
        
        # Initialisation des tas (Priority Queues) pour extraire rapidement les deux coûts minimaux
        heaps_lignes = {}
        for i in range(self.nb_ligne):
            ligne_donnees = [(self.cout[i][j], j) for j in range(self.nb_colonne)]
            ligne_donnees.sort()
            # On ne garde qu'une partie pour optimiser la mémoire sur de très grandes matrices
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
        type_last = None # Optimisation pour ne recalculer que les pénalités impactées
        
        while len(set_ind_ligne_poss) != 0 and len(set_ind_col_poss) != 0:
            # Calcul des deltas (différence entre les deux coûts les plus bas)
            if type_last is None or type_last == "col":
                delta_ligne = []
                for ind_ligne in set_ind_ligne_poss:
                    delta_ligne.append(self.calcul_delta_hammer_ligne(ind_ligne, set_ind_col_poss, heaps_lignes))
            if type_last is None or type_last == "ligne":
                delta_colonne = []  
                for ind_col in set_ind_col_poss:
                    delta_colonne.append(self.calcul_delta_hammer_colonne(ind_col, set_ind_ligne_poss, heaps_colonnes))
            
            # Recherche de la pénalité maximale pour agir prioritairement dessus
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
                # Affichage des pénalités max et du choix de l'arête
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
            
            # Affectation du flux sur l'arête choisie et mise à jour des structures
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
                
            # Nettoyage des listes de deltas pour la prochaine itération
            if type_last is None or type_last == "ligne":
                delta_ligne = [element for element in delta_ligne if element[1] != min_delta[1]]
            if type_last is None or type_last == "col":
                delta_colonne = [element for element in delta_colonne if element[2] != min_delta[2]]
                
    
    def calcul_delta_hammer_ligne(self, ligne, colonnes_poss, heaps_lignes):
        """Calcule l'écart entre les deux meilleurs coûts pour une ligne."""
        heap = heaps_lignes[ligne]
        # Nettoyage du tas pour ignorer les colonnes déjà saturées
        while heap and heap[0][1] not in colonnes_poss:
            heapq.heappop(heap)
        # Si le tas est vide, on doit le recharger avec les colonnes restantes
        if not heap:
            self.recharger_heap_ligne(ligne, heaps_lignes, colonnes_poss)
            heap = heaps_lignes[ligne]
            
        cout_min_1, ind_min_1 = heapq.heappop(heap)
        
        while heap and heap[0][1] not in colonnes_poss:
            heapq.heappop(heap)
            
        if not heap:
            # Cas où il ne reste qu'une seule colonne possible
            if len(colonnes_poss) == 1:
                heapq.heappush(heap, (cout_min_1, ind_min_1))
                return cout_min_1, ligne, ind_min_1, "ligne"
            else:
                self.recharger_heap_ligne(ligne, heaps_lignes, colonnes_poss)
                heap = heaps_lignes[ligne]
                heap.pop()
                
        cout_min_2, ind_min_2 = heapq.heappop(heap)
        # On remet les éléments dans le tas pour ne pas les perdre
        heapq.heappush(heap, (cout_min_1, ind_min_1))
        heapq.heappush(heap, (cout_min_2, ind_min_2))
        
        delta = cout_min_2 - cout_min_1 # Pénalité si on ne prend pas le min
        return delta, ligne, ind_min_1, "ligne"
                
    
    def calcul_delta_hammer_colonne(self, colonne, lignes_poss, heaps_colonnes):
        """Calcule l'écart entre les deux meilleurs coûts pour une colonne."""
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
        """Recharge les données du tas d'une ligne pour continuer le calcul de pénalité."""
        nouvelle_liste = []
        for j in range(self.nb_colonne):
            if j in colonnes_poss:
                nouvelle_liste.append((self.cout[ligne][j], j))
        nouvelle_liste.sort()
        nouveau_heap = nouvelle_liste[:500]
        heapq.heapify(nouveau_heap)
        heaps_lignes[ligne] = nouveau_heap
    
    def recharger_heap_colonne(self, colonne, heaps_colonnes, lignes_poss):
        """Recharge les données du tas d'une colonne."""
        nouvelle_liste = []
        for i in range(self.nb_ligne):
            if i in lignes_poss:
                nouvelle_liste.append((self.cout[i][colonne], i))
        nouvelle_liste.sort()
        nouveau_heap = nouvelle_liste[:500]
        heapq.heapify(nouveau_heap)
        heaps_colonnes[colonne] = nouveau_heap
        
        
    def calcul_cout_tot(self):
        """Calcule le coût global de la solution actuelle (Somme de Flux * Coût unitaire)."""
        cout_tot = 0
        for ligne in range(self.nb_ligne):
            for colonne, valeur in self.prob_transp[(ligne, "ligne")].items():
                cout_tot += valeur * self.cout[ligne][colonne]
        return cout_tot
    
    def detection_cycle(self, verbose = True):
        """Utilise un parcours en largeur (BFS) pour détecter un cycle dans le graphe des flux."""
        parents = {(0, "ligne") : None}
        sommets_en_cours = deque([(0, "ligne", None)])
        
        while sommets_en_cours:
            sommet, type_sommet, parent = sommets_en_cours.popleft()
            for sommet_suivant in self.prob_transp[(sommet, type_sommet)]:
                if sommet_suivant != parent:
                    # Inversion du type de sommet (ligne <-> colonne) car le graphe est biparti
                    if type_sommet == "ligne":
                        voisin = (sommet_suivant, "col")
                    else:
                        voisin = (sommet_suivant, "ligne")
                        
                    # Si le voisin est déjà dans les parents, on a bouclé le cycle
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
        """Reconstruit la séquence des sommets formant le cycle à partir du dictionnaire des parents."""
        chemin_fin = [noeud_fin]
        chemin_boucle = [noeud_boucle]
        # On remonte l'arbre depuis les deux sommets jusqu'à la racine commune
        courant = noeud_fin
        while parents[courant] != None:
            courant = parents[courant]
            chemin_fin.append(courant)
        courant = noeud_boucle
        while parents[courant] != None:
            courant = parents[courant]
            chemin_boucle.append(courant)
        
        # Suppression de la partie commune au début des chemins (tronc commun de l'arbre)
        while len(chemin_boucle) > 1 and len(chemin_fin) > 1 and chemin_fin[-2] == chemin_boucle[-2]:
            chemin_boucle.pop()
            chemin_fin.pop()
        
        chemin_fin.reverse()
        chemin_tot = chemin_fin + chemin_boucle[:-1]
        chemin_point = []
        precedent = None
        # Transformation des sommets (ligne/col) en coordonnées de cases (i, j)
        for sommet in chemin_tot:
            if precedent is not None:
                if sommet[1] == "ligne":
                    chemin_point.append((sommet[0],precedent[0]))
                else:
                    chemin_point.append((precedent[0],sommet[0]))
            precedent = sommet
            
        # Fermeture du cycle
        if chemin_tot[0][1] == "ligne":
            chemin_point.append((chemin_point[0][0], chemin_point[-1][1]))
        else:
            chemin_point.append((chemin_point[-1][0], chemin_point[0][1]))
        return chemin_point
    
    @staticmethod
    def affichage_cycle(cycle):
        """Affiche les points du cycle sur la console."""
        print("Cycle détecté")
        print("Le cycle est composé des points :")
        print(cycle[0], end=" ")
        for element in cycle[1:]:
            print(f"=> {element}", end= " ")
        print("\n")
                
                
    @staticmethod
    def affichage_sous_graphe(tab_graphe):
        """Affiche les composantes connexes si le graphe n'est pas encore totalement lié."""
        if len(tab_graphe) != 1:
            print(f"Dans ce graphe on observe {len(tab_graphe)} sous-graphes connexes :\n")
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
        else:
            print("La proposition fournie est connexe nous passons donc à l'étape suivante\n")
    
    def est_connexe(self, verbose=True):
        """Utilise un parcours BFS pour identifier toutes les composantes connexes du graphe."""
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
        """
        Détermine les variables duales u_i et v_j (potentiels) pour l'optimisation.
        Utilise la règle : u_i + v_j = cout[i][j] pour toutes les cases de la base.
        """
        if verbose:
            print("\nCalcul des coûts potentiels")
            print("On initialise le potentiel de la ligne 0 à 0")
            
        self.dico_cout_pot = {(0, "ligne"): 0} # Fixation arbitraire d'un potentiel à 0
        en_cours = deque([(0, "ligne")])
        
        while len(self.dico_cout_pot) != (self.nb_colonne + self.nb_ligne) and en_cours:
            sommet, type_sommet = en_cours.popleft()
            type_suivant = "ligne" if type_sommet == "col" else "col"
            for sommet_suivant in self.prob_transp[(sommet, type_sommet)]:
                if (sommet_suivant, type_suivant) not in self.dico_cout_pot:
                    # Calcul du potentiel manquant par soustraction
                    if type_sommet == "ligne":
                        self.dico_cout_pot[(sommet_suivant, type_suivant)] = self.cout[sommet][sommet_suivant] - self.dico_cout_pot[(sommet, type_sommet)]
                    else:
                        self.dico_cout_pot[(sommet_suivant, type_suivant)] = self.cout[sommet_suivant][sommet] - self.dico_cout_pot[(sommet, type_sommet)]
                    en_cours.append((sommet_suivant, type_suivant))
        if verbose:
            self.affichage_cout_potentiel()
            
    def affichage_cout_potentiel(self, max_display=15):
        """Affiche les vecteurs de potentiels et la matrice complète u+v."""
        def obtenir_indices(nb, max_d):
            if nb <= max_d:
                return list(range(nb))
            demi = max_d // 2
            return list(range(demi)) + ["..."] + list(range(nb - demi, nb))
            
        indices_u = obtenir_indices(self.nb_ligne, max_display)
        indices_v = obtenir_indices(self.nb_colonne, max_display)
        
        print("\nPotentiel des lignes:")
        u_vals = [self.dico_cout_pot.get((i, "ligne"), "ø") if i != "..." else "..." for i in indices_u]
        print(tabulate([u_vals], headers=[f"u{i}" if i != "..." else "..." for i in indices_u], tablefmt="grid"))
        
        print("\nPotentiel des colonnes:")
        v_vals = [self.dico_cout_pot.get((j, "col"), "ø") if j != "..." else "..." for j in indices_v]
        print(tabulate([v_vals], headers=[f"v{j}" if j != "..." else "..." for j in indices_v], tablefmt="grid"))
        
        print("\nMatrice des Coûts Potentiels: ")
        headers_mat = ["u \\ v"] + [f"v{j}" if j != "..." else "..." for j in indices_v]
        table_mat = []
        for i in indices_u:
            if i == "...":
                table_mat.append(["..."] * (len(indices_v) + 1))
                continue
            u_i = self.dico_cout_pot.get((i, "ligne"), 0)
            row = [f"u{i}"]
            for j in indices_v:
                if j == "...":
                    row.append("...")
                    continue
                v_j = self.dico_cout_pot.get((j, "col"), 0)
                # Somme des potentiels duaux
                row.append(u_i + v_j)
            table_mat.append(row)
        print(tabulate(table_mat, headers=headers_mat, tablefmt="grid"))
        print("\n")
    
    def calcul_min_cout_marginaux(self, ligne_start = 0, verbose = True, partial = False):
        """
        Calcule les coûts marginaux : Delta_ij = Coût - (u_i + v_j).
        Une valeur négative indique une opportunité d'amélioration.
        """
        min_marg = (float("inf"), (None,None))
        pot_cols = [self.dico_cout_pot[(j, "col")] for j in range(self.nb_colonne)]
        
        if verbose:
            self.affichage_cout_marginaux()
            
        if ligne_start is None:
            ligne_start = 0
            
        for offset in range(self.nb_ligne):
            ind_ligne = (offset + ligne_start) % self.nb_ligne
            pot_ligne = self.dico_cout_pot[(ind_ligne, "ligne")]
            couts_ligne = self.cout[ind_ligne]
            for ind_colonne in range(self.nb_colonne):
                # Formule du coût marginal
                cout_marg = couts_ligne[ind_colonne] - (pot_ligne + pot_cols[ind_colonne])
                if cout_marg < min_marg[0]:
                    min_marg = (cout_marg,(ind_ligne,ind_colonne))
                    # Optimisation partial : arrêt précoce si gain suffisant trouvé
                    if partial and self.lim_partial is not None and min_marg[0] < self.lim_partial:
                        return min_marg
        if partial:
            self.lim_partial = min_marg[0]//2
        return min_marg
    
    def affichage_cout_marginaux(self, max_display=20):
        """Affiche la grille des écarts à l'optimalité."""
        print("Calcul des coûts marginaux")
        print("\nMatrice des Coûts Marginaux:")
        if self.nb_colonne <= max_display:
            cols_indices = list(range(self.nb_colonne))
        else:
            demi = max_display // 2
            cols_indices = list(range(demi)) + ["..."] + list(range(self.nb_colonne - demi, self.nb_colonne))
            
        headers = ["Pot."] + [f"v{j}" if j != "..." else "..." for j in cols_indices]
        table = []
        if self.nb_ligne <= max_display:
            lignes_indices = list(range(self.nb_ligne))
        else:
            demi = max_display // 2
            lignes_indices = list(range(demi)) + ["..."] + list(range(self.nb_ligne - demi, self.nb_ligne))
            
        for i in lignes_indices:
            if i == "...":
                table.append(["..."] * (len(cols_indices) + 1))
                continue
            u_i = self.dico_cout_pot.get((i, "ligne"), 0)
            row = [f"u{i}"]
            for j in cols_indices:
                if j == "...":
                    row.append("...")
                    continue
                v_j = self.dico_cout_pot.get((j, "col"), 0)
                delta_ij = self.cout[i][j] - (u_i + v_j)
                row.append(delta_ij)
            table.append(row)
        print(tabulate(table, headers=headers, tablefmt="grid"))
    
    @staticmethod
    def create_random_pb(nb_ligne, nb_colonne):
        """Méthode utilitaire générant un problème aléatoire équilibré."""
        Pb = ProblemeTransport(nb_ligne, nb_colonne)
        for ind_ligne in range(nb_ligne):
            for ind_colonne in range(nb_colonne):
                val_cout = randint(1,100)
                val_temp = randint(1,100)
                Pb.cout[ind_ligne][ind_colonne] = val_cout
                # On équilibre l'offre et la demande globalement
                Pb.commande[ind_colonne] += val_temp
                Pb.provision[ind_ligne] += val_temp
        return Pb
    
    def marche_pied_potentiel(self, verbose = True, partial = False):
        """
        Algorithme de Stepping-Stone (Marchepied) par la méthode des potentiels.
        Itère jusqu'à ce que tous les coûts marginaux soient >= 0.
        """
        iteration = 1
        marg_min = (-float("inf"), (None,None))
        self.lim_partial = None
        while marg_min[0] < 0:
            if verbose:
                print(f"Itération {iteration}\n")
                iteration +=1
                print("Solution actuelle:")
                self.affichage_solution()
            
            # Étape 1 : Si un cycle a été créé par l'ajout d'une arête, on le sature pour éliminer une arête
            presence_cycle, cycle = self.detection_cycle(verbose = verbose)
            if presence_cycle:
                self.maximisation_cycle(cycle, marg_min[1], verbose = verbose)
            else:
                if verbose:
                    print("aucun cycle détecté nous passons donc à l'étape suivante\n")
            
            # Étape 2 : S'assurer que le graphe est connexe pour calculer les potentiels duaux
            if marg_min[1][0] is None:
                est_connexe, tab_sous_graphe = self.est_connexe(verbose = verbose)
                if not est_connexe:
                    self.rendre_connexe(tab_sous_graphe)
            
            # Étape 3 : Calculer les potentiels u et v basés sur la solution actuelle
            self.calcul_cout_potentiel(verbose = verbose)
            
            # Étape 4 : Chercher l'arête qui minimise le coût marginal
            marg_min = self.calcul_min_cout_marginaux(ligne_start = marg_min[1][0],verbose = verbose, partial = partial)
            
            # Étape 5 : Si amélioration possible, on ajoute l'arête à la base (flux de 0 initialement)
            if marg_min[0] < 0:
                self.prob_transp[(marg_min[1][0], "ligne")][marg_min[1][1]] = 0
                self.prob_transp[(marg_min[1][1], "col")][marg_min[1][0]] = 0
                if verbose:
                    print(f"On ajoute l'arête {marg_min[1]} car elle possède un coût potentiel de {marg_min[0]}\n\n")
            else:
                print("Aucune arête améliorante détectée on stop donc l'algorithme\n\n")

        

    def maximisation_cycle(self, cycle, arete_depart, verbose = True):
        """
        Optimise le flux le long d'un cycle fermé.
        On ajoute Delta aux sommets pairs et on retranche Delta aux sommets impairs du cycle.
        """
        i = 0
        tab_del = []
        i = cycle.index(arete_depart)
        cycle = cycle[i:] + cycle[:i]
        delta = float("inf")
        
        # Déterminer la valeur maximale de Delta (le flux minimum des arêtes sortantes)
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
            
        # Mise à jour des flux
        for ind_sommet in range(len(cycle)):
            sommet = cycle[ind_sommet]
            if ind_sommet % 2:
                # Retrait de flux
                self.prob_transp[(sommet[0], "ligne")][sommet[1]] -= delta
                self.prob_transp[(sommet[1], "col")][sommet[0]] -= delta
                if verbose:
                    print(f"{sommet} (-{delta})", end=" ")
            else:
                # Ajout de flux
                self.prob_transp[(sommet[0], "ligne")][sommet[1]] += delta
                self.prob_transp[(sommet[1], "col")][sommet[0]] += delta
                if verbose:
                    print(f"{sommet} (+{delta})", end=" ")
            if ind_sommet != len(cycle)-1:
                if verbose:
                    print(f"=>", end=" ")
 
        sommet = tab_del[0] # Arête saturée à supprimer de la base
        if verbose:
            print(f"\nOn supprime donc l'arête : {tab_del[0]}\n")
        del self.prob_transp[(sommet[0], "ligne")][sommet[1]]
        del self.prob_transp[(sommet[1], "col")][sommet[0]] 
        

    def rendre_connexe(self, tab_sous_graphe, verbose = True):
        """
        Relie les composantes connexes isolées en ajoutant des arêtes à flux nul.
        C'est nécessaire pour gérer la dégénérescence dans l'algorithme des potentiels.
        """
        graphe_construit = set(tab_sous_graphe.pop(0))
        lignes_restantes = {i for i in range(self.nb_ligne) if (i, "ligne") not in graphe_construit}
        cols_restantes = {j for j in range(self.nb_colonne) if (j, "col") not in graphe_construit}
        
        while tab_sous_graphe:
            min_arete = (float("inf"), None)
            # Recherche de l'arête la moins chère pour lier deux composantes
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
                            
            # Ajout de l'arête de liaison avec un flux de 0
            self.prob_transp[(min_arete[1][0],"ligne")][min_arete[1][1]] = 0
            self.prob_transp[(min_arete[1][1],"col")][min_arete[1][0]] = 0
            nouveau_sommet = (min_arete[1][0], "ligne") if (min_arete[1][0], "ligne") not in graphe_construit else (min_arete[1][1], "col")
            
            if verbose:
                print(f"On ajoute donc l'arête {min_arete[1]} afin de rendre le graphe connexe\n")
                
            # Mise à jour des ensembles de sommets restants
            for i in range(len(tab_sous_graphe)):
                if nouveau_sommet in tab_sous_graphe[i]:
                    sous_graphe_trouve = tab_sous_graphe[i]      
                    graphe_construit.update(sous_graphe_trouve)
                    lignes_restantes -= {s[0] for s in sous_graphe_trouve if s[1] == "ligne"}
                    cols_restantes -= {s[0] for s in sous_graphe_trouve if s[1] == "col"}
                    tab_sous_graphe.pop(i)
                    break