#!/usr/bin/python
# -*- coding: utf-8 -*-#

# ---------------------------------------------------------------------------------------
# rasec_thomas.py (script Python 3.x)
# Décodage d'une chaîne de caractères encodée à la César.
# Nécessite la présence dans le même répertoire que ce script du script dawg.py
# ansi que d'une liste de mots servant de référence pour la validation des
# chaînes décodées. 
# ---------------------------------------------------------------------------------------

# L'alphabet pris en compte (chaîne) 
alphabet = "abcdefghijklmnopqrstuvwxyz"
taille_alphabet = len(alphabet)

# Génèration des différents alphabets césarisés. 
# Ils sont stockés dans 'variantes_alphabet'. 
i = 1
a = alphabet
variantes_alphabet = []
variantes_alphabet.append(alphabet) 
while i <= taille_alphabet: 
    # On rejette la lettre initiale de la dernière chaîne traitée a[0] 
    # à la fin de la nouvelle chaîne. 
    a = a[1:] + a[0]
    variantes_alphabet.append(a) 
    i += 1 

# Préparation/nettoyage de la chaîne saisie par l'utilisateur. 
# L'apostrophe est convertie en espace. Les signes de ponctuation sont éliminés.
# *** A FAIRE :
# Assurer un meilleur traitement des signes de ponctuation pour éviter p.ex.
# de découper les noms de domaine 'data.gouv.fr' et les nombres '3.1416' 
transtab = str.maketrans("'’", "  ", "?,.;:!()«»")


# ---------------------------------------------------------------------------------------
print("==================================================================")
print("======    Script de déchiffrement d'une chaîne césarisée    ======") 
print("==================================================================")

# Chargement du dictionnaire de référence permettant de valider les mots décodés. 
# La procédure optimise le dictionnaire en mémoire et prend qq secondes.
print("\n*** Chargement et préparation du dictionnaire de référence.")
print("*** Veuillez patienter quelques instants ", end = "") 
from dawg import * 

# Exemple de texte encodé : ath hpcvadih adcvh sth kxdadch st a pjidbct
# (= les sanglots longs des violons de l'automne) 

while True: 
    try: 
        print("\n==================================================================")
        print("Chaîne à décoder ? [Enter ou Ctrl-C pour sortir]") 
        print(">>> ", end ="")

        # chaine_entree = la chaîne à décoder 
        chaine_entree = input() 

        # Etape 1 - Préparation de la chaîne à traiter
        
        # Si la chaîne est vide, on sort de la boucle while 
        if chaine_entree == "": 
            break
        
        # On passe toute la chaîne en minuscules 
        chaine_entree = chaine_entree.lower()

        # On remplace les apostrophes par des espaces et
        # on élimine les signes de ponctuations
        chaine_entree = chaine_entree.translate(transtab)

        # On élimine les espaces en trop
        chaine_entree = chaine_entree.replace('  ', ' ')

        # Calcul de la longueur de la chaîne (on élimine les espaces) 
        # (sert à évaluer le score des transcodages) 
        taille_chaine = len(chaine_entree.replace(' ', '')) 

        print("\n------------------------------------------------------------------")
        print("*** Chaîne à décoder :\n\"%s\"" % chaine_entree)


        # Etape 2 - On décode la chaîne d'entrée en invoquant chacun
        # des alphabets générés précédemment. Chacun des décodages est
        # stocké dans la liste 'liste_chaine_sortie'. 
        liste_chaine_sortie = {}
        i = 0
        for variante in variantes_alphabet: 
            trans = str.maketrans(variante, alphabet) 
            chaine_sortie = chaine_entree.translate(trans)
            # Stockage de la chaîne de caractère avec référence à l'alphabet
            # utilisé (i) 
            liste_chaine_sortie[i] = chaine_sortie
            i += 1 


        # Etape 3 - Epreuve du dictionnaire.
        # On reprend les chaînes transcodées une à une.
        # On en extrait les mots un à un et on les confronte au dictionnaire. 
        # Si le mot figure dans le dictionnaire, on augmente le score de la
        # chaîne transcodée en lui ajoutant la longueur de ce mot.
        best_score  = 0
        best_code   = 0
        best_string = ""
        # Stockage des mots reconnus et inconnus 
        mots_reconnus = {}
        mots_inconnus = {}
        # Stockage des résultats 
        scoring = []
        # Pour chaque chaîne transcodée : 
        for i in liste_chaine_sortie:
            score  = 0 
            code   = i
            chaine = liste_chaine_sortie[i]
            # Extraction des mots de la chaîne transcodée
            mots = chaine.split(' ') 
            mots_reconnus[i] = [] 
            mots_inconnus[i] = []
            # Pour chaque mot extrait : 
            for mot in mots:
                # Analyse des mots 
                if dawg.lookup(mot):
                    # Le mot est reconnu, on le stocke pour un éventuel
                    # affichage final
                    mots_reconnus[i].append(mot) 
                    score = score + len(mot) 
                else: 
                    # Le mot n'est pas reconnu, on le stocke pour un éventuel 
                    # affichage final 
                    mots_inconnus[i].append(mot) 
            # Stockage du résultat obtenu (le score, le code César et la chaîne) 
            scoring.append((score, code, chaine))
            # Si le score est le meilleur jusqu'ici, on le garde sous le coude 
            if score > best_score:
                best_score  = score
                best_code   = code 
                best_string = liste_chaine_sortie[i]

        # On procède au tri des résultats
        ordered_results = sorted(scoring, reverse=True)

        # Evaluation du résultat final
        # A FAIRE :
        # - vérifier qu'il n'y a pas plusieurs résultats avec un même score
        # - afficher plusieurs résultats quand les scores sont proches 
        print("------------------------------------------------------------------")
        if best_score == taille_chaine:
            # Si la chaîne d'entrée est intégralement validée par le dictionnaire, 
            # le résultat est réputé fiable. 
            type_decodage = "fiable" 
            resultat = ordered_results[0][2]
            detail = 0
        elif best_score > (taille_chaine / 1.2):
            # Si le score est bon ou très bon (au moins 80% validé par le dico),
            # on note le résultat comme probable. 
            type_decodage = "plutôt fiable"
            resultat = ordered_results[0][2]
            detail = 1
        elif best_score < (taille_chaine / 3):
            # Si le score est trop faible ou nul (moins de 30% validé par le dico),
            # on s'avoue vaincu. 
            type_decodage = "inexploitable"
            # resultat = chaine_entree
            resultat = ordered_results[0][2]
            detail = 3
        else: 
            # Entre 30 et 80%, on exprime des doutes 
            type_decodage = "incertain"
            resultat = ordered_results[0][2]
            detail = 2
        
        # Affichage du résultat final
        # (a) le score obtenu et la valeur de décalage du code César 
        print("*** Résultat %s (score = %d/%d) avec valeur de décalage = %d [%d]." \
              % (type_decodage, best_score, taille_chaine, best_code, best_code - taille_alphabet))
	# (b) la chaîne transcodée 
        print("\"%s\"" % resultat)
        # (c) facultatif : la liste des mots non reconnus (pour les résultats fiables) 
        # ou la liste des mots reconnus (pour les résultats non fiables) 
        if (detail == 1 or detail == 2) and len(mots_inconnus[best_code]) > 0: 
            print("--> Mots inconnus : %s" % mots_inconnus[best_code])
        if (detail == 2 or detail == 3) and len(mots_reconnus[best_code]) > 0: 
            print("--> Mots reconnus : %s" % mots_reconnus[best_code])

    except KeyboardInterrupt: 
        # Traitement du Ctrl+C pour une sortie "propre" du programme 
        print("\n==================================================================\n")
        print("Adios, Caesar!\n") 
        exit(1)

print("\n==================================================================\n")
print("Adios, Caesar!\n") 


