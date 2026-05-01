from ProblemeTransport import *
import time
import csv
import copy
import gc
import os  # 👈 Nouveau module nécessaire pour vérifier le fichier

def lancer_benchmark():
    """
    Fonction principale de benchmarking.
    Elle génère des matrices de tailles variées, applique les algorithmes,
    mesure les temps d'exécution et sauvegarde les coûts dans un fichier CSV[cite: 5].
    """
    # Tailles de matrices carrées à tester (N x N)
    tab_n = [10, 40, 100, 400, 1000, 4000, 10000]
    nom_fichier = "benchmark_resultats.csv"
    
    # Vérification si le fichier existe déjà et n'est pas vide pour l'en-tête
    fichier_existe = os.path.isfile(nom_fichier) and os.path.getsize(nom_fichier) > 0

    # Ouverture du fichier en mode 'append' (ajout)
    with open(nom_fichier, mode='a', newline='', encoding='utf-8') as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=';')
        
        # Si le fichier est nouveau, on écrit les en-têtes des colonnes
        if not fichier_existe:
            writer.writerow([
                "Taille_N", 
                "Temps_NordWest", "Cout_NW_Initial", 
                "Temps_NW_MarchePied", "Cout_NW_Final",
                "Temps_Hammer", "Cout_Hammer_Initial", 
                "Temps_Hammer_MarchePied", "Cout_Hammer_Final"
            ])
            
        print(f"Début du benchmark")
        for n in tab_n:
            # On effectue 100 tests par taille pour lisser les résultats statistiques[cite: 5]
            for _ in range(100): 
                print(f"\n--- Génération de la matrice {n}x{n} ---")
                # Création du problème de base aléatoire
                Pb_base = ProblemeTransport.create_random_pb(n, n)
                
                # Initialisation du dictionnaire de résultats pour cette itération
                res = {
                    "N": n,
                    "t_nw": None, "cout_nw_init": None, "t_nw_mp": None, "cout_nw_final": None,
                    "t_h": None, "cout_h_init": None, "t_h_mp": None, "cout_h_final": None
                }
                
                # ==========================================
                # RUN 1 : NORD-WEST + MARCHEPIED
                # ==========================================
                # Copie profonde pour ne pas altérer la matrice de base
                Pb_NW = copy.deepcopy(Pb_base)
                gc.collect() # Appel explicite au ramasse-miettes pour libérer la RAM
                
                t0 = time.perf_counter()
                Pb_NW.nord_west() # Application de l'heuristique initiale
                t1 = time.perf_counter()
                
                res["t_nw"] = round(t1 - t0, 4)
                res["cout_nw_init"] = Pb_NW.calcul_cout_tot()
                
                # Optimisation Marchepied : ignorée au-delà de 4000 pour NW car trop coûteuse[cite: 5]
                if n < 4000:
                    t2 = time.perf_counter()
                    Pb_NW.marche_pied_potentiel(verbose=False, partial=True) 
                    t3 = time.perf_counter()
                    
                    res["t_nw_mp"] = round(t3 - t2, 4)
                    res["cout_nw_final"] = Pb_NW.calcul_cout_tot()
                    print(f"NW terminé (Init: {res['t_nw']}s | MP: {res['t_nw_mp']}s)")
                else:
                    print(f"NW Marchepied ignoré pour N={n}")
                
                del Pb_NW # Suppression de l'objet pour vider la mémoire
                
                # ==========================================
                # RUN 2 : BALAS-HAMMER + MARCHEPIED
                # ==========================================
                Pb_H = copy.deepcopy(Pb_base)
                gc.collect()
                
                t0 = time.perf_counter()
                Pb_H.hammer(verbose=False) # Application de l'heuristique de Hammer[cite: 5]
                t1 = time.perf_counter()
                
                res["t_h"] = round(t1 - t0, 4)
                res["cout_h_init"] = Pb_H.calcul_cout_tot()
                
                # Optimisation Marchepied sur la solution de Hammer
                t2 = time.perf_counter()
                Pb_H.marche_pied_potentiel(verbose=False, partial=True)
                t3 = time.perf_counter()
                
                res["t_h_mp"] = round(t3 - t2, 4)
                res["cout_h_final"] = Pb_H.calcul_cout_tot()
                print(f"Hammer terminé (Init: {res['t_h']}s | MP: {res['t_h_mp']}s)")    
                del Pb_H
                
                # --- SAUVEGARDE DES RÉSULTATS DANS LE FICHIER ---
                writer.writerow([
                    res["N"],
                    res["t_nw"], res["cout_nw_init"], res["t_nw_mp"], res["cout_nw_final"],
                    res["t_h"], res["cout_h_init"], res["t_h_mp"], res["cout_h_final"]
                ])
                # Flush pour forcer l'écriture sur disque et ne pas perdre de données en cas de crash
                fichier_csv.flush() 

    print("\n Benchmark terminé ! Les données ont été ajoutées.")