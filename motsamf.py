# coding : utf-8

import csv
import spacy
from collections import Counter

tal = spacy.load("fr_core_news_md")

# Ajout ici de stop words

tal.Defaults.stop_words.add("0337Autres")
tal.Defaults.stop_words.add("— 30 —")
tal.Defaults.stop_words.add("Sylvain")
tal.Defaults.stop_words.add("Théberge")
tal.Defaults.stop_words.remove("gens")

# Importation de mon fichier CSV créé précédemment. 

nouvellesamf = "amfcommuniqués.csv"
f = open(nouvellesamf)
nouvelles = csv.reader(f)
next(nouvelles)

# Création de trois listes pour tester différentes choses. 

listebigrams = []
listemots = []
listebigramsassurance = []

# Première bouche pour aller chercher tous les éléments.

for nouvelle in nouvelles:
    # Je vais donc aller chercher uniquement les textes qui se retrouvent dans la quatrième colonne de mon fichier CSV. 
    textes = nouvelle[3]
    # print(textes)
    doc = tal(textes)
    # Je vais utiliser des lemmes pour ma recherche. 
    lemmes = [token.lemma_ for token in doc if token.is_stop == False and token.is_punct == False and token.like_num == False and token.is_space == False]
    # print(lemmes)
    
    # https://spacy.io/api/token a été la source consultée qui m'a permis d'enlever les nombres et les espaces que l'on retrouvait dans les bigrams et les mots (?)
    
    # Création de bigrams
    for x, y in enumerate(lemmes[:-1]):
        bigrams = "{} {}".format(lemmes[x],lemmes[x + 1])
        listebigrams.append(bigrams)
        # Je veux ici aller chercher les paires de mots contenant le mot "assurance" ou "insurance", car je crois que c'est la seule manière, pour le moment, de ne pas me retrouver avec les mots fréquemment rencontrés dans la fin des communiqués (comme le contact pour les journalistes)
        if "surance" in bigrams:
            listebigramsassurance.append(bigrams)
    
    # Je viens également chercher les mots seuls. 
    
    for lemme in lemmes:
        listemots.append(lemme)

# Utilisation de Counter pour être en mesure d'aller chercher les mots ou les paires de mots que l'on retrouve le plus souvent dans les textes. 

freq = Counter(listebigrams)
freq2 = Counter(listemots)
freq3 = Counter(listebigramsassurance)

print(freq.most_common(50))
# print(len(listebigrams))
print("-"*10)
print(freq2.most_common(50))
# print(len(listemots))
print("-"*10)
print(freq3.most_common(20))
