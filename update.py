# -*- coding: utf-8 -*-
import pymysql
import pymysql.cursors
import re
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
        print("Erreur de connexion, veuillez vérifier les paramètres dans le fichier constants.py")

def sql_to_list(sql_=""):
    list_ID = []
    for d in sql_ :
        for key,val in d.items():
            print(val)
            list_ID.append(val)
    return list_ID


def delete_false():
    with connection.cursor() as cursor:
        sql = "SELECT PRODUITS.ID FROM PRODUITS INNER JOIN SUBSTITUTS ON PRODUITS.ID = SUBSTITUTS.PRODUIT_ID"
        cursor.execute(sql, ())
        PRODUIT_ID = cursor.fetchall()
        print(PRODUIT_ID)
        list_ID = sql_to_list(sql_=PRODUIT_ID)

        """Récupurer nombre produit"""
        sql_count = "SELECT MAX(ID) FROM PRODUITS"
        cursor.execute(sql_count, ())
        MAX_ID = cursor.fetchone()
        MAX_ID = MAX_ID.pop("MAX(ID)")
        print(type(MAX_ID))

        for i in range(1,MAX_ID+1) :
            if not i in list_ID :
                sql = "DELETE FROM PRODUITS WHERE ID=%s" % i
                print(sql)
                cursor.execute(sql, ())
                connection.commit()


delete_false()
"""
DELETE FROM `PRODUITS` WHERE `ID`
DELETE FROM PRODUITS INNER JOIN SUBSTITUTS ON PRODUITS.ID != SUBSTITUTS.PRODUIT_ID
Requête SQL selectionnant les ID des produits étant enregistrés comme substituts




DELETE FROM PRODUITS WHERE PRODUITS.ID NOT IN (SELECT PRODUITS.ID FROM PRODUITS INNER JOIN SUBSTITUTS ON PRODUITS.ID = SUBSTITUTS.PRODUIT_ID)"""