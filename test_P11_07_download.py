import unittest #Test tools
import pymysql #mysql connection utility
import pymysql.cursors

from P11_01_codesource import DownloadProduct, MainLoopBDD #Function concerned by the test

from connect import *


class WidgetTestCase(unittest.TestCase):
    """Test the database cleaning"""
    

    def test_download(self):
        print("TEST DU TÉLÉCHARGEMENT DE DONNÉES OPEN FOOD FACT !")
        self.download = MainLoopBDD(category_french="Dessert", category_english="desserts", user_product="Œufs à la neige").test_category_in_BDD()
        print("\n\n---------- 1) LE PROGRAMME DETECTE-T-IL UNE CATÉGORIE NON EXISTANTE ----------\n\n")
        if self.assertEqual(self.download, False) == None :
            print("Test réussi ! le programme détecte que la catégorie n'existe pas")
        print("\n\n---------- 2) LE PROGRAMME A-T-IL BIEN TÉLÉCHARGÉ UNE CATÉGORIE DESSERT ? ----------\n\n")
        print("\n\n---------- 3) LE PROGRAMME A-T-IL BIEN TÉLÉCHARGÉ DES PRODUITS DE CETTE CATÉGORIE ? ----------\n\n")
        print("\n\n---------- 3) LE PROGRAMME A-T-IL BIEN ENREGISTRÉ UN SUBSTITUTS ? ----------\n\n")

    def test_existante(self):

        exist = MainLoopBDD(category_french="Dessert", category_english="desserts", user_product="Œufs à la neige").test_category_in_BDD()
        print("\n\n---------- 1) LE PROGRAMME DETECTE-T-IL LES CATÉGORIES EXISTANTES ? ----------\n\n")
        if self.assertEqual(exist, True) == None :
            print("Test réussi ! Le programme détecte une catégorie existante")



if __name__ == '__main__':
    unittest.main()
