import unittest #Test tools
import pymysql #mysql connection utility
import pymysql.cursors
import time

from P11_01_codesource import test_plural as test_plural, sql_to_list #Function concerned by the test

from connect import *


class WidgetTestCase(unittest.TestCase):
    """Test the database cleaning"""
    def setUp(self):
        time.sleep(1.5)
        """Start of cleaning"""
        self.plural = test_plural(2)
        self.singulier = test_plural(1)
        tri_data = [{'NOM': 'Boisson'}, {'NOM': 'Gâteaux/Sucrerie'}]
        self.tri_sql = sql_to_list(tri_data)

    def test_plural_(self):
        print("\n\n       >>> 4 <<< ---------- TESTS FONCTIONS DIVERSES ---------- >>>  4 <<< \n\n")
        print("\n\n       >>> 4 <<< ---------- TEST DU PLURIEL ---------- >>> 4 <<< \n\n")
        time.sleep(1.5)
        """SQL query for comparison"""
        if self.assertEqual(self.plural, ("s")) == None:
            print(" >>> 4 <<< ---------- TEST DU PLURIEL : OK ---------- >>> 4 <<<")
            time.sleep(1.5)


    def test_singulier(self):
        print("\n\n       >>> 4 <<< ---------- TEST DU SINGULIER ---------- >>> 4 <<< \n\n")
        time.sleep(1.5)
        if self.assertEqual(self.singulier, ("")) == None:
            print("\n\n >>> 4 <<< ---------- TEST DU SINGULIER : OK >>> 4 <<< ---------- \n\n")
            time.sleep(1.5)

    def test_tri_sql(self):
        print("TEST TRI DE DONNÉES")
        time.sleep(1.5)
        if self.assertEqual(self.tri_sql, (['Boisson', 'Gâteaux/Sucrerie'])) == None:
            print("\n\n >>> 4 <<< ---------- TEST TRI DE DONNÉES : OK ! >>> 4 <<< ---------- \n\n")
        time.sleep(2)
        print("\n"*50)
if __name__ == '__main__':
    unittest.main()
