#!/usr/bin/python
# -*- coding: utf-8 -*-#

# ---------------------------------------------------------------------------------------
# cesar_thomas.py (script Python 3.x) 
# Encodage d'une chaîne de caractères à la César. Génère une version cryptée 
# d'une chaîne d'entrée par application d'un principe de décalage constant 
# de chacune des lettres de l'alphabet. 
# Principe : (1) On définit une valeur de décalage. (2) On crée un tableau 
# associant à chaque lettre de l'alphabet source la lettre correspondante 
# dans l'alphabet décalé (p.ex. a -> e, si le décalage vaut 4). (3) On demande 
# à l'utilisateur une chaîne de caractères qu'on transforme selon ce tableau. 
# ---------------------------------------------------------------------------------------

# Fonction générique de transcodage de caractères (pour permettre de ramener 
# les caratères accentués aux caractères non accentués correspondants). 
# Cf. https://pypi.python.org/pypi/text-unidecode/ 
from text_unidecode import unidecode

# L'alphabet pris en compte (liste) 
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', \
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']  

# La taille de l'alphabet (longueur de la liste) 
taille_alphabet = len(alphabet) 

# Valeur de décalage par défaut pour la césarisation de l'alphabet 
DECALAGE = 3

# ---------------------------------------------------------------------------------------
# checkint/scanum = fonction de vérification qu'un nombre est bien un nombre. 
# Utilisé pour valider la saisie d'entiers négatifs. Un appel direct int(input()) 
# renvoie une erreur (input renvoyant lui-même une chaîne de caractères). 
# Cf. https://www.daniweb.com/programming/software-development/threads/278529/numeric-input-python3 
def checkint(i):
    s=[n for n in  i if n.isdigit()]
    return ''.join(s)==i

def scanum(x):
    orig=x 
    x=x.lstrip()
    if x[0]=='-':
        x=x[1:].lstrip('0')
        intpart,found,fracpart=x.partition('.')
        intpart=intpart or '0' ## use 0.234 instead of .234
        ok=checkint(intpart)
        if found:
            ok = ok and checkint(fracpart)
        if not ok: return orig #renvoie la chaîne d'origine
        if found:
            return '-'+intpart+'.'+fracpart.rstrip('0')
        else: return '-'+intpart
    else:
        if x[0]=='+': x=x[1:]
        else: x=x.lstrip()
        x=x.lstrip('0')
        intpart,found,fracpart=x.partition('.')
        intpart=intpart or '0' ## use 0.234 instead of .234
        ok=checkint(intpart)
        if found:
            ok = ok and checkint(fracpart)
        if not ok: return orig #renvoie la chaîne d'origine
        if found:
            return intpart+'.'+fracpart.rstrip('0')
        else: return intpart

# ---------------------------------------------------------------------------------------
# cesarise_alphabet = fonction de création de l'alphabet décalé selon la valeur 
# de décalage retenue  
# Le résultat est un tableau 'alphabet_cesar' dans lequel on associe à chaque lettre de 
# l'alphabet d'origine la lettre décalée correspondante (selon la valeur 'decalage')
# A FAIRE :
# Au lieu de créer un tableau, créer une table de transcodage à exploiter via
# la fonction "str.maketrans(chaine1, chaine2)" 
def cesarise_alphabet ( decalage = DECALAGE ): 
    # alphabet_cesar = le tableau est initialisé à vide 
    alphabet_cesar = {} 
    i = 0 
    # On prend chacune des lettres de l'alphabet d'origine une à une 
    while i < taille_alphabet: 
        # On calcule la valeur décalée 
        j = i + decalage 
        # Si cette valeur excède la taille de l'alphabet, on lui retranche la taille 
        # de l'alphabet pour la maintenir compatible avec l'alphabet  
        if abs(j) >= taille_alphabet: 
            if j < 0: 
                j = j + taille_alphabet 
            else: 
                j = j - taille_alphabet 
        
        # On stocke dans 'alphabet_cesar' la paire lettre-source/lettre-décalée 
        alphabet_cesar[alphabet[i]] = alphabet[j]
        # print("row = %s,%s" % (alphabet[i], alphabet[j]))

        # On passe à la lettre suivante 
        i += 1 

    # On renvoie le tableau créé 
    return (alphabet_cesar) 

# ---------------------------------------------------------------------------------------
# cesarise_chaine = fonction de réencodage d'une chaîne quelconque (chaine1) 
# en une nouvelle chaîne (chaine2) par exploitation de l'alphabet césarisé
# A FAIRE :
# Au lieu de parcourir les car. un à un, appliquer une fonction exploitant
# la table de transcodage créée ci-dessus : "chaine.translate(table)" 
def cesarise_chaine ( chaine1, alphabet_cesar ): 
    # On s'assure que la chaîne de sortie chaine2 est bien remise à 0 
    chaine2 = "" 
    # On parcourt les caractères de la chaîne chaine1 un par un 
    for caractere in chaine1: 
        if caractere in alphabet_cesar: 
            # Si le caractère courant figure dans l'alphabet, on lui substitue sa 
            # valeur dans le tableau alphabet_cesar qu'on ajoute à la chaîne chaine2 
            chaine2 = chaine2 + alphabet_cesar[caractere] 
        else: 
            # Sinon on l'ajoute tel quel à la chaîne chaine2 
            # (On garde ainsi les espaces et les signes de ponctuation.)
            chaine2 = chaine2 + caractere 

    # On renvoie la nouivelle chaîne une fois tous les caractères traités
    return (chaine2) 



# ---------------------------------------------------------------------------------------
#
# Initialisation de la session utilisateur 
#
print("==================================================================")
print("======   Script de chiffrement par décalage de l'alphabet   ======") 
print("==================================================================")

# ---------------------------------------------------------------------------------------
# 1/ On demande la valeur de décalage à appliquer pour cette session 

print("\nPréciser une valeur de décalage (entier entre -%d et +%d)" \
  % (taille_alphabet, taille_alphabet)) 
print(">>> ", end ="")

param_decalage = input() 

# On vérifie qu'on a bien une valeur valide (sinon, appel de la valeur par défaut) 
if param_decalage != "": 
    # On s'assure qu'on a bien affaire à une valeur numérique 
    param_decalage = scanum(param_decalage) 
    try: 
        DECALAGE = int(param_decalage)
        # On teste que la valeur de décalage n'excède pas la taille de l'alphabet 
        # Sinon, on la ramène à une valeur compatible avec la taille de l'alphabet 
        if abs(DECALAGE) >= taille_alphabet:
            x = abs(DECALAGE) % taille_alphabet 
            DECALAGE = x * -1 if DECALAGE < 0 else x 
    except ValueError:
        # La valeur n'est pas un entier 
        print("*** %s: valeur invalide" % param_decalage) 

# On affiche la valeur de décalage qui sera utilisée pour la session 
print("Valeur de décalage retenue = %d " % DECALAGE, end="") 


# ---------------------------------------------------------------------------------------
# 2/ On crée l'alphabet décalé (alphabet2) pour la valeur DECALAGE précédente 
alphabet2 = cesarise_alphabet(DECALAGE)

# On exemplifie la valeur de décalage via l'alphabet décalé
print("('%s' devient '%s')" % (alphabet[0], alphabet2[alphabet[0]]))


# ---------------------------------------------------------------------------------------
# 3/ On procède à l'encodage d'une chaîne de caractères saisie par l'utilisateur. 
# On demande en boucle à l'utilisateur une chaîne de départ (chaine_entree) 
# et on lui restitue la chaîne césarisée. 
# On sort de la boucle par la saisie d'une chaîne vide ou un Ctrl+C. 
while True: 
    try: 
        print("\n==================================================================\n")
        print("Texte à encoder ? [Ctrl+C pour sortir]") 
        print(">>> ", end ="")

        chaine_entree = input() 

        # Si la chaîne est vide, on sort de la boucle while 
        if chaine_entree == "": 
            break 

        # On transcode les éventuels caractères accentués en caractères non accentués 
        chaine_entree = unidecode(chaine_entree) 
        
        # On passe toute la chaîne en minuscules 
        chaine_entree = chaine_entree.lower() 

        # On produit la chaîne césarisée (chaine_sortie) en appelant 
        # la fonction cesarise_chaine avec l'alphabet décalé créé précédemment 
        chaine_sortie = cesarise_chaine(chaine_entree, alphabet2) 

        # On recapitule le tout à l'écran 
        print("------------------------------------------------------------------")
        print("Texte à encoder = %s " % chaine_entree) 
        print("Texte encodé    = %s " % chaine_sortie) 

    except KeyboardInterrupt: 
        # Traitement du Ctrl+C pour une sortie "propre" du programme 
        print("\n==================================================================\n")
        print("Adios, Caesar!\n") 
        exit(1)

print("\n==================================================================\n")
print("Adios, Caesar!\n") 
