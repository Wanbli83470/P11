"""constantes connection"""
import os
import datetime

date_day = datetime.datetime.now()

LOGIN_CONNECT = {
    "HOST": '127.0.0.1',
    "USER": 'thomas',
    "PASSWORD": os.environ.get("SECRET_PASSWORD_P11"),
    "DB": 'P11',
    "PORT": 3306
}

CATEGORIES = "`CATEGORIES`"
PRODUITS = "`PRODUITS`"
SUBSTITUTS = "`SUBSTITUTS`"

TABLES = [SUBSTITUTS, PRODUITS, CATEGORIES]

PRODUCTS = {"Boisson": ["Coca Cola", "Ice tea", "Fanta", "Orangina"],
            "Gâteaux/Sucrerie": ["Kinder Pingouin", "Oréo", "Nutella", "Petit Prince", "Cookie"],
            "Dessert": ["Lait nestlé", "Fondant Chocolat", 'Flamby'],
            "Poisson": ["Batonnet de surémi", "poisson pané"],
            "Pizza": ["Pizza"]}

CATEGORIES_TO_ENGLISH = {
    "Boisson": "carbonated-drinks",
    "Gâteaux/Sucrerie": "sweet-snacks",
    "Dessert": "desserts",
    "Poisson": "seafood",
    "Pizza":"Pizzas pies and quiches"
}

TRANSITION = "\n" + "-" * 204
