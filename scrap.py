from bs4 import BeautifulSoup
import string
import requests
import json

baseUrl = "https://magene.pagesperso-orange.fr/"
alphabet = list(string.ascii_uppercase)


def getHTML(url): #Récupères le code source de la page HTML cible
    req = baseUrl+url+".html"
    print("[ScrapNormandico] requêtes GET '"+req+"' en cours.")
    try:
        request = requests.get(req)
        print("[ScrapNormandico] requêtes effectué.")
    except:
        print("[ScrapNormandico] requêtes échoué.")
        return None
    html = request.text
    soup = BeautifulSoup(html,"html.parser")
    return soup

def parseHTML(soup): #Scrap les balises cibles de la page HTML
    if (soup == None):
        return None
    print("[ScrapNormandico] Analyse des balises <p> en cours")
    
    try:
        scrap = soup.find_all("p")
    except:
        print("[ScrapNormandico] Analyse échouée! Impossible d'obtenir les balises")
    
    print("[ScrapNormandico] Analyse terminé!")
    return scrap

def appendTerm(letterScrap,scrap): #Convertis et exportes les données vers un fichier JSON
    print("[ScrapNormandico] Sauvegarde des données en cours")
    scraplist = [] #liste dans lequel on va mettre les expressions
    scrapData = [] #liste dans lequel les expressions vont être scrappés
    expressionDict = {letterScrap : []} #dictionnaire pour y rajouter les expressions en fonction de la lettre de l'alphabet

    for expression in scrap: #encodes et enlèves les balises des expressions
        expression = str(expression)
        expression.encode('utf_32','strict')
        expression = expression.replace('<p>','')
        expression = expression.replace('</p>','')
        expression = expression.replace("   ","")
        expression = expression.strip()
        expression = expression.splitlines()
        
        scraplist.append(expression)

    for term in scraplist: #sépares les expressions du français et du normands
        for expression in term:
            expression = expression.split("=",1)
            scrapData.append(expression)
    
    for expression in scrapData: #vérifies si les expressions sont bien conformes
        if (len(expression)>1):
            if ("<" in expression[0] or ">" in expression[0] or "<" in expression[1] or ">" in expression[1]):
                pass
            elif ("<" not in expression and ">" not in expression):
                terme = {
                    "french" : expression[1].strip(),
                    "normand" : expression[0].strip()
                }
                expressionDict[letterScrap].append(terme)

    print("[ScrapNormandico] Conversion des données terminée.")
    with open("output/dico_"+letterScrap+".json","a+") as file:
        file.write(json.dumps(expressionDict))
        file.close()
    print("[ScrapNormandico] Sauvegarde des données terminée dans le fichier 'output/dico_"+letterScrap+".json'.")

for letter in alphabet:
    url=letter
    if letter == "A":
        url = "menudico"
    scrap = parseHTML(getHTML(url))
    appendTerm(letter,scrap)