 #!/usr/bin/env python
 # -*- coding: utf-8 -*-
 #  Copyright 2019 Thomas ESTIVAL
"""use of the reportlab library to generate the PDF and uses of the modules units to work in cm
Use regex for extract the importants informations
Use the json and requests module for a json result
Use the beautifulsup for scrapping product
Use the pymysql for connect to local Database
Import the personnals parameters with a constants.py file
"""

import math
import re
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

import requests as r
import json
import pymysql
import pymysql.cursors

from constants import *

"""CONNECT TO THE DATABASE"""
try :
    connection = pymysql.connect(host=HOST, #variable in file constantes.py
                                     user=USER,
                                     password=PASSWORD,
                                     db=DB,
                                     charset='utf8mb4',
                                     port = PORT,
                                     cursorclass=pymysql.cursors.DictCursor)
except :
        print("Erreur de connexion, veuillez vérifier les paramètres dans le fichiers constants.py")

class ExportPdf():
    """New program to export substitutes in PDF format"""
    def export():
        """recovery of the number of products with count and registration of substitutes in the PDF"""
        with connection.cursor() as cursor:
            sql = "SELECT COUNT(*) FROM SUBSTITUTS"
            cursor.execute(sql, ())
            count = cursor.fetchall()
            print(count)
            count = str(count)
            expression = re.compile("([0-9])")
            tes = expression.findall(count)
            print(tes)
            count = tes            
            connection.commit()

        name = input("Quelle est votre nom ? \n>>> ")
        pdf = canvas.Canvas("substituts-{}.pdf".format(name))
        pdf.drawString(3*cm, 28*cm, u'Bienvenue {} vous avez enregistré {} produits'.format(name, count[0]))
        pdf.line(10.5*cm,23*cm,10.5*cm,0*cm)
        #Create the column
        pdf.drawString(3.5*cm, 23.5*cm, u'Mes habitudes')
        pdf.drawString(13.5*cm, 23.5*cm, u'Mes substituts')
        #Create the lines
        nb_line = 21
        x = 21
        y = 21

        #Get the input_product from table SUBSTITUTS from Database
        with connection :
            cur = connection.cursor()
            cur.execute("SELECT INPUT_PRODUCT, PRODUIT_ID FROM SUBSTITUTS")
            data_sub = cur.fetchall()
        

        position = 20.4
        for s in data_sub :
            print(s["INPUT_PRODUCT"])
            print(s["PRODUIT_ID"])

            with connection :
                cur = connection.cursor()
                cur.execute("SELECT NOM FROM PRODUITS WHERE ID=%s" % (int(s["PRODUIT_ID"])))
                data_sub2 = cur.fetchall()
                pdf.drawString(14*cm, position*cm, str(data_sub2[0]["NOM"]))

            print(position)
            pdf.drawString(4*cm, position*cm, s["INPUT_PRODUCT"])
            pdf.line(0*cm,x*cm,21*cm,y*cm)
            nb_line = nb_line - 1
            position = position - 1
            x = x - 1
            y = y - 1

        #Get the substituts from table SUBSTITUS from Database


        pdf.save()

class DownloadProduct():

    def get_product(max_pages=5, requête=""):
        # Creation list for BDD
        url = []
        name = []
        ns = []
        link_pictures = []

        print("la requête retourne un code : {}".format(requête))
        dynamic_link = r.get("https://fr-en.openfoodfacts.org/category/{}/1.json".format(requête))
        info = dynamic_link.json()
        count = info['count']
        page_size = info['page_size']

        nbPages = int(math.floor(count / page_size) + 1)  # On déduit le nombre de pages
        print("nombre de pages = " + str(nbPages))
        i = 0
        live_page = 1
        while live_page <= nbPages:
            dynamic_json = dynamic_link.json()
            for data in dynamic_json["products"]:

                # Filter produced with nutriscore

                if data["nutrition_grades_tags"] != ['not-applicable'] and data["nutrition_grades_tags"] != ['unknown']:
                    try:
                        url.append((data["url"]))
                        name.append((data["product_name"]))
                        ns.append((data["nutrition_grades_tags"][0]))
                        link_pictures.append((data["image_url"]))
                        i = i + 1


                    #
                    # Deleting products without images

                    except KeyError:
                        print("un produit sans image; n°{}".format(i))
                        numero = i

                        del url[numero]
                        del name[numero]
                        del ns[numero]

            live_page += 1
            dynamic_link = r.get("https://fr-en.openfoodfacts.org/category/{}/{}.json".format(requête, live_page))
            print(live_page)
            print(dynamic_link)
            if live_page > max_pages:
                break

            # Convert number to letters
        for n, i in enumerate(ns):
            if i == 'a':
                ns[n] = 1

            elif i == 'b':
                ns[n] = 2

            elif i == 'c':
                ns[n] = 3

            elif i == 'd':
                ns[n] = 4
            elif i == 'e':
                ns[n] = 5

        print(ns)
        print("{} élément dans la liste".format(len(link_pictures)))
        with connection.cursor() as cursor:

            sql = "SELECT MAX(`ID`) FROM CATEGORIES"
            cursor.execute(sql, ())
            id_category = cursor.fetchall()
        print(id_category)
        id_category = str(id_category)
        N_ID = ""
        for x in id_category :
            if x in ("0","1","2","3","4","5","6","7","8","9") :
                N_ID+=(x)

        print(N_ID)
        N_ID = int(N_ID)

        nb_product = len(link_pictures)
        list_position = 0

        while list_position < nb_product :
            print("rentre boucle")
            with connection.cursor() as cursor:
                sql = "INSERT INTO PRODUITS (`NOM`,`URL`,`NUTRISCORE`, `CATEGORIE_ID`) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (name[list_position], url[list_position], ns[list_position], N_ID))
                    
            connection.commit()
            list_position += 1
            print(list_position)
       
    def consult_product(name_categorie):
        print("Enregistrement de substituts")

        with connection.cursor() as cursor:

            sql = "SELECT PRODUITS.NOM, PRODUITS.ID FROM PRODUITS INNER JOIN CATEGORIES ON PRODUITS.CATEGORIE_ID = CATEGORIES.ID WHERE CATEGORIES.NOM = %s AND NUTRISCORE < 3 LIMIT 5"
            cursor.execute(sql, (name_categorie))
            result = cursor.fetchall()
            result = str(result)
            result = result.replace('{','\n')
            result = result.replace('}','')
            print(result)


        choice_substitut = input("\n Indiquer le numéro du produit que vous souhaitez consulter ")
        print(transition) 


class MainLoopBDD():
    def __init__(self, category_french="", category_english=""):
        self.category_french = category_french
        self.category_english = category_english

    def test_category_in_BDD(self):
        with connection.cursor() as cursor:
            sql = "SELECT NOM FROM `CATEGORIES`"
            cursor.execute(sql, ())
            category_exist_sql = cursor.fetchall()                    
            connection.commit()
        category_exist_list = []    
        
        for c in category_exist_sql :
            for d, e in c.items():
                category_exist_list.append(e)
        
        if self.category_french in category_exist_list :
            print("Catégorie existante")
            DownloadProduct.consult_product(name_categorie=self.category_french)
            return True

        else :
            print("Catégorie Nouvelle")
            with connection.cursor() as cursor:
                sql = "INSERT INTO CATEGORIES (`NOM`,`LINK_OFF`) VALUES (%s, %s)"
                cursor.execute(sql, (self.category_french, "lien hardcodé"))
            connection.commit()
            DownloadProduct.get_product(max_pages = 1, requête=self.category_english)
            DownloadProduct.consult_product(name_categorie=self.category_french)
            return False



class Consult():
    def consult_compare():
        """Class to consult products already registered by comparing with the initial product"""
        with connection.cursor() as cursor:
            sql = "SELECT INPUT_PRODUCT FROM `SUBSTITUTS` ORDER BY PRODUIT_ID"
            cursor.execute(sql, ())
            my_products = cursor.fetchall()                    
            connection.commit()

        with connection.cursor() as cursor:
            sql = "SELECT PRODUITS.NOM, PRODUITS.NUTRISCORE, PRODUITS.URL, PRODUITS.STORE FROM PRODUITS INNER JOIN SUBSTITUTS ON PRODUITS.ID = SUBSTITUTS.PRODUIT_ID"
            cursor.execute(sql, ())
            my_substituts = cursor.fetchall()
            connection.commit()

        index = -1
        for i in my_products :
            for j, k in i.items():
                print("\nPour remplacer : " + k)
                index += 1
                print(f"MON SUBSTITUT : {my_substituts[index]}")

class CleaningDB():
    """Class to clean the database with sql requests Delete and alter"""
    def cleaning_tables():
        """Deleting data with a python loop interacting with SQL"""
        with connection.cursor() as cursor:
            for t in TABLES:
                print(t)
                sql = "DELETE FROM %s;" %(t)
                cursor.execute(sql, ())
                connection.commit()
    
    def reset_counter():
        """resets the counters with auto_increment"""

        with connection.cursor() as cursor:
            for t in TABLES:
                sql = "ALTER TABLE %s AUTO_INCREMENT=0;" % (t)
                cursor.execute(sql, ())
                connection.commit()

class MainLoop(object):
    """Main loop of the program"""  
    continu = True
    transition = "\n"+"-"*204
    while continu:
        try :
            print(transition)
            terminal_mode = input("\n1 - Quel aliment souhaitez-vous remplacer ? \n2 - Retrouver mes aliments substitués. \n3 - Supprimer mes produits \n4 - exporter PDF \n5 - Sortir du programme ? \n \n>>> ")
            terminal_mode = int(terminal_mode)

            if terminal_mode == 1 :

                """ Select the category"""
                
                index_category = 1
                for keys, values in PRODUCTS.items():
                    print(str(index_category) + " " + keys)
                    index_category += 1
                user_category_choice = int(input("Choissisez le numéro de la catégorie de produits : "))
                user_category_choice -= 1
                print("\nVous avez choisi : " + list(PRODUCTS)[user_category_choice])
                user_category_choice = list(PRODUCTS)[user_category_choice]        
                category_to_english = CATEGORIES_TO_ENGLISH[user_category_choice]
                print(category_to_english)

                """Select The product"""

                index_products = 1
                for p in PRODUCTS[user_category_choice]:
                    print(str(index_products) + " " + p)
                    index_products += 1
                user_product_choice = int(input("Choissisez le numéro de produits : "))
                user_product_choice -= 1
                print("\n vous avez choisi : " + PRODUCTS[user_category_choice][user_product_choice])

                """Dowload the products"""
                MainLoopBDD(category_french = user_category_choice, category_english = category_to_english).test_category_in_BDD()


            if terminal_mode == 2 :
                Consult.consult_compare()

            if terminal_mode == 3 :
                verif_user = int(input("ëtes vous sûr de votre choix, cette action est irréversible ! \n 1 : OUI \n 2 : NON \n >>>"))

                if verif_user == 1 :
                    CleaningDB.cleaning_tables()
                    CleaningDB.reset_counter()
                    print("Base de données nettoyer ! ")
                else :
                    pass
                    print('Données restaurées ! ')
            if terminal_mode == 4 :
                ExportPdf.export()

            if terminal_mode == 5 :
                print("Merci d'utiliser notre programme, au revoir ! ")
                continu = False
        except ValueError :
            if len(terminal_mode) > 1 :
                print("\nOops! {} est un mot, veuillez recommencer : \n".format(terminal_mode))
            else :
                print("\nOops! {} est une lettre, veuillez recommencer : \n".format(terminal_mode))
MainLoop()
