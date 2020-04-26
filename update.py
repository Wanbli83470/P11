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

def delete_false():
    with connection.cursor() as cursor:
        sql = "SELECT PRODUITS.ID FROM PRODUITS INNER JOIN SUBSTITUTS ON PRODUITS.ID = SUBSTITUTS.PRODUIT_ID"
        cursor.execute(sql, ())
        count = cursor.fetchall()
        print(count)
        count = str(count)
        print(type(count))

        for i in range(1,2) :
            sql = "DELETE FROM PRODUITS WHERE ID=4"
            print(sql)
            cursor.execute(sql, ())
            connection.commit()


delete_false()
"""
DELETE FROM `PRODUITS` WHERE `ID`
DELETE FROM PRODUITS INNER JOIN SUBSTITUTS ON PRODUITS.ID != SUBSTITUTS.PRODUIT_ID
Requête SQL selectionnant les ID des produits étant enregistrés comme substituts




DELETE FROM PRODUITS WHERE PRODUITS.ID NOT IN (SELECT PRODUITS.ID FROM PRODUITS INNER JOIN SUBSTITUTS ON PRODUITS.ID = SUBSTITUTS.PRODUIT_ID)"""