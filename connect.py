"""Use the pymysql for connect to local Database"""
import pymysql
import pymysql.cursors
from constants import LOGIN_CONNECT as C

try:
    connection = pymysql.connect(host=C["HOST"],
                                 user=C["USER"],
                                 password=C["PASSWORD"],
                                 db=C["DB"],
                                 charset='utf8mb4',
                                 port=C["PORT"],
                                 cursorclass=pymysql.cursors.DictCursor)
    print(">>> Connexion réussie !")

except:
    print("Erreur de connexion, veuillez vérifier les paramètres dans le fichier constants.py")
