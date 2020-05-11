import unittest
import re
import pymysql
import pymysql.cursors

from P11_01_codesource import CleaningDB
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


class WidgetTestCase(unittest.TestCase):
    def setUp(self):
        self.cleaning = CleaningDB.cleaning_all_products()
        print("\n\n---------- TEST DU NETTOYAGE DE LA BASE DE DONNEES ----------\n\n")

    def test_clean(self):
        for t in TABLES:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM %s;" %(t)
                cursor.execute(sql, ())
                clean_test = cursor.fetchall()
                print(clean_test)

                if clean_test == ():
                    print(f"{t} est bien vide, test réussi !")
                else :
                    print(f"{t} n'est pas vide, test échoué !")

                connection.commit()
            self.assertEqual(clean_test, ())

    def test_reset_counter(self):
        pass


if __name__ == '__main__':
    unittest.main()
