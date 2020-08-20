#!/usr/bin/python
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
import json
import time
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import requests as r
import pymysql
import pymysql.cursors
from P11_02_constantes import *

continu = False
if __name__ == '__main__':
    continu = True

try:
    connection = pymysql.connect(host=LOGIN_CONNECT["HOST"],
                                 user=LOGIN_CONNECT["USER"],
                                 password=LOGIN_CONNECT["PASSWORD"],
                                 db=LOGIN_CONNECT["DB"],
                                 charset='utf8mb4',
                                 port=LOGIN_CONNECT["PORT"],
                                 cursorclass=pymysql.cursors.DictCursor)
    print(">>> Connexion réussie !")

except:
    print("Erreur de connexion, veuillez vérifier les paramètres dans le fichier constants.py")


def sql_to_list(sql_=""):
    list_id = []
    for d in sql_:
        for key, val in d.items():
            list_id.append(val)
    return list_id


def test_plural(vartest: ""):
    if vartest > 1:
        return "s"
    else:
        return ""


class ExportPdf:
    """New program to export substitutes in PDF format"""
    def export():
        """recovery of the number of products with count and registration of substitutes in the PDF"""
        with connection.cursor() as cursor:
            sql = "SELECT COUNT(*) FROM SUBSTITUTS"
            cursor.execute(sql, ())
            count = cursor.fetchone()['COUNT(*)']
            connection.commit()

        name = input("Quelle est votre nom ? \n>>> ")
        pdf = canvas.Canvas("substituts-{}.pdf".format(name))
        pdf.drawString(3*cm, 28*cm, u'Bienvenue {} vous avez enregistré {} produit{}'.format(name, count, test_plural(vartest=count)))
        pdf.line(7.5*cm, 23*cm, 7.5*cm, 0*cm)
        pdf.line(14.5*cm, 23*cm, 14.5*cm, 0*cm)
        #Create the column

        pdf.drawString(2*cm, 23.5*cm, u'Mes habitudes')
        pdf.drawString(9.5*cm, 23.5*cm, u'Mes substituts')
        pdf.drawString(17*cm, 23.5*cm, u'Magasins')
        #Create the lines
        nb_line, x_position, y_position = 21, 21, 21

        #Get the input_product from table SUBSTITUTS from Database
        with connection:
            cur = connection.cursor()
            cur.execute("SELECT INPUT_PRODUCT, PRODUIT_ID, STORE FROM SUBSTITUTS")
            data_sub = cur.fetchall()

        position = 20.4
        for s in data_sub:

            with connection:
                cur = connection.cursor()
                cur.execute("SELECT NOM FROM PRODUITS WHERE ID=%s" % (int(s["PRODUIT_ID"])))
                data_sub2 = cur.fetchall()
                pdf.drawString(9*cm, position*cm, str(data_sub2[0]["NOM"]))

            pdf.drawString(2.5*cm, position*cm, s["INPUT_PRODUCT"])
            pdf.drawString(15.5*cm, position*cm, s["STORE"])
            pdf.line(0*cm, x_position*cm, 21*cm, y_position*cm)
            nb_line -= 1
            position -= 1
            x_position -= 1
            y_position -= 1

        #Get the substituts from table SUBSTITUS from Database

        pdf.save()
        print("\nVotre PDF a bien été enregistré sous le nom : substituts-{}.pdf".format(name))


class MainLoopBDD:
    def __init__(self, category_french="", category_english="", user_product=""):
        self.category_french = category_french
        self.category_english = category_english
        self.user_product = user_product

    def test_category_in_BDD(self):
        with connection.cursor() as cursor:
            sql = "SELECT NOM FROM `CATEGORIES`"
            cursor.execute(sql, ())
            category_exist_sql = cursor.fetchall()
            connection.commit()
        category_exist_list = []

        for c in category_exist_sql:
            for d, e in c.items():
                category_exist_list.append(e)

        if self.category_french in category_exist_list:
            print("Catégorie existante")
            DownloadProduct.save_substituts(name_categorie=self.category_french, user_product=self.user_product)
            return True

        else:
            link_off = "https://fr-en.openfoodfacts.org/category/{}.json".format(self.category_english)
            print("Nouvelle catégorie de produits !")
            with connection.cursor() as cursor:
                sql = "INSERT INTO CATEGORIES (`NOM`,`LINK_OFF`) VALUES (%s, %s)"
                cursor.execute(sql, (self.category_french, link_off))
            connection.commit()
            DownloadProduct.get_product(max_pages=3, requete=self.category_english)
            DownloadProduct.save_substituts(name_categorie=self.category_french, user_product=self.user_product)
            return False


class DownloadProduct:

    def get_product(max_pages=int, requete=""):
        # Creation list for BDD
        url, name, nutriscore, link_pictures = [], [], [], []
        dynamic_link = r.get("https://fr-en.openfoodfacts.org/category/{}/1.json".format(requete))
        info = dynamic_link.json()
        count = info['count']
        page_size = info['page_size']

        nb_pages = int(math.floor(count / page_size) + 1)  # On déduit le nombre de pages
        i, live_page = 0, 1
        while live_page <= nb_pages:
            dynamic_json = dynamic_link.json()
            for data in dynamic_json["products"]:

                # Filter produced with nutriscore

                if data["nutrition_grades_tags"] != ['not-applicable'] and data["nutrition_grades_tags"] != ['unknown']:
                    try:
                        url.append((data["url"]))
                        name.append((data["product_name"]))
                        nutriscore.append((data["nutrition_grades_tags"][0]))
                        link_pictures.append((data["image_url"]))
                        i += 1

                    # Deleting products without images

                    except KeyError:
                        digit = i
                        del url[digit]
                        del name[digit]
                        del nutriscore[digit]

            live_page += 1
            dynamic_link = r.get("https://fr-en.openfoodfacts.org/category/{}/{}.json".format(requete, live_page))
            if live_page > max_pages:
                break

            # Convert number to letters
        ns_dico = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
        ns_sort = [ns_dico[i] for i in nutriscore]
        nutriscore = ns_sort
        del ns_sort

        with connection.cursor() as cursor:
            sql = "SELECT MAX(`ID`) FROM CATEGORIES"
            cursor.execute(sql, ())
            id_category = cursor.fetchone()['MAX(`ID`)']

        nb_product = len(link_pictures)
        list_position = 0

        while list_position < nb_product:
            with connection.cursor() as cursor:
                sql = "INSERT INTO PRODUITS (`NOM`,`URL`,`NUTRISCORE`, `CATEGORIE_ID`) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (name[list_position], url[list_position], nutriscore[list_position], id_category))

            connection.commit()
            list_position += 1
        del url, name, nutriscore, link_pictures

    def save_substituts(name_categorie, user_product):
        print(">>>>>> Nos propositions de substituts ci dessous ! <<<<<<<<<")

        with connection.cursor() as cursor:

            sql = "SELECT PRODUITS.NOM, PRODUITS.ID FROM PRODUITS INNER JOIN CATEGORIES ON PRODUITS.CATEGORIE_ID = CATEGORIES.ID WHERE CATEGORIES.NOM = %s AND NUTRISCORE < 3 LIMIT 5"
            cursor.execute(sql, (name_categorie))
            result = str(cursor.fetchall())
            result = result.replace('{', '\n')
            result = result.replace('}', '')
            print(result)

        choice_substitut = input("\n Indiquer le numéro du produit que vous souhaitez consulter ")
        print(TRANSITION)

        with connection.cursor() as cursor:

            sql = "SELECT `URL` FROM PRODUITS WHERE `ID`=%s"
            cursor.execute(sql, (choice_substitut))
            link_result = cursor.fetchone()

        link_result = link_result['URL']
        n_link = ''
        for x in link_result:
            if x in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"):
                n_link += x
                if len(n_link) == 13:
                    break

        link_url = "https://fr.openfoodfacts.org/api/v0/produit/{}.json".format(n_link)
        print(link_url)
        ri = r.get(link_url)
        product_substitut = json.loads(ri.text)
        product_name = (product_substitut["product"]["product_name"])
        description = (product_substitut["product"]["ingredients_text_debug"])
        link_url = (product_substitut["product"]["image_front_url"])
        stores = (product_substitut["product"]["stores"])

        print("voici le produit " + product_name + "\n\n" + "Ce produit contient : " + description + "\n\n" + " vous pouvez retrouver le lien ici même : " + link_url + "\n\n" + "Il est disponible dans les magasins : " + stores )

        save_mode_substitut = True
        while save_mode_substitut:
            try:
                save_database = input("Voulez-vous enregistrer ce produit dans vos achats ? 1/oui ; 2/non ")
                save_database = int(save_database)
                if save_database == 1:
                    print("Enregistrement en cours...")
                    with connection.cursor() as cursor:
                        sql = "INSERT INTO SUBSTITUTS (`PRODUIT_ID`,`INPUT_PRODUCT`,`STORE`) VALUES (%s, %s, %s)"
                        cursor.execute(sql, (choice_substitut, user_product, stores))
                        connection.commit()
                    print("enregistrement terminé !")
                    save_mode_substitut = False
                elif save_database == 2:
                    print("\nenregistrement non effectué, \n>>>retour vers le menu")
                    save_mode_substitut = False
                elif save_database > 2:
                    print("\n{} n'est pas dans les numéros proposés\n".format(save_database))
            except ValueError:
                if len(save_database) > 1:
                    print("\nOops! {} est un mot, veuillez recommencer : \n".format(save_database))
                else:
                    print("\nOops! {} est une lettre, veuillez recommencer : \n".format(save_database))


class Consult():

    def consult_compare():

        """Class to consult products already registered by comparing with the initial product"""
        with connection.cursor() as cursor:
            sql = "SELECT INPUT_PRODUCT FROM `SUBSTITUTS` ORDER BY PRODUIT_ID"
            cursor.execute(sql, ())
            my_products = cursor.fetchall()
            connection.commit()
            """Select product_id for present the comparaison"""
            sql = "SELECT ID FROM `SUBSTITUTS` ORDER BY PRODUIT_ID"
            cursor.execute(sql, ())
            my_products_id = cursor.fetchall()
            connection.commit()
            my_products_id = sql_to_list(sql_=my_products_id)
            """Select caracteristics of my substituts"""
            sql = "SELECT PRODUITS.NOM, PRODUITS.NUTRISCORE FROM PRODUITS INNER JOIN SUBSTITUTS ON PRODUITS.ID = SUBSTITUTS.PRODUIT_ID ORDER BY PRODUIT_ID"
            cursor.execute(sql, ())
            my_substituts = cursor.fetchall()
            connection.commit()
        if my_substituts == ():
            print("Vous n'avez pas encore enregistré de produits !")
            time.sleep(1.5)
        index = -1
        for i in my_products:
            for j, k in i.items():
                print("\nPour remplacer : " + k + " ID = " + str(my_products_id[index+1]))
                index += 1
                print(f"MON SUBSTITUT : {my_substituts[index]}")


class CleaningDB():

    """Class to clean the database with sql requests Delete and alter"""
    def cleaning_all_products():
        """Deleting data with a python loop interacting with SQL"""
        with connection.cursor() as cursor:
            for delete in TABLES:
                sql = "DELETE FROM %s;" %(delete)
                cursor.execute(sql, ())
                connection.commit()
            """resets the counters with auto_increment"""
            for reset in TABLES:
                sql = "ALTER TABLE %s AUTO_INCREMENT=0;" % (reset)
                cursor.execute(sql, ())
                connection.commit()

    def cleaning_only_product():
        Consult.consult_compare()
        choice_id = input("Tapez l'ID du produit que vous souhaitez supprimer\n>>> ")
        with connection.cursor() as cursor:
            sql = "DELETE FROM `SUBSTITUTS` WHERE ID=%s" % choice_id
            cursor.execute(sql, ())
            connection.commit()


def update():
    with connection.cursor() as cursor:
        sql = "SELECT PRODUITS.ID FROM PRODUITS INNER JOIN SUBSTITUTS ON PRODUITS.ID = SUBSTITUTS.PRODUIT_ID"
        cursor.execute(sql, ())
        list_id_products = cursor.fetchall()
        list_id_products = sql_to_list(sql_=list_id_products)

        """Récupurer nombre produit"""
        sql_count = "SELECT MAX(ID) FROM PRODUITS"
        cursor.execute(sql_count, ())
        max_id = cursor.fetchone()
        max_id = max_id.pop("MAX(ID)")

        for i in range(1, max_id+1):
            if not i in list_id_products:
                sql = "DELETE FROM PRODUITS WHERE ID=%s" % i
                cursor.execute(sql, ())
                connection.commit()
        for r in TABLES:
            sql = "ALTER TABLE %s AUTO_INCREMENT=0;" % (r)
            cursor.execute(sql, ())
            connection.commit()

        """Récupérer les catégories en anglais"""
        print(">>> Récupération de vos catégories de produits")
        time.sleep(3)
        sql_get_category = "SELECT `NOM` FROM `CATEGORIES`"
        cursor.execute(sql_get_category, ())
        sql_link_category = cursor.fetchall()
        sql_link_category = sql_to_list(sql_=sql_link_category)
        temp = []
        while len(sql_link_category) > 0:
            for l in sql_link_category:
                temp.append(CATEGORIES_TO_ENGLISH[sql_link_category.pop()])

        sql_link_category = temp
        del temp
        """Télécharger les nouvelles données"""
        print(">>> Mise à jour de vos données")
        for i in sql_link_category:
            DownloadProduct.get_product(max_pages=1, requete=i)
        print(">>> Base de données actualisée")
        sql_get_date = "SELECT `DATE` FROM `PRODUITS` WHERE ID=%s" % "1"
        cursor.execute(sql_get_date, ())
        sql_get_date = cursor.fetchone()["DATE"]
        sql_get_date = str(sql_get_date)
        print(sql_get_date)
        return sql_get_date


class MainLoop:
    """Main loop of the program"""
    while continu:
        try:
            print(TRANSITION)
            terminal_mode = int(input("\n1 - Quel aliment souhaitez-vous remplacer ? \n2 - Retrouver mes aliments substitués. \n3 - Supprimer des produits \n4 - exporter un PDF imprimable \n5 - Sortir du programme ? \n6 - Mettre à jour mes produits ! \n>>> "))
            if terminal_mode == 1:

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
                name_product_choice = PRODUCTS[user_category_choice][user_product_choice]
                """Dowload the products"""
                MainLoopBDD(category_french=user_category_choice, category_english=category_to_english, user_product=name_product_choice).test_category_in_BDD()

            elif terminal_mode == 2:
                Consult.consult_compare()

            elif terminal_mode == 3:
                choice_nb_products = int(input("1 - Supprimer tous les produits\n2 - Supprimer un produit\n3 - Revenir à l'accueil \n>>> "))
                if choice_nb_products == 1:
                    CleaningDB.cleaning_all_products()
                    print("Base de données nettoyée ! ")
                elif choice_nb_products == 2:
                    CleaningDB.cleaning_only_product()
                    print("Produit supprimé ! ")
                else:
                    print('Données restaurées ! ')
            elif terminal_mode == 4:
                ExportPdf.export()

            elif terminal_mode == 5:
                print("Merci d'utiliser notre programme, au revoir ! ")
                continu = False

            elif terminal_mode == 6:
                update()

            elif terminal_mode > 6 or terminal_mode < 1:
                print("\nOops! {} n'est pas dans les propositions, veuillez recommencer : \n".format(terminal_mode))

        except ValueError:
            print("\nOops! Ce n'est pas un chiffre, veuillez recommencer :")
