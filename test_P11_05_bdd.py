import unittest #Test tools
import pymysql #mysql connection utility
import pymysql.cursors

from P11_01_codesource import CleaningDB #Function concerned by the test
from P11_02_constantes import LOGIN_CONNECT, TABLES

from connect import *


class WidgetTestCase(unittest.TestCase):
    """Test the database cleaning"""
    def setUp(self):
        """Start of cleaning"""
        print("\n\n---------- TEST DU NETTOYAGE DE LA BASE DE DONNEES ----------\n\n")
    
    def test_clean_(self):
        id_clean = CleaningDB.cleaning_only_product()
        print(f"Test nettoyage unitaire du produit : {id_clean}")
        with connection.cursor() as cursor:
            sql = "SELECT `INPUT_PRODUCT` FROM `SUBSTITUTS` WHERE ID=%s" % id_clean
            cursor.execute(sql, ())
            clean_test = cursor.fetchone()

            if clean_test == None:
                print(f"La requête SQL du produit associé à l'ID n°{id_clean} est bien nulle !")
            else:
                print("Test échoué !")

            connection.commit()

            if self.assertEqual(clean_test, None) == None :
                print("\n\n---------- TEST NETTOYAGE UNITAIRE : OK ----------\n\n")

    def test_clean_all(self):
        """SQL query for comparison"""
        print("Test nettoyage intégral")
        CleaningDB.cleaning_all_products()
        for t in TABLES:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM %s;" %(t)
                cursor.execute(sql, ())
                clean_test = cursor.fetchall()
                print(clean_test)

                if clean_test == ():
                    print(f"{t} est bien vide, test réussi !")
                else:
                    print(f"{t} n'est pas vide, test échoué !")

                connection.commit()

            if self.assertEqual(clean_test, ()) :
                print("\n\n---------- TEST DU NETTOYAGE DE LA BASE DE DONNEES OK ----------\n\n")


if __name__ == '__main__':
    unittest.main()
