# -*- coding: utf-8 -*-
import pymysql
import pymysql.cursors
import re
from constants import *
"""CONNECT TO THE DATABASE"""
from P11 import DownloadProduct
try :
    connection = pymysql.connect(host=HOST, #variable in file constantes.py
                                     user=USER,
                                     password=PASSWORD,
                                     db=DB,
                                     charset='utf8mb4',
                                     port = PORT,
                                     cursorclass=pymysql.cursors.DictCursor)
except :
        print("Erreur de connexion, veuillez vérifier les paramètres dans le fichier constants.py")

def sql_to_list(sql_=""):
    list_ID = []
    for d in sql_ :
        for key,val in d.items():
            list_ID.append(val)
    return list_ID


def update():
    with connection.cursor() as cursor:
        sql = "SELECT PRODUITS.ID FROM PRODUITS INNER JOIN SUBSTITUTS ON PRODUITS.ID = SUBSTITUTS.PRODUIT_ID"
        cursor.execute(sql, ())
        PRODUIT_ID = cursor.fetchall()
        list_ID_produit = sql_to_list(sql_=PRODUIT_ID)

        """Récupurer nombre produit"""
        sql_count = "SELECT MAX(ID) FROM PRODUITS"
        cursor.execute(sql_count, ())
        MAX_ID = cursor.fetchone()
        MAX_ID = MAX_ID.pop("MAX(ID)")

        for i in range(1,MAX_ID+1) :
            if not i in list_ID_produit :
                sql = "DELETE FROM PRODUITS WHERE ID=%s" % i
                cursor.execute(sql, ())
                connection.commit()

        """Récupérer les catégories en anglais"""
        print(">>> Récupération de vos catégories de produits")
        sql_get_category = "SELECT `NOM` FROM `CATEGORIES`"
        cursor.execute(sql_get_category, ())
        sql_link_category = cursor.fetchall()
        sql_link_category = sql_to_list(sql_=sql_link_category)
        temp = []
        while len(sql_link_category)>0:
            for l in sql_link_category :
                temp.append(CATEGORIES_TO_ENGLISH[sql_link_category.pop()])

        sql_link_category = temp
        """Télécharger les nouvelles données"""
        print(">>> Mise à jour de vos données")
        for i in sql_link_category :
            DownloadProduct.get_product(max_pages=1, requête=i)
        print(">>> Base de données actualisée")

update()