Ce script permet de recuperer et de stocker les information suivante presente sur le site http://books.toscrape.com :

    product_page_url
    universal_ product_code (upc)
    title
    price_including_tax
    price_excluding_tax
    number_available
    product_description
    category
    review_rating
    image_url

Le script enregistre aussi l'image de chaque couverture de livre presente sur le site.

Les données sont enregistrées dans un fichier CSV portant le nom de la categorie du livre. Tout les livre d'une meme categorie sont dans le meme fichier CSV.


/!\ TOUTES LES DONNEES RESULTANT DU SCRIPTS SONT STOCKER DANS LE DOSSIER result. /!\
/!\ UN .gitkeep EST PRESENT DANS CES FICHIERS POUR LES FAIRE APPARAITRE DANS GITHUB /!\

Python >= 3.10

ETAPE POUR EXECUTER LE SCRIPT
1. Installation et execution de l'environnement virtuel :

    Pour windows
    sh`python -m venv env`
    `.\env\Scripts\activate`
    `pip install -r .\requirements.txt`

    (Linux/Mac)
    sh`python3 -m venv env`
    `.` `env/bin/activate`
    `pip install -r requirements.txt`


2. Execution du script :

    sh`.\projprem.py`


3. Une fois le script terminer vous pouvez quitter l'environnement virutel :

    sh`deactivate`
