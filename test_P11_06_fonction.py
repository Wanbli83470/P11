import unittest #Test tools
import pymysql #mysql connection utility
import pymysql.cursors

from P11_01_codesource import test_plural as test_plural, sql_to_list #Function concerned by the test

from connect import *


class WidgetTestCase(unittest.TestCase):
    """Test the database cleaning"""
    def setUp(self):
        
        """Start of cleaning"""
        self.plural = test_plural(2)
        self.singulier = test_plural(1)
        tri_data = [{'NOM': 'Boisson'}, {'NOM': 'Gâteaux/Sucrerie'}]
        self.tri_sql = sql_to_list(tri_data)

    def test_plural_(self):
        print("\n\n---------- TEST DU PLURIEL ----------\n\n")
        """SQL query for comparison"""
        if self.assertEqual(self.plural, ("s")) == None:
            print("Test pluriel concluant !")


    def test_singulier(self):
        print("\n\n---------- TEST DU SINGULIER ----------\n\n")
        if self.assertEqual(self.singulier, ("")) == None:
            print("Test singulier concluant !")

    def test_tri_sql(self):
        print("TEST TRI SQL")
        if self.assertEqual(self.tri_sql, (['Boisson', 'Gâteaux/Sucrerie'])) == None:
            print("TEST TRI SQL OK !")
if __name__ == '__main__':
    unittest.main()
