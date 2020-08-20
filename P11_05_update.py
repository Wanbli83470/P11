# -*- coding: utf-8 -*-
import pymysql
import pymysql.cursors
import time
from P11_01_codesource import *
"""CONNECT TO THE DATABASE"""
from P11_02_constantes import *


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
            DownloadProduct.get_product(max_pages=2, requete=i)
        print(">>> Base de données actualisée")


if __name__ == '__main__':
    update()
