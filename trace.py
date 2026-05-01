import sys
import os
from contextlib import redirect_stdout
from ProblemeTransport import ProblemeTransport
GROUPE = "1"
EQUIPE = "6" 

def generer_toutes_les_traces():
    """
    Parcourt les 12 problèmes, exécute les résolutions et 
    sauvegarde les sorties console dans des fichiers .txt.
    """
    # Création du dossier pour stocker les traces
    dossier_traces = "traces_rendu"
    if not os.path.exists(dossier_traces):
        os.makedirs(dossier_traces)

    print(f"Début de la génération des traces pour le Groupe {GROUPE}, Équipe {EQUIPE}...")

    for i in range(1, 13):
        nom_base = f"{i}.txt"
        
        # Vérification si le fichier existe dans data/
        if not os.path.exists(f"data/{nom_base}"):
            print(f"Fichier data/{nom_base} introuvable, passage au problème suivant.")
            continue

        # --- CAS 1 : NORD-OUEST (NO) ---
        pb_no = ProblemeTransport.charger_fichier(nom_base)
        nom_fichier_no = f"{dossier_traces}/{GROUPE}-{EQUIPE}-trace{i}-no.txt"
        
        with open(nom_fichier_no, 'w', encoding='utf-8') as f:
            with redirect_stdout(f):
                print(f"=== TRACE D'EXÉCUTION : PROBLÈME {i} (NORD-OUEST) ===")
                print("\n[ÉTAPES INITIALES]")
                pb_no.affichage_initial()
                
                print("\n[RÉSOLUTION INITIALE : NORD-OUEST]")
                pb_no.nord_west()
                pb_no.affichage_solution()
                
                print("\n[DÉROULÉ DU MARCHEPIED AVEC POTENTIEL]")
                # L'entièreté des tableaux et informations est gérée par verbose=True
                pb_no.marche_pied_potentiel(verbose=True)
                
                print("\n[RÉSULTAT FINAL OPTIMAL]")
                pb_no.affichage_solution()

        # --- CAS 2 : BALAS-HAMMER (BH) ---
        pb_bh = ProblemeTransport.charger_fichier(nom_base)
        nom_fichier_bh = f"{dossier_traces}/{GROUPE}-{EQUIPE}-trace{i}-bh.txt"
        
        with open(nom_fichier_bh, 'w', encoding='utf-8') as f:
            with redirect_stdout(f):
                print(f"=== TRACE D'EXÉCUTION : PROBLÈME {i} (BALAS-HAMMER) ===")
                print("\n[ÉTAPES INITIALES]")
                pb_bh.affichage_initial()
                
                print("\n[RÉSOLUTION INITIALE : BALAS-HAMMER]")
                # On affiche le détail des pénalités (Hammer verbose)
                pb_bh.hammer(verbose=True)
                pb_bh.affichage_solution()
                
                print("\n[DÉROULÉ DU MARCHEPIED AVEC POTENTIEL]")
                pb_bh.marche_pied_potentiel(verbose=True)
                
                print("\n[RÉSULTAT FINAL OPTIMAL]")
                pb_bh.affichage_solution()

        print(f"Problème {i} : Traces NO et BH générées avec succès.")

    print(f"\nTerminé ! Les 24 fichiers sont dans le dossier '{dossier_traces}'.")

if __name__ == "__main__":
    generer_toutes_les_traces()