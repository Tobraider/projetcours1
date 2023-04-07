import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com"


def recupecategorie(liendusite):    #recupere toutes les categorie et les parcours une a une

    reponse,result = myRequest(liendusite)
    if result:
        soup = BeautifulSoup(reponse.text, "html.parser")   #transforme la reponse en donnée utilisable par bs4 (format choisi html.parser)

        #recuper le ul dans lequel il y a tout le <li> qui affiche chacun une categorie
        lis = soup.findAll("ul")[2].findAll("li")
        for li in lis:

            #recupere le "href" present dans chaque <li> et appelle la fonction pour check livre de chaque categorie
            checkcategorie(li.find('a')['href'])


def checkcategorie(liendepage):     #recupere tout les liens des pages livres et les parcours

    #recupere le nom de la categorie et en fait le nom du ficher
    nomfichier = "./result/CSV/"+liendepage.split('/')[-2].split('_')[0] + ".csv"
    with open(nomfichier, "w", encoding="utf-8") as outfile:

        #entete des categorie. elles sont les meme quelque soit la categorie
        entete = ["product_page_url","universal_ product_code","title","price_including_tax","price_excluding_tax","number_available","product_description","category","review_rating","image_url"]
        ajoutoutfile(entete,outfile)

        #creer le liens de la page a parcourir
        liendepage = liendepage.split('/')
        debutlien = "http://books.toscrape.com/catalogue/category/books/"
        debutlien += liendepage[-2]+"/"
        lien = debutlien+liendepage[-1]

        #passe TOUTE les pages de la categorie
        page = 1
        while page > 0:
            reponse,result = myRequest(lien)
            if result: #si page existe
                page += 1
                soup = BeautifulSoup(reponse.text, "html.parser")

                #recupere touts les articles de la page, ils ont une balise <article> puis les parcours un a un
                articles = soup.findAll('article')
                for article in articles:

                    #va recuperer les information sur la page article
                    checkpagelivre(article.find('a')["href"].split('/')[-2], outfile)

                #prepare le liens pour voir si page suivante existe
                lien = debutlien+"page-"+str(page)+".html"

            else:       #si page existe pas arrive ici car 404
                page = 0
            

def checkpagelivre(nomlivre, outfile):      #recupe la page du livre et recupere toutes les information demandées

    #genere le liens de la page
    liendelapage = "http://books.toscrape.com/catalogue/"+nomlivre+"/index.html"

    reponse,result = myRequest(liendelapage)
    if result:

        #initialise avec le lien de la page
        result = [liendelapage]
        
        soup = BeautifulSoup(reponse.text, "html.parser")

        #recupere tout les <td> car plusieurs information voulu dedans
        tds = soup.findAll('td')

        #ajout de UPC
        result.append(tds[0].text)

        #ajout du titre stocker dans le premier <h1>. Double guillemets pour eviter tout conflit possible de syntaxe dans le titre
        result.append('"'+soup.find('h1').text.replace('"','""')+'"')

        #ajout du prix avec les taxes. Attention un Â se glisse devant a cause de html.parser
        result.append(tds[3].text[1:])

        #ajout du prix sans les taxes. Attention un Â se glisse devant a cause de html.parser
        result.append(tds[2].text[1:])
        
        #ajout du nombre en stock. Attention une ( est presente devant le numero
        result.append(tds[5].text.split()[2][1:])

        #recupe tout les <p> car plusieurs donnée a l'interieur
        ps = soup.findAll('p')

        #ajout de la description du produit mets des guillement car virgule dedans. remplace ensuite toutes les guillemets par des doubles car convention. Retire 5 cararctere au debut car il y a un \n et 4 espaces
        result.append('"'+soup.find('meta', {"name":"description"})["content"].replace('"','""')[5:]+'"')

        #ajout de la categorie
        result.append(soup.findAll('a')[3].text)

        #recupere la class de <p> dans lequel est stocké le nombre d'etoile du livre puis le convertie en chiffre.
        match ps[2]["class"][1]:
            case "One":
                result.append(1)
            case "Two":
                result.append(2)
            case "Three":
                result.append(3)
            case "Four":
                result.append(4)
            case "Five":
                result.append(5)
            case _:     #En cas d'erreur (nom pas present dans la liste car faute de frappe ou note differente) retourne une erreur sur la console et mets la valeur erreur
                result.append("error")
                print("erreur sur le nomnbre d'etoile")

        #telecharge l'image puis ajout du liens de l'image dans la liste
        result.append(sauvegardeImage(soup.find('img')["src"].replace("../..","http://books.toscrape.com"), nomlivre))

        #ecrit toutes ces données dans le fichier correspondant
        ajoutoutfile(result, outfile)

def ajoutoutfile(listaajouter, outfile):

    #initialise avec la premiere valeur de la liste
    encsv = str(listaajouter.pop(0))

    #parcours tout les objets de la liste
    for i in listaajouter:
        
        #ajout a la chaine de caractere en ajoutant une virgule devant (delimitaion csv)
        encsv += ','+str(i)
    
    #ajout un retour a la ligne a la fin de la ligne
    encsv+='\n'

    #ecrit dans le fichier la chaine de charactere
    outfile.write(encsv)

    #ecrit un petit messasge pour dire que tout est ok
    print("donnée OK")

def sauvegardeImage(lien, nomlivre):
    reponse = requests.get(lien)
    if reponse.ok:

        #ouvre un fichier en wb (write binaire) pour enregistrer l'image. ouverture en binaire obligatoire pour l'image recu
        with open("./result/Images/"+nomlivre+".jpg", 'wb') as image:

            #recupe le content de la reponse
            image.write(reponse.content)

            #envoie un petit message a la console pour etre sur que tout est ok
            print("image OK")

    #retourne le lien car doit etre enregistrer ailleurs.
    return lien


def myRequest(lien):
    reponse = requests.get(lien)    #fait une requete au site
    if reponse.ok:                  #verifie si requete ok (200...)
        reponse.encoding="utf-8"    #converti tout en utf-8
        return reponse,True         #ajout de true car condition plus tard possible
    else:
        return reponse,False

#execute le programme
recupecategorie("http://books.toscrape.com/catalogue/category/books_1/index.html")