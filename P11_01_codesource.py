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
from P11_02_constantes import *
from connect import *

CONTINU = False
if __name__ == '__main__':  # pragma: no cover
    CONTINU = True


def sql_to_list(sql_=""):
    """Extract important data from SQL query"""
    list_id = []
    for d in sql_:
        for key, val in d.items():
            list_id.append(val)
    return list_id


def test_plural(vartest=""):
    """assign the plural mark according to the number"""
    if vartest > 1:
        return "s"
    else:
        return ""


class ExportPdf:
    """New program to export substitutes in PDF format"""
    def export():

        """recovery of the number of products with count
        and registration of substitutes in the PDF"""
        with connection.cursor() as cursor:
            sql = "SELECT COUNT(*) FROM SUBSTITUTS"
            cursor.execute(sql, ())
            count = cursor.fetchone()['COUNT(*)']
            connection.commit()

        name = input("Quelle est votre nom ? (Tapez 0 pour revenir à l'accueil !)\n>>> ")
        if name == "0":  # pragma: no cover
            terminal_mode = 0
        else:
            pdf = canvas.Canvas("substituts-{}.pdf".format(name))
            pdf.drawString(8*cm, 27*cm, u'{} produit{} enregistré{}'.format(count, test_plural(vartest=count),
                                                                            test_plural(vartest=count)))
            pdf.drawString(0.3*cm, 29*cm, u'Date de mon document : {}/{}/{}'.format(date_day.day, date_day.month,
                                                                                    date_day.year))
            pdf.line(8*cm, 26.8*cm, 12*cm, 26.8*cm)
            pdf.line(7.5*cm, 22.5*cm, 7.5*cm, 0*cm)
            pdf.line(14.5*cm, 22.5*cm, 14.5*cm, 0*cm)
            #Create the column

            pdf.drawString(2*cm, 21.5*cm, u'Mes habitudes')
            pdf.drawString(9.5*cm, 21.5*cm, u'Mes substituts')
            pdf.drawString(17*cm, 21.5*cm, u'Magasins')
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
                    if len(data_sub2[0]["NOM"]) > 30:  # pragma: no cover
                        pdf.drawString(7.6*cm, position*cm, str(data_sub2[0]["NOM"][:30] + "..."))
                    else:  # pragma: no cover
                        pdf.drawString(7.6*cm, position*cm, str(data_sub2[0]["NOM"]))

                pdf.drawString(2.5*cm, position*cm, s["INPUT_PRODUCT"])
                pdf.drawString(15.5*cm, position*cm, s["STORE"])
                pdf.line(0*cm, x_position*cm, 21*cm, y_position*cm)
                nb_line -= 1
                position -= 1
                x_position -= 1
                y_position -= 1

            if data_sub == ():  # pragma: no cover
                print("\nAttention votre document est vide ! Vous n'avez pas enregistré de produits")
            pdf.save()
            print("\nVotre PDF a bien été enregistré sous le nom : substituts-{}.pdf".format(name))


class MainLoopBDD:
    """BDD management class, response to a conditional structure"""
    def __init__(self, category_french="", category_english="", user_product=""):
        self.category_french = category_french
        self.category_english = category_english
        self.user_product = user_product

    def test_category_in_BDD(self):
        """Direction of the program according
        to the results of the condition"""
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
            print(self.category_french)
            print("Nouvelle catégorie de produits !")
            with connection.cursor() as cursor:
                sql = "INSERT INTO CATEGORIES (`NOM`,`LINK_OFF`) VALUES (%s, %s)"
                cursor.execute(sql, (self.category_french, link_off))
            connection.commit()
            DownloadProduct.get_product(max_pages=3, requete=self.category_english)
            DownloadProduct.save_substituts(name_categorie=self.category_french, user_product=self.user_product)
            return False


class DownloadProduct:
    """Class handling the downloading of files with the openfoodfacts API"""
    def get_product(max_pages=int, requete=""):
        # Creation list for BDD
        url, name, nutriscore, link_pictures = [], [], [], []
        dynamic_link = r.get("https://fr-en.openfoodfacts.org/category/{}/1.json".format(requete))
        info = dynamic_link.json()
        count = info['count']
        page_size = info['page_size']

        nb_pages = int(math.floor(int(count) / int(page_size)) + 1)  # On déduit le nombre de pages
        i, live_page = 0, 1
        while live_page <= nb_pages:
            dynamic_json = dynamic_link.json()
            for data in dynamic_json["products"]:

                # Filter produced with nutriscore

                if data["nutrition_grades_tags"] != ['not-applicable'] and data["nutrition_grades_tags"] != ['unknown']:
                    try:
                        if "url" in data and "product_name" in data and "image_url" in data and "nutrition_grades_tags" in data and "stores" in data:
                            url.append((data["url"]))
                            name.append((data["product_name"]))
                            nutriscore.append((data["nutrition_grades_tags"][0]))
                            link_pictures.append((data["image_url"]))
                            i = i + 1
                        else:
                            pass
                    # Deleting products without images

                    except KeyError:  # pragma: no cover
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
        try:  # pragma: no cover
            description = (product_substitut["product"]["ingredients_text_debug"])
        except KeyError as e:
            description = (product_substitut["product"]["ingredients_text_fr"])
        else:
            print("Ingrédient indisponibles")
        link_url = (product_substitut["product"]["image_front_url"])
        stores = (product_substitut["product"]["stores"])
        try :  # pragma: no cover

            if stores:  # pragma: no cover
                print("voici le produit " + product_name + "\n\n" + "Ce produit contient : " + description + "\n\n" + "\n\n" + "Il est disponible dans les magasins : " + stores )
            else:
                print("voici le produit " + product_name + "\n\n" + "Ce produit contient : " + description + "\n\n" + "\n\n" + "Nous n'avons pas trouvé de magasin le proposant." )

        except :
            print("Nous n'avons pas pu obtenir certains détail sur votre produit !")


        save_mode_substitut = True
        while save_mode_substitut:
            try:
                save_database = input("Voulez-vous enregistrer ce produit dans vos achats ? 1/oui ; 2/non ")
                save_database = int(save_database)
                if save_database == 1:
                    print("Enregistrement en cours...")
                    with connection.cursor() as cursor:
                        sql = "INSERT INTO SUBSTITUTS (`PRODUIT_ID`,`INPUT_PRODUCT`,`STORE`) VALUES (%s, %s, %s)"
                        if stores:  # pragma: no cover
                            cursor.execute(sql, (choice_substitut, user_product, stores))
                        else:  # pragma: no cover
                            cursor.execute(sql, (choice_substitut, user_product, "Magasin indisponible"))
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


class Consult:
    """Class to consult products already registered by comparing with the initial product"""
    def consult_compare():
        with connection.cursor() as cursor:
            sql = "SELECT INPUT_PRODUCT FROM `SUBSTITUTS` ORDER BY PRODUIT_ID"
            cursor.execute(sql, ())
            my_products = cursor.fetchall()
            connection.commit()
            sql = "SELECT ID FROM `SUBSTITUTS` ORDER BY PRODUIT_ID"
            cursor.execute(sql, ())
            my_products_id = cursor.fetchall()
            connection.commit()
            my_products_id = sql_to_list(sql_=my_products_id)
            sql = "SELECT PRODUITS.NOM, PRODUITS.NUTRISCORE FROM PRODUITS INNER JOIN SUBSTITUTS ON PRODUITS.ID = SUBSTITUTS.PRODUIT_ID ORDER BY PRODUIT_ID"
            cursor.execute(sql, ())
            my_substituts = cursor.fetchall()
            print(my_substituts)
            connection.commit()
        if my_substituts == ():  # pragma: no cover
            print("Vous n'avez pas encore enregistré de produits !")
            time.sleep(1.5)
            return 0

        index = -1
        for i in my_products:
            for j, k in i.items():
                print("\nPour remplacer : " + k + " ID = " + str(my_products_id[index+1]))
                index += 1
                print(f"MON SUBSTITUT : {my_substituts[index]}")

        time.sleep(1.5)
        return 0

class CleaningDB:
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
        """Single product delete function"""
        Consult.consult_compare()
        choice_id = input("Tapez l'ID du produit que vous souhaitez supprimer\n>>> ")
        with connection.cursor() as cursor:
            sql = "DELETE FROM `SUBSTITUTS` WHERE ID=%s" % choice_id
            cursor.execute(sql, ())
            connection.commit()
        return choice_id


def update():
    """Product update function"""
    with connection.cursor() as cursor:
        sql = "SELECT PRODUITS.ID FROM PRODUITS INNER JOIN SUBSTITUTS ON PRODUITS.ID = SUBSTITUTS.PRODUIT_ID"
        cursor.execute(sql, ())
        list_id_products = cursor.fetchall()
        list_id_products = sql_to_list(sql_=list_id_products)
        sql_count = "SELECT MAX(ID) FROM PRODUITS"
        cursor.execute(sql_count, ())
        max_id = cursor.fetchone()
        max_id = max_id.pop("MAX(ID)")
        sql_get_date = "SELECT `DATE` FROM `PRODUITS` WHERE ID=%s" % max_id
        cursor.execute(sql_get_date, ())
        sql_get_date = cursor.fetchone()["DATE"]
        sql_get_date = str(sql_get_date)
        sql_get_date = sql_get_date[:10]
        
        for i in range(1, max_id+1):
            if not i in list_id_products:
                sql = "DELETE FROM PRODUITS WHERE ID=%s" % i
                cursor.execute(sql, ())
                connection.commit()
        for r in TABLES:
            sql = "ALTER TABLE %s AUTO_INCREMENT=0;" % (r)
            cursor.execute(sql, ())
            connection.commit()

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
        print(">>> Mise à jour de vos données")
        for i in sql_link_category:
            DownloadProduct.get_product(max_pages=1, requete=i)
        print(f">>> Base de données actualisée le {sql_get_date}")
        return sql_get_date



class MainLoop:  # pragma: no cover
    """Main loop of the program"""
    terminal_mode = 0
    while CONTINU:  # pragma: no cover
        try:
            print(TRANSITION)
            terminal_mode = int(input("\n1 - Comment changer mon alimentation ? \n2 - Visualiser mon alimentation \n3 - Supprimer des produits \n4 - exporter un PDF imprimable \n5 - Sortir du programme ? \n6 - Mettre à jour mes produits ! \n>>> "))
            while terminal_mode == 1 and terminal_mode != 0:

                """ Select the category"""

                index_category = 1
                for keys, values in PRODUCTS.items():
                    print(str(index_category) + " " + keys)
                    index_category += 1
                return_accueil = index_category
                print(f"{return_accueil} Revenir à l'accueil ! ")
                user_category_choice = int(input("Choissisez le numéro de la catégorie de produits : "))
                if user_category_choice == return_accueil:
                    print("\n>>> Retour à l'accueil\n")
                    terminal_mode = 0
                else:
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

            while terminal_mode == 2:
                Visual_product = Consult.consult_compare()
                if Visual_product == 0:
                    terminal_mode = 0
                    print("\n>>> Retour à l'accueil")

            while terminal_mode == 3:
                choice_nb_products = int(input("1 - Supprimer tous les produits\n2 - Supprimer un produit\n3 - Revenir à l'accueil \n>>> "))
                if choice_nb_products == 1:
                    CleaningDB.cleaning_all_products()
                    print("Base de données nettoyée ! ")
                    terminal_mode = 0
                elif choice_nb_products == 2:
                    CleaningDB.cleaning_only_product()
                    print("Produit supprimé ! ")
                elif choice_nb_products >= 3:
                    terminal_mode = 0
                    print("\n>>> Retour à l'accueil")

            while terminal_mode == 4:
                ExportPdf.export()
                print(">>> Retour à l'accueil")
                terminal_mode = 0


            while terminal_mode == 5:
                print("Merci d'utiliser notre programme, au revoir ! ")
                terminal_mode = 0
                CONTINU = False

            while terminal_mode == 6:
                update()
                terminal_mode = 0

            while terminal_mode > 6:
                print("\nOops! {} n'est pas dans les propositions, veuillez recommencer : \n".format(terminal_mode))

        except ValueError:
            print("\nOops! Ce n'est pas un chiffre, veuillez recommencer :")
