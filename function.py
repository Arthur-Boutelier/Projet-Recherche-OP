
def somme_ligne(matrice,indice):
    resultat = 0
    for nombre in matrice[indice]:
        resultat += nombre
    return nombre
    
def somme_colonne(matrice,indice):
    resultat = 0
    for ligne in matrice:
        resultat += ligne[indice]
    return resultat 
