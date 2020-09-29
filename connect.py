import pymysql
import pymysql.cursors
from P11_02_constantes import *

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

