from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import requests as r
from bs4 import BeautifulSoup as b
import unicodedata
import re
import json
from gi.repository import Gtk
count = 10
class search_products():
	def dire(propos="hello"):
		print(propos)

class ScrappingJson():
    def __init__(self, button, product="Nutella"):
        self.product = product
        print(self.product)

    def get_product_url(self, link_product=""):
        self.link_product = link_product
        requête = r.get("https://fr.openfoodfacts.org/cgi/search.pl?search_terms={}&search_simple=1&action=process".format(self.product))
        html = requête.content
        soup = b(html, 'html.parser')
        list_products = soup.select(".products")[0]
        product_one = list_products.li

        # On récupère une url
        nb = 0

        for link in list_products.find_all('a'):
            while nb < 1:
                self.link_product = link.get('href')
                # print(link_product)
                nb += 1

        return self.link_product
        print(self.link_product)

    def get_json_categorie(self):
        # get the product barcode
        print(self.link_product)
        CB_link = re.findall("([0-9]+)", self.link_product)
        CB_link = str(CB_link)
        print(CB_link)
        # On requête l'api du produit
        product = r.get('https://fr.openfoodfacts.org/api/v0/produit/{}.json'.format(CB_link))
        print(product)
        # We run the json to get the name of the category
        product_json = product.json()
        product_json = product_json['product']['categories_tags'][1]
        product_json = product_json[3:]
        print(product_json)
        # Configuring the url category in json
        category_json = "https://fr-en.openfoodfacts.org/category/{}/1.json".format(product_json)
        print(category_json)
        return category_json, product_json