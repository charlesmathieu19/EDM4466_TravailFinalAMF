# coding : utf-8

import requests
import csv
from bs4 import BeautifulSoup

fichier = "amfcommuniqués.csv"

# Utiliser un URL me permettant d'aller regarder dans plusieurs pages différentes. Ces pages contiennent les liens vers les communiqués de l'AMF.  

url = "https://lautorite.qc.ca/grand-public/salle-de-presse/actualites/?tx_solr[filter][0]=category%3A50&tx_solr[page]="

entetes = {
    "User-Agent":"Charles Mathieu - 514-746-5481 : requête envoyée dans le cadre d'une démarche journalistique", 
    "From":"charlesbmathieu@hotmail.com"
}

# Il y a 42 pages de communiqués, et la première page est la page 0. Ainsi, j'ai créé une liste de nombre allant de 0 à 41. C'est pour cette raison qu'elle se finit par 42. 

pages = list(range(0,42))

# Création de ma première boucle. Ici je viens créer un lien pour chaque page consultée. 

for page in pages:

    urlpage = url + str(page) 
    # print(urlpage)

    # Création de requêtes pour aller chercher les 42 pages. 

    sites = requests.get(urlpage, headers=entetes)
    pages2 = BeautifulSoup(sites.text, "html5lib")
    articles = pages2.find_all("li", class_="search-result")
    
    for article in articles:
        # Je vais chercher la date pour aller l'inclure dans mon fichier CSV.
        date = article.find("span", class_="search-result-date").text.strip()
        # Je vais également inclure le titre du communiqué. 
        titrecommunique = article.find("a", class_="search-result-title").text.strip()
        listesujets = []
        listesujets.append(date)
        listesujets.append(titrecommunique)
        # Parce que les urls que l'on retrouve dans le code source ne sont que la fin de l'URL requis, j'ai pris la première partie de l'URL pour par la suite inclure la partie retrouvée sur le code. 
        urldebut = "https://lautorite.qc.ca"
        urlfin = article.find("a", class_="search-result-title")["href"]
        urlfinal = urldebut + urlfin
        # Ajout de l'URL complet dans ma liste. 
        listesujets.append(urlfinal)

        # Création d'une deuxième requête pour chacun des liens. 

        sites2 = requests.get(urlfinal, headers=entetes)
        # J'ai eu à utiliser "html5lib" parce que html parser ne fonctionnait pas pour aller chercher certaines parties du texte. Le tout est sensé être un peu plus lent que le parser que nous utilisions, mais au final, le résultat est meilleur, d'après moi. 
        pages3 = BeautifulSoup(sites2.text, "html5lib")
        # print(nouvelles)

        # Ici, parce qu'un des liens était un PDF, j'ai dû faire un TRY pour aller chercher les textes et les ajouter à ma liste. 

        try:
            # Je suis ici allé chercher tout le texte de toutes les pages pour par la suite en faire une analyse. 
            n = pages3.find("div", class_="news-single").text.replace("AVIS", "").replace("\n", " ").replace("\r", " ").replace("\t", " ").replace("  ", " ").replace("   ", " ").replace("     ", " ").replace("Ce lien s'ouvrira dans une nouvelle fenêtre", " ").strip()
            listesujets.append(n)
        except:
            n2 = "PDF"
            listesujets.append(n2)
            

        Charles = open(fichier, "a")
        Lea = csv.writer(Charles)
        Lea.writerow(listesujets)
           
           



            










