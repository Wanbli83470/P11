"""constantes connection"""
import os
HOST='127.0.0.1'
USER='thomas'
PASSWORD = "jpmfmaemp73%"

# PASSWORD= os.environ.get("SECRET_PASSWORD_P11")
DB='P11'
PORT = 3306

CATEGORIES = "`CATEGORIES`"
PRODUITS = "`PRODUITS`"
SUBSTITUTS = "`SUBSTITUTS`"

TABLES = [SUBSTITUTS, PRODUITS, CATEGORIES]

PRODUCTS = {"Boisson" :["Coca Cola", "Ice tea", "Fanta", "Orangina"], 
			"Gâteaux/Sucrerie":["Kinder Pingouin", "Oréo", "Nutella", "Petit Prince", "Cookie"], 
			"Apérétifs":["Chips", "Cacahuètes", "Crackers", "Kiri"], 
			"Dessert":["Lait nestlé", "Fondant Chocolat", 'Flamby'], 
			"Poisson":["Batonnet de surémi", "poisson pané"]}

CATEGORIES_TO_ENGLISH = {"Boisson":"carbonated-drinks", "Gâteaux/Sucrerie": "sweet-snacks", "Apérétifs":"salty-snacks", "Dessert" : "desserts", "Poisson" : "seafood"}

transition = "\n"+"-"*204
