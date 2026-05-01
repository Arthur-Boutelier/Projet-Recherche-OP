from ProblemeTransport import *
from pathlib import Path
import time
import Benchmark

en_cours = True
# Boucle principale de l'application
while en_cours :
    selection = False
    # Boucle de sélection du problème (chargement ou génération)
    while not selection:
        resultat = input("Veuillez choisir le numéro du problème à traiter ou rentrer -1 pour créer un problème aléatoire: ")
        
        # Option : Génération aléatoire
        if resultat == "-1":
            dimension_choisie = False
            while not dimension_choisie:
                nb_ligne = input("Veuillez entrer le nombre de ligne: ")
                nb_colonne = input("Veuillez entrer le nombre de colonne: ")
                
                # Validation de la saisie (doit être numérique)
                if not (nb_ligne.isdigit() and nb_colonne.isdigit()):
                    print("Erreur dans la saisie de vos valeurs veuillez recommencer: ")
                else:
                    print(f"Génération d'un Problème de transport aléatoire de taille {nb_ligne} x {nb_colonne}")
                    dimension_choisie = True
                    # Instanciation via la méthode statique de génération aléatoire[cite: 6, 7]
                    Pb = ProblemeTransport.create_random_pb(int(nb_ligne),int(nb_colonne))
                    selection = True
                    
        # Option : Chargement d'un fichier existant
        elif resultat.isdigit():
            chemin = Path(f"data/{resultat}.txt")
            if chemin.exists():
                print(f"Génération du problème de transport N°{resultat}:")
                Pb = ProblemeTransport.charger_fichier(f"{resultat}.txt")
                selection = True
            else:
                print("Fichier introuvable veuillez réessayer")
        else:
            print("Saisie non reconnue veuillez réessayer")
            
    # Affichage de la matrice des coûts et des contraintes initiales
    print("Affichage du Problème initial :")
    Pb.affichage_initial()
    
    selection = False
    # Choix de l'algorithme de résolution initiale
    while not selection:
        resultat = input("\n\nVeuillez choisir l'algoritme utilisé pour résoudre ce problème (0:Nord-West,1:Ballas-Hammer): \n")
        
        if resultat == "0":
            print("Vous avez choisi la méthode de Nord-West\nApplication de l'algorithme :\n")
            temps_debut = time.perf_counter()
            Pb.nord_west() # Lancement NW[cite: 6, 7]
            temps_fin = time.perf_counter()
            print("Résultat obtenu:\n")
            Pb.affichage_solution()
            print(f"\nMéthode de Nord-West terminée en {temps_fin - temps_debut}s\n\n")
            selection = True
            
        elif resultat == "1":
            print("Vous avez choisi la méthode de Ballas-Hammer\nApplication de l'algorithme :")
            temps_debut = time.perf_counter()
            Pb.hammer() # Lancement Balas-Hammer[cite: 6, 7]
            temps_fin = time.perf_counter()
            print("Résultat obtenu:\n")
            Pb.affichage_solution()
            print(f"Méthode de Ballas-Hammer terminée en {temps_fin - temps_debut}s\n\n")
            selection = True
        else:
            print("Erreur lors de la saisie veuillez recommencer")
            
    selection = False
    # Étape d'optimisation (Marchepied / Stepping-Stone)
    while not selection:
        resultat = input("Entrez y lorsque vous êtes prêt pour le marchepied: ")
        if resultat == "y":
            print("\n")
            selection = True
        else:
            print("Erreur dans la saisie veuillez recommencer")
            
    # Mesure du temps pour l'algorithme du Marchepied
    temps_debut = time.perf_counter()
    Pb.marche_pied_potentiel(verbose=True) # Appel de la méthode d'optimisation
    temps_fin = time.perf_counter()
    
    print("Résultat obtenu:\n")
    Pb.affichage_solution()
    print(f"Méthode du marchepied terminée en {temps_fin-temps_debut}s\n\n")
    
    selection = False
    # Demande de relance du programme
    while not selection:
        resultat = input("Voulez vous essayer un autre problème? (y/n)")
        if resultat == "y":
            selection = True
        elif resultat == "n":
            en_cours = False # Arrêt de la boucle principale
        else:
            print("Erreur lors de votre saisie veuillez réessayer")