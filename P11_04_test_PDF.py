import os
import unittest
import glob
import re
from P11_01_codesource import ExportPdf

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
        print("\n\n---------- TEST DE L'EXPORT PDF ----------\n\n")
        self.generate = ExportPdf.export()
        self.search_pdf = glob.glob("./*pdf")

    def test_exist(self):
        if not self.search_pdf:
            search = False
            print("Test échoué la liste est vide")
        else:
            search = True
            print("Test réussi, la liste contient un fichier pdf en sortie")
        self.assertEqual(search, True)

    def test_name_pdf(self):
        pass


if __name__ == '__main__':
    unittest.main()
