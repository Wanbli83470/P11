# -*- coding: utf-8 -*-
import pymysql
import pymysql.cursors
import re
from constants import *
"""CONNECT TO THE DATABASE"""
from P11 import DownloadProduct, update, sql_to_list
import time
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

update()