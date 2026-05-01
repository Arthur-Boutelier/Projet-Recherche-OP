from ProblemeTransport import *
import time
import csv
import copy
import gc
import os  # 👈 Nouveau module nécessaire pour vérifier le fichier

def lancer_benchmark():
    tab_n = [10, 40, 100, 400, 1000, 4000, 10000]
    nom_fichier = "benchmark_resultats.csv"
    fichier_existe = os.path.isfile(nom_fichier) and os.path.getsize(nom_fichier) > 0

    with open(nom_fichier, mode='a', newline='', encoding='utf-8') as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=';')
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
            for _ in range(100): 
                print(f"\n--- Génération de la matrice {n}x{n} ---")
                Pb_base = ProblemeTransport.create_random_pb(n, n)
                
                res = {
                    "N": n,
                    "t_nw": None, "cout_nw_init": None, "t_nw_mp": None, "cout_nw_final": None,
                    "t_h": None, "cout_h_init": None, "t_h_mp": None, "cout_h_final": None
                }
                
                # ==========================================
                # RUN 1 : NORD-WEST + MARCHEPIED
                # ==========================================
                Pb_NW = copy.deepcopy(Pb_base)
                gc.collect()
                t0 = time.perf_counter()
                Pb_NW.nord_west()
                t1 = time.perf_counter()
                res["t_nw"] = round(t1 - t0, 4)
                res["cout_nw_init"] = Pb_NW.calcul_cout_tot()
                if n < 4000:
                    t2 = time.perf_counter()
                    Pb_NW.marche_pied_potentiel(verbose=False, partial=True) 
                    t3 = time.perf_counter()
                    
                    res["t_nw_mp"] = round(t3 - t2, 4)
                    res["cout_nw_final"] = Pb_NW.calcul_cout_tot()
                    print(f"NW terminé (Init: {res['t_nw']}s | MP: {res['t_nw_mp']}s)")
                else:
                    print(f"NW Marchepied ignoré pour N={n}")
                
                del Pb_NW
                
                # ==========================================
                # RUN 2 : BALAS-HAMMER + MARCHEPIED
                # ==========================================
                Pb_H = copy.deepcopy(Pb_base)
                gc.collect()
                t0 = time.perf_counter()
                Pb_H.hammer(verbose=False)
                t1 = time.perf_counter()
                res["t_h"] = round(t1 - t0, 4)
                res["cout_h_init"] = Pb_H.calcul_cout_tot()
                t2 = time.perf_counter()
                Pb_H.marche_pied_potentiel(verbose=False, partial=True)
                t3 = time.perf_counter()
                res["t_h_mp"] = round(t3 - t2, 4)
                res["cout_h_final"] = Pb_H.calcul_cout_tot()
                print(f"Hammer terminé (Init: {res['t_h']}s | MP: {res['t_h_mp']}s)")    
                del Pb_H
                
                # --- SAUVEGARDE DE LA LIGNE DANS LE FICHIER ---
                writer.writerow([
                    res["N"],
                    res["t_nw"], res["cout_nw_init"], res["t_nw_mp"], res["cout_nw_final"],
                    res["t_h"], res["cout_h_init"], res["t_h_mp"], res["cout_h_final"]
                ])
                fichier_csv.flush() 

    print("\n Benchmark terminé ! Les données ont été ajoutées.")