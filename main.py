from ProblemeTransport import *
from pathlib import Path
import time
import Benchmark
en_cours = True
while en_cours :
    selection = False
    while not selection:
        resultat = input("Veuillez choisir le numéro du problème à traiter ou rentrer -1 pour créer un problème aléatoire: ")
        if resultat == "-1":
            dimension_choisie = False
            while not dimension_choisie:
                nb_ligne = input("Veuillez entrer le nombre de ligne: ")
                nb_colonne = input("Veuillez entrer le nombre de colonne: ")
                if not (nb_ligne.isdigit() and nb_colonne.isdigit()):
                    print("Erreur dans la saisie de vos valeurs veuillez recommencer: ")
                else:
                    print(f"Génération d'un Problème de transport aléatoire de taille {nb_ligne} x {nb_colonne}")
                    dimension_choisie = True
                    Pb = ProblemeTransport.create_random_pb(int(nb_ligne),int(nb_colonne))
                    selection = True
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
    print("Affichage du Problème initial :")
    Pb.affichage_initial()
    selection = False
    while not selection:
        resultat = input("\n\nVeuillez choisir l'algoritme utilisé pour résoudre ce problème (0:Nord-West,1:Ballas-Hammer): \n")
        if resultat == "0":
            print("Vous avez choisie la méthode de Nord-West\nApplication de l'algorithme :\n")
            temps_debut = time.perf_counter()
            Pb.nord_west()
            temps_fin = time.perf_counter()
            print("Résultat obtenue:\n")
            Pb.affichage_solution()
            print(f"\nMéthode de Nord-West terminé en {temps_fin - temps_debut}s\n\n")
            selection = True
        elif resultat == "1":
            print("Vous avez choisie la méthode de Ballas-Hammer\nApplication de l'algorithme :")
            temps_debut = time.perf_counter()
            Pb.hammer()
            temps_fin = time.perf_counter()
            print("Résultat obtenue:\n")
            Pb.affichage_solution()
            print(f"Méthode de Ballas-Hammer terminé en {temps_fin - temps_debut}s\n\n")
            selection = True
        else:
            print("Erreur lors de la saisie veuillez recommencez")
    selection = False
    while not selection:
        resultat = input("Entrez y lorsque vous êtes prêt pour le marchepied: ")
        if resultat == "y":
            print("\n")
            selection = True
        else:
            print("Erreur dans la saisie veuillez recommencer")
    temps_debut = time.perf_counter()
    Pb.marche_pied_potentiel(verbose=True)
    temps_fin = time.perf_counter()
    print("Résultat obtenue:\n")
    Pb.affichage_solution()
    print(f"Méthode du marchepied terminé en {temps_fin-temps_debut}s\n\n")
    selection = False
    while not selection:
        resultat = input("Voulez vous essayer un autre problème? (y/n)")
        if resultat == "y":
            selection = True
        elif resultat == "n":
            en_cours = False
        else:
            print("erreur lors de votre saisie veuillez réessayer")

    


