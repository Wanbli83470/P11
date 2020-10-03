import unittest #Test tools
import pymysql #mysql connection utility
import pymysql.cursors
import time
from P11_01_codesource import DownloadProduct, MainLoopBDD #Function concerned by the test

from connect import *

class WidgetTestCase(unittest.TestCase):
    """Test the database cleaning"""
    

    def test_download(self):
        print("TEST DU TÉLÉCHARGEMENT DE DONNÉES OPEN FOOD FACT !")
        self.download = MainLoopBDD(category_french="Dessert", category_english="desserts", user_product="Œufs à la neige").test_category_in_BDD()
        print("\n\n       >>> 5 <<< ----------LE PROGRAMME DETECTE-T-IL UNE CATÉGORIE NON EXISTANTE ? ---------- >>> 5 <<< \n\n")
        if self.assertEqual(self.download, False) == None :
            print("\n\n---------- TEST RÉUSSSI : DETECTION D'UNE CATÉGORIE NON EXISTANTE EN BDD : OK ---------- >>> 5 <<< \n\n")
        print("\n\n       >>> 5 <<< ----------LE PROGRAMME A-T-IL BIEN TÉLÉCHARGÉ UNE CATÉGORIE DESSERT ? ---------- >>> 5 <<< \n\n")
        print("\n\n       >>> 5 <<< ----------LE PROGRAMME A-T-IL BIEN TÉLÉCHARGÉ DES PRODUITS DE CETTE CATÉGORIE ? ---------- >>> 5 <<< \n\n")
        print("\n\n       >>> 5 <<< ----------LE PROGRAMME A-T-IL BIEN ENREGISTRÉ UN SUBSTITUT ? ---------- >>> 5 <<< \n\n")

    def test_existante(self):

        exist = MainLoopBDD(category_french="Dessert", category_english="desserts", user_product="Œufs à la neige").test_category_in_BDD()
        print("\n\n >>> 5 <<< ---------- LE PROGRAMME DETECTE-T-IL LES CATÉGORIES EXISTANTES ? ---------- >>> 5 <<< \n\n")
        if self.assertEqual(exist, True) == None :
            print("\n\n >>> 5 <<< ---------- TEST RÉUSSSI : DETECTION D'UNE CATÉGORIE EXISTANTE EN BDD : OK ---------- >>> 5 <<< \n\n")
        time.sleep(2)
        print("\n"*50)


if __name__ == '__main__':
    unittest.main()
