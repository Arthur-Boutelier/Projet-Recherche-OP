

def somme_ligne(dico, indice):
    resultat = 0
    for valeur in dico[(indice, "ligne")].values():
        resultat += valeur
    return resultat
        
    
def somme_colonne(dico,indice):
    resultat = 0
    for valeur in dico[(indice, "col")].values():
        resultat += valeur
    return resultat 
            
        


        
        