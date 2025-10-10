# -*- coding: utf-8 -*-
import csv
import os

"""
=============================================
FONCTION 
=============================================
"""

             
#ouverture du fichier csv         
def charger_fich(fichier):
    """
    Charge un fichier CSV et retourne les lignes sous forme de liste.

    Args:
        fichier (str): Le chemin du fichier CSV à charger.

    Returns:
        list: Liste des lignes du fichier CSV.
    """
    with open(fichier,"r") as fich:
        lignes=list(csv.reader(fich, delimiter=";"))
    return lignes
#affichage des tableaux  
def affichage(nom,data):
    """
    Affiche un nombre spécifié de lignes d'un tableau sous forme tabulaire.

    Args:
        nom (str): Nom du tableau.
        data (list): Liste contenant les données du tableau.

    Returns:
        None
    """
    limit=int(input(f"Combien de ligne voulez-vous afficher dans le fichier {nom} ? : "))+1
    print("-"*50)
    print(f"{nom:^25}")
    print("-"*50)
    cpt=0
    for ligne in data :
        if cpt==limit:
            break
        else:
            print(f"{ligne[0]:6}|{ligne[1]:70}|{ligne[2]:20}|{ligne[3]:10}|{ligne[4]:15}") 
            print("_"*121)
            cpt += 1
def somme_modalite_sans_critere(data,variable_tableau,agregat_colonne,modalite):
    """
    Calcule la somme des valeurs d'une variable pour une modalité donnée.

    Args:
        data (list): Liste contenant les données.
        variable_tableau (str): Nom de la variable à afficher.
        agregat_colonne (str): Nom de la colonne ou on va additionner ses valeur.
        modalite (str): Modalité pour laquelle effectuer le calcul.

    Returns:
        int: Somme des valeurs pour la modalité sélectionnée.
    """
    somme=0
    indice_mod=Index_variable(data,variable_tableau)
    indice_fich=Index_variable(data,agregat_colonne)

    #somme des effectif et recrutement 
    for ligne in data[1:]:
        if ligne[indice_mod]==modalite:
            somme += int(ligne[indice_fich])
    return somme    

#création de tcd

def somme_modalité_avec_critere(data,var,crit,variable_tableau,agregat_colonne,modalite):
    """
    Calcule la somme des valeurs d'une variable pour une modalité après un filtrage.

    Args:
        data (list): Liste contenant les données.
        var (str): Nom de la variable à filtrer.
        crit (str): Critère de filtrage.
        variable_tableau (str): Nom de la variable à afficher.
        agregat_colonne (str):Nom de la colonne ou on va additionner ses valeur.
        modalite (str): Modalité pour laquelle effectuer le calcul.

    Returns:
        int: Somme des valeurs pour la modalité sélectionnée après filtrage.
    """
    somme=0
    nvl_data=extraire_un_critere(data,crit,var)

    indice_mod=Index_variable(data,variable_tableau)

    indice_fich=Index_variable(data,agregat_colonne)

    #somme des effectif et recrutement 
    for ligne in nvl_data[1:]:
        if ligne[indice_mod]==modalite:
            somme += int(ligne[indice_fich])
    return somme    


#fonction pour renommer les variable
def renommer_variables(liste_data):
    """
    Permet de renommer les colonnes d'un tableau.

    Args:
        liste_data (list): Liste contenant les colonnes du tableau.

    Returns:
        None
    """
    for i in range(len(liste_data[0])):
        print(f"\nL'ancien nom :'{liste_data[0][i]}'")
        new_name = input("le nouveau nom (laisser vide pour garder le même nom) : ")
        if new_name: 
            liste_data[0][i] = new_name

def repartition(agregat,modalite_ligne,chemin):

    critere_effec_h = extraire_un_critere(effectif_data, "homme",effectif_data[0][3])
    critere_effec_f = extraire_un_critere(effectif_data, "femme",effectif_data[0][3])
    critere_recru_h = extraire_un_critere(recrutement_data, "homme", effectif_data[0][3])
    critere_recru_f = extraire_un_critere(recrutement_data, "femme", effectif_data[0][3])
    titre_de_lagregat=agregat[0]
    titre_de_la_modalite= modalite_ligne[0]
    colonne_effectif=effectif_data[0][4]
    colonne_recrutement=recrutement_data[0][4]

    for modalité_de_la_repartition in agregat[1:]:
        tableau = [["métier", "effectif total", "effectif H", "effectif F", "Recrutement TOTAL", "Recrutement H", "Recrutement F"]]
        modalité_de_la_repartition=modalité_de_la_repartition.strip()
        for modalite in modalite_ligne[1:]:
            modalite = modalite.strip()
            # Partie effectif
            if modalité_de_la_repartition== "Manager de proximité":
                modalité_de_la_repartition="Manager de proximité, maitrise"        
            effec_tot = somme_modalité_avec_critere(effectif_data,titre_de_lagregat , modalité_de_la_repartition,titre_de_la_modalite, colonne_effectif, modalite)
            effec_h = somme_modalité_avec_critere(critere_effec_h,titre_de_lagregat, modalité_de_la_repartition, titre_de_la_modalite, colonne_effectif, modalite)
            effec_f = somme_modalité_avec_critere(critere_effec_f, titre_de_lagregat, modalité_de_la_repartition,titre_de_la_modalite, colonne_effectif, modalite)
            if modalité_de_la_repartition== "Manager de proximité, maitrise":
                modalité_de_la_repartition="Manager de proximité"
            # Partie recrutement
            recru_tot = somme_modalité_avec_critere(recrutement_data, titre_de_lagregat, modalité_de_la_repartition, titre_de_la_modalite, colonne_recrutement, modalite)
            recru_h = somme_modalité_avec_critere(critere_recru_h, titre_de_lagregat, modalité_de_la_repartition,titre_de_la_modalite, colonne_recrutement, modalite)
            recru_f = somme_modalité_avec_critere(critere_recru_f,titre_de_lagregat, modalité_de_la_repartition, titre_de_la_modalite, colonne_recrutement, modalite)
            
            tableau.append([modalite, effec_tot, effec_h, effec_f, recru_tot, recru_h, recru_f])
        exporter(tableau,f"EXPORT/STATISTIQUES/{chemin}/Repartition_{modalité_de_la_repartition}.csv")

def repartition_evolution(modalite_colonne,modalite_ligne,chemin,repartition_par_genre,data):
    if repartition_par_genre=="vide":
        tableau_evolution = [[["métier"]+ [les_annees[1:]]+["effectif moyen"]]]
        for modalite in modalite_ligne[1:]:
            ligne = []
            for colonne in modalite_colonne[1:]:
                critere_recru = extraire_un_critere(data, colonne, modalite_colonne[0])
                effec = somme_modalite_sans_critere(critere_recru,modalite_ligne[0], data[0][4], modalite)
                ligne.append(effec)            
        critere_moy = extraire_un_critere(data, modalite.strip(),data[0][1])
        moy = moyenne_variable(critere_moy, "effectif")
        tableau_evolution.append([modalite] + ligne + [round(moy,2)])
    else:
        tableau_evolution = [[["métier"]+[les_annees[1:]]+["effectif moyen"]]]
        for modalite in modalite_ligne[1:]:
            ligne = []
            for colonne in modalite_colonne[1:]:
                critere_recru = extraire_un_critere(effectif_data, colonne, effectif_data[0][0])
                effec = somme_modalité_avec_critere(critere_recru, effectif_data[0][3],repartition_par_genre,effectif_data[0][1], effectif_data[0][4], modalite)
                ligne.append(effec)
        critere_moy = extraire_deux_critere(effectif_data, effectif_data[0][1],modalite.strip(),effectif_data[0][3],repartition_par_genre)           
        moy = moyenne_variable(critere_moy, "effectif")
        tableau_evolution.append([modalite] + ligne + [round(moy,2)])
    exporter(tableau_evolution,f"EXPORT/STATISTIQUES/Evolution _effectif/{chemin}")
    
    
def menu():
    print("""=====================================================
          \nExploitation données effectifs et recrutement SNCF
          \n=====================================================
          \n\n------MENU GENERAL------
          \n1. Données : Description Globale (qualité & quantité)
          \n2. Visualisation : Affichage des données
          \n3. Extraction Données : Sélection des données et Exports
          \n4. Indicateurs & statistiques : Affichage / Exports Stat
          \n5. Vérification Résultats répartition Sexe : Affichage / Export (comparaison)
          \n0. FIN""")
    
def gestion(effectif_data, recrutement_data):
    """
    Gère l'intéraciton avec le menu principal.

    Args:
        effectif_data (list): Données des effectifs.
        recrutement_data (list): Données des recrutements.
    """
    while True:  # Boucle principale
        menu()  # Affichage du menu
        choix = input("Entrez le numéro de votre choix : ")

        if choix == "0":
            print("FIN du programme.")
            break

        elif choix == "1":
            print("\n-----------------Données : Description Globale--------------------")
            print(f"Nombre de variables dans effectif : {len(effectif_data[0])}")
            print(f"Nombre de lignes dans effectif : {len(effectif_data)}")
            print(f"Nombre de variables dans recrutement : {len(recrutement_data[0])}")
            print(f"Nombre de lignes dans recrutement : {len(recrutement_data)}")

        elif choix == "2":
            print("\n-----------------Visualisation : Affichage des données--------------------")
            affichage("Effectif", effectif_data)
            affichage("Recrutement", recrutement_data)

        elif choix == "3":
            print("\n-----------------Extraction Données--------------------")
            critere = input("Entrez le critère de filtrage (ex : '2020') : ")
            colonne = input("Entrez le nom de la colonne à filtrer (ex : 'Annee') : ")

            # Extraction des données pour critère
            extrait_effectif = extraire_un_critere(effectif_data, critere, colonne)
            extrait_recrutement = extraire_un_critere(recrutement_data, critere, colonne)

            # Exportation
            exporter(extrait_effectif, f"EXPORT/EXTRACTION/effectif_{critere}.csv")
            exporter(extrait_recrutement, f"EXPORT/EXTRACTION/recrutement_{critere}.csv")
            print(f"Données extraites et exportées pour le critère '{critere}'.")

        elif choix == "4":
            print("\n-----------------Indicateurs et Statistiques--------------------")
            print(f"Moyenne des effectifs : {moyenne_variable(effectif_data, 'effectif')}")
            print(f"Effectif maximum : {max_variable(effectif_data, 'effectif')}")
            print(f"Effectif minimum : {min_variable(effectif_data, 'effectif')}")
            print(f"Total des effectifs : {total_variable(effectif_data, 'effectif')}")

        elif choix == "5":
            print("\n-----------------Vérification Résultats Répartition Sexe--------------------")
            sexe = input("Entrez le sexe à vérifier (Homme/Femme) : ")
            extrait_effectif = extraire_un_critere(effectif_data, sexe,effectif_data[0][3])
            extrait_recrutement = extraire_un_critere(recrutement_data, sexe, recrutement_data[0][3])

            exporter(extrait_effectif, f"EXPORT/STATISTIQUES/{sexe}_effectif.csv")
            exporter(extrait_recrutement, f"EXPORT/STATISTIQUES/{sexe}_recrutement.csv")
            print(f"Données pour le sexe '{sexe}' exportées.")

        else:
            print("Choix invalide. Veuillez réessayer.")
            # Fonction pour obtenir l'index d'une clé dans un dictionnaire
def index_cle(dictionnaire, cle):
    """
    Retourne l'index d'une clé dans un dictionnaire.

    Args:
        dictionnaire (dict): Le dictionnaire à parcourir.
        cle (str): La clé dont on veut connaître l'index.

    Returns:
        int: L'index de la clé si elle existe, sinon -1.
    """
    try:
        return list(dictionnaire.keys()).index(cle)
    except ValueError:
        return -1
#retourne l'indice d'une variable    
def Index_variable(datalist,variable):
    """
    Retourne l'index correspondant à une variable dans les colonnes.

    Args:
        datalist (list): Liste contenant les données.
        variable (str): Nom de la variable.

    Returns:
        int: Index de la variable.
    """
    nom_var=datalist[0]
    i=0

    for var in nom_var:
        variable=variable.upper()
        var=var.upper()
        if var== variable:
            return i 
        else:
            i+=1
#retourne les valeur distinct
def les_modalites (data, variable_quali):
    """
    Retourne les valeurs distinctes d'une colonne donnée.

    Args:
        data (list): Liste contenant les données.
        variable_quali (str): Nom de la variable qualitative.

    Returns:
        list: Liste des modalités distinctes.
    """
    col=les_valeurs(variable_quali,data)  
    distinct = []
    for ligne in col:
        if ligne not in distinct:
            if ligne!="":
                distinct.append(ligne)
        
    return distinct
def repartition_genre_effectif(les_date,les_contrat,data_homme,data_femme,chemin):
    tableau_evolution = [[les_date[0],les_contrat[0],"Nombre d'homme","Nombre de femme"]]
    for annee in les_date[1:]:
        for contrat in les_contrats[1:]:
            crit_homme=extraire_deux_critere(data_homme,les_date[0],annee,les_contrats[0],contrat)
            crit_femme=extraire_deux_critere(data_femme,les_date[0],annee,les_contrats[0],contrat)
            effec_homme=total_variable(crit_homme,crit_homme[4])
            effec_femme=total_variable(crit_homme,crit_femme[4])  
            tableau_evolution.append(annee,contrat,effec_homme,effec_femme)    
    exporter(tableau_evolution,f"EXPORT/STATISTIQUES/Evolution _effectif/{chemin}")      
def exporter(dataliste, file):
    """
    La fonction exporte une liste dans un fichier csv
    Paramètres :
    liste : list
    nom_fichier : 
    """
    with open(file, "w", newline='') as fich:
        data=csv.writer(fich, delimiter = ";")
        data.writerows(dataliste)
        

def extraire_un_critere(data, critere, colonne):
    """_summary_

    Args:
        data (list): liste des donnee
        critere (str): critere
        colonne (int): numero de colonne

    Returns:
        _type_: list avec critere
    """
    data_crit = []  
    data_crit.append(data[0])
    num_col=Index_variable(data,colonne)
    for ligne in data[1:]:
   
            if ligne[num_col].strip().upper() == critere.strip().upper():
                data_crit.append(ligne)   
    if len(data_crit) == 1:
        print(f"Aucune modalite ne correspond au critère {critere} à la colonne {colonne}.")      
    return data_crit

def max_variable(data, variable_quanti):
    """
    Retourne la valeur maximale d'une variable quantitative.

    Args:
        data (list): Liste des données.
        variable_quanti (str): Nom de la variable quantitative.

    Returns:
        str: Valeur maximale trouvée.
    """
    datadevar=les_valeurs(variable_quanti,data)
    modalite=datadevar[1:]
    return max(modalite)

def  min_variable(data, variable_quanti):
    """
    Retourne la valeur minimale d'une variable quantitative.

    Args:
        data (list): Liste des données.
        variable_quanti (str): Nom de la variable quantitative.

    Returns:
        str: Valeur minimale trouvée.
    """
    datadevar=les_valeurs(variable_quanti,data)
    modalite=datadevar[1:]
    return min(modalite)

# retourne toutes les valeurs de la colonne variable
def les_valeurs(variable,data): 
    """
    Retourne toutes les valeurs d'une colonne donnée.

    Args:
        variable (str): Nom de la variable.
        data (list): Liste contenant les données.

    Returns:
        list: Liste des valeurs de la colonne.
    """
    indice=Index_variable(data,variable)
    col=[]
    for ligne in data:
        col.append(ligne[indice])
    return col

def moyenne_variable(data, variable_quanti):
    """
    Calcule la moyenne des valeurs d'une variable quantitative.

    Args:
        data (list): Liste des données.
        variable_quanti (str): Nom de la variable quantitative.

    Returns:
        float: Moyenne calculée.
    """
    datadevar=les_valeurs(variable_quanti,data)
    modalite=datadevar[1:]
    somme=0
    cpt=0
    
    for i in modalite:
        if i!="":
            somme=int(i)+somme
            cpt+=1
    if somme==0 or cpt==0:
        return 0 
    else :
        moyenne=somme/cpt   
        return moyenne     

def total_variable(data,variable_quanti):
    """
    Calcule la somme des valeurs d'une variable quantitative.

    Args:
        data (list): Liste des données.
        variable_quanti (str): Nom de la variable quantitative.

    Returns:
        int: Somme totale des valeurs.
    """
    datadevar=les_valeurs(variable_quanti,data)
    modalite=datadevar[1:]
    somme=0
    for i in modalite:
        if i!="":
            somme=int(i)+somme

    return somme
def extraire_deux_critere(data,var1,crit1,var2,crit2):
    data1=extraire_un_critere(data,crit1,var1)
    data2=extraire_un_critere(data1,crit2,var2)
    return data2

#retourne la data avec les critere      
def extraire_plus_criteres(data):
    """
    Permet de filtrer les données selon plusieurs critères.

    Args:
        data (list): Liste des données.

    Returns:
        list: Liste des données filtrées selon les critères.
    """
    variable=input("Quel est la variable voulez vous filtrer ? : ")
    critere=input("Quel critere voulez vous mettre ? : ")        
    data = extraire_un_critere(data,critere,variable)    
    ajtcrit=input("Voulez-vous ajouter un autre critère ? : ")    
    while ajtcrit.upper()=="OUI":
        variable=input("Quel est la variable voulez vous filtrer ? : ")
        critere=input("Quel critere voulez vous mettre ? : ")
        data = extraire_un_critere(data,critere,variable)    
    return data
def arborescence(chemin):
    chem=f"EXPORT/STATISTIQUES/{chemin}"
    os.makedirs(chem, exist_ok=True)
"""
===================================================================
PROGRAMME PRINCIPALE
===================================================================
"""

#***************************************************
# Lecture des fichiers effectifs & recrutements
#*************************************************** 
"""
effectif_data=charger_fich("DATA/effectif-metiers_sncf.csv")

nom_fich2="Effectifs des metiers chez sncf : "

recrutement_data=charger_fich("DATA/recrutement-metiers-sncf.csv")
nom_fich1="Recrutements des metiers chez sncf : "

#***************************************************
# Renommage des variables d'effectifs & recrutements
#***************************************************
print("="*25)
print(f"{"Fichier des effectif":25}")
print("="*25)
renommer_variables(effectif_data)
print("="*25)
print(f"{"Fichier des recrutements":25}")
print("="*25)
renommer_variables(recrutement_data)

#***************************************************
# Extraction par critères
#***************************************************
print("="*25)
print(f"{"Fichier des effectif":25}")
print("="*25)
resultat_crit_effec=extraire_plus_criteres(effectif_data)
print("="*25)
print(f"{"Fichier des recrutements":25}")
print("="*25)
resultat_crit_recru=extraire_plus_criteres(recrutement_data)
print("="*25)
print("Affichage avec critere ")
print("="*25)
affichage(nom_fich2,resultat_crit_effec)  
affichage(nom_fich1,resultat_crit_recru)  




#***************************************************
# Exportation des données renommées
#***************************************************
exporter(effectif_data,"DATA/effectif.csv")
exporter(recrutement_data,"DATA/recrutement.csv")
"""
# Recharger les données renommées
effectif_data=charger_fich("DATA/effectif.csv")
recrutement_data=charger_fich("DATA/recrutement.csv")

"""
#***************************************************
# Extraction par critères des données renommées
#***************************************************

print("*"*25)
print(f"{"Relecture du fichier effectifs":25}")
print("*"*25)
resultat_crit=extraire_plus_criteres(effectif_data)
exporter(resultat_crit,"EXPORT/EXTRACTIONS/effectif.csv")
print("*"*25)
print(f"{"Relecture du fichier Recrutement":25}")
print("*"*25)
resultat_crit=extraire_plus_criteres(recrutement_data)
exporter(resultat_crit,"EXPORT/EXTRACTIONS/recrutement.csv")"""


# Création des variables pour les tcd
les_annees = les_modalites(effectif_data,effectif_data[0][0])
les_métiers = les_modalites(effectif_data, effectif_data[0][1])
les_contrats=les_modalites(effectif_data, effectif_data[0][2])
les_sexes=les_modalites(effectif_data, effectif_data[0][3])
homme_data=extraire_un_critere(effectif_data,"homme",effectif_data[0][3])
femme_data=extraire_un_critere(effectif_data,"femme",effectif_data[0][3])
#premiere partie par année

arborescence("Repartition_sexe/Par_annee")
repartition(les_annees,les_métiers,"Repartition_sexe/Par_annee")


#deuxieme partie par métiers
arborescence("Repartition_sexe/Par_métier")
repartition(les_métiers,les_annees,"Repartition_sexe/Par_métier")

#troisieme partie par contrat
arborescence("Repartition_sexe/Par_contrat")
repartition(les_contrats,les_métiers,"Repartition_sexe/Par_contrat")

#quatrieme partie evolution des effectif  
arborescence("Evolution _effectif") 

tablveau_evo_effectif = [[[effectif_data[0][1]]+ [les_annees]+["effectif moyen"]]]
for metier in les_métiers[1:]:
    ligne = []
    for annee in les_annees[1:]:
        critere_recru = extraire_un_critere(effectif_data, annee, effectif_data[0][0])
        effec = somme_modalite_sans_critere(critere_recru, effectif_data[0][1], "effectif", metier)
        ligne.append(effec)
    critere_moy = extraire_un_critere(effectif_data, metier.strip(),effectif_data[0][1])
    moy = moyenne_variable(critere_moy, "effectif")
    

    tablveau_evo_effectif.append([metier] + ligne + [round(moy,2)])
exporter(tablveau_evo_effectif,f"EXPORT/STATISTIQUES/Evolution _effectif/Evolution_effectif_par_métier.csv")

#cinquieme partie evolution des homme


tableau_evo_homme = [[[effectif_data[0][1]]+ [les_annees]+["effectif moyen"]]]
for metier in les_métiers[1:]:
    ligne = []
    for annee in les_annees[1:]:
        critere_recru = extraire_un_critere(effectif_data, annee, effectif_data[0][0])
        effec = somme_modalité_avec_critere(critere_recru, effectif_data[0][3],"homme",effectif_data[0][1], "effectif", metier)
        ligne.append(effec)
    critere_moy = extraire_deux_critere(effectif_data, effectif_data[0][1],metier.strip(),effectif_data[0][3],"homme")
    moy = moyenne_variable(critere_moy, "effectif")
    tableau_evo_homme.append([metier] + ligne + [round(moy,2)])

exporter(tableau_evo_homme,f"EXPORT/STATISTIQUES/Evolution _effectif/Evolution_effectif_homme_par_metier.csv")

#sixcieme partie evolution des femme
tableau_evo_femme = [[[effectif_data[0][1]]+ [les_annees]+["effectif moyen"]]]
for metier in les_métiers[1:]:
    ligne = []
    for annee in les_annees[1:]:
        critere_recru = extraire_un_critere(effectif_data, annee, effectif_data[0][0])
        effec = somme_modalité_avec_critere(critere_recru, effectif_data[0][3],"femme",effectif_data[0][1], "effectif", metier)
        ligne.append(effec)
    critere_moy = extraire_deux_critere(effectif_data, effectif_data[0][1],metier.strip(),effectif_data[0][3],"femme")
    moy = moyenne_variable(critere_moy, "effectif")
    tableau_evo_femme.append([metier] + ligne + [round(moy,2)])
exporter(tableau_evo_femme,f"EXPORT/STATISTIQUES/Evolution _effectif/Evolution_effectif_femme_par_metier.csv")

gestion(effectif_data, recrutement_data)

