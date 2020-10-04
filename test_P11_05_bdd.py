import unittest  # Test tools
import time  # time space
from P11_01_codesource import CleaningDB  # Function concerned by the test

from connect import *


class WidgetTestCase(unittest.TestCase):
    """Test the database cleaning"""

    def setUp(self):
        """Start of cleaning"""
        print("\n\n       >>> 3 <<< ---------- TEST DU NETTOYAGE DE LA BASE DE DONNEES ---------- >>> 3 <<< \n\n")
        time.sleep(1.5)

    def test_clean_(self):
        id_clean = CleaningDB.cleaning_only_product()
        print(f"TEST NETTOYAGE UNITAIRE : {id_clean}")
        with connection.cursor() as cursor:
            sql = "SELECT `INPUT_PRODUCT` FROM `SUBSTITUTS` WHERE ID=%s" % id_clean
            cursor.execute(sql, ())
            clean_test = cursor.fetchone()

            if clean_test == None:
                print(f"La requête SQL du produit associé à l'ID n°{id_clean} est bien nulle !")
            else:
                print("Test échoué !")

            connection.commit()

            if self.assertEqual(clean_test, None) == None:
                print("\n\n >>> 3 <<< ---------- TEST NETTOYAGE UNITAIRE : OK ---------- >>> 3 <<< \n\n")
                time.sleep(1.5)

    def test_clean_all(self):
        """SQL query for comparison"""
        print("TEST NETTOYAGE INTÉGRALE")
        CleaningDB.cleaning_all_products()
        for t in TABLES:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM %s;" %(t)
                cursor.execute(sql, ())
                clean_test = cursor.fetchall()

                if clean_test == ():
                    print(f"{t} est bien vide, test réussi !")
                else:
                    print(f"{t} n'est pas vide, test échoué !")

                connection.commit()

            if self.assertEqual(clean_test, ()):
                print("\n\n >>> 3 <<< ---------- TEST DU NETTOYAGE DE LA BASE DE DONNEES OK ---------- >>> 3 <<< \n\n")

        time.sleep(2)
        print("\n"*50)


if __name__ == '__main__':
    unittest.main()
