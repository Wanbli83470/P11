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

import requests
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

    def test_category_in_BDD(user_category = str):
        with connection.cursor() as cursor:
            sql = "SELECT NOM FROM `CATEGORIES`"
            cursor.execute(sql, ())
            category_exist_sql = cursor.fetchall()                    
            connection.commit()
        category_exist_list = []    
        
        for c in category_exist_sql :
            for d, e in c.items():
                category_exist_list.append(e)
        
        if user_category in category_exist_list :
            print("Catégorie existante")
            return True

        else :
            print("Catégorie Nouvelle")
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

class Main(object):
    """Main loop of the program"""  
    continu = True
    transition = "\n"+"-"*204
    while continu:
        try :
            print(transition)
            terminal_mode = input("\n1 - Quel aliment souhaitez-vous remplacer ? \n2 - Retrouver mes aliments substitués. \n3 - Sortir du programme ? \n4 - exporter PDF \n5 - Nettoyer la Base de données\n \n>>> ")
            terminal_mode = int(terminal_mode)

            if terminal_mode == 1 :

                index_category = 1
                for keys, values in PRODUCTS.items():
                    print(str(index_category) + " " + keys)
                    index_category += 1
                # print(PRODUCTS)
                user_category_choice = int(input("Choissisez le numéro de la catégorie de produits : "))
                user_category_choice -= 1
                print("Vous avez choisi : " + list(PRODUCTS)[user_category_choice])
                user_category_choice = list(PRODUCTS)[user_category_choice]        
                DownloadProduct.test_category_in_BDD(user_category = user_category_choice)


            if terminal_mode == 2 :
                Consult.consult_compare()


            if terminal_mode == 3 :
                continu = False

            if terminal_mode == 4 :
                ExportPdf.export()

            if terminal_mode == 5 :
                CleaningDB.cleaning_tables()
                CleaningDB.reset_counter()
        except ValueError :
            if len(terminal_mode) > 1 :
                print("\nOops! {} est un mot, veuillez recommencer : \n".format(terminal_mode))
            else :
                print("\nOops! {} est une lettre, veuillez recommencer : \n".format(terminal_mode))
Main()
