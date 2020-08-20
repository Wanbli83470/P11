import os
import unittest
import glob
import re
import datetime
from P11_01_codesource import update as test_update
from P11_02_constantes import *

date_test = datetime.datetime.now()
if date_test.month < 10 :

    print(date_test)

elif date_test.day < 10 :
    print(date_test)
    
else :
    date_test = f"{date_test.year}-{date_test.month}-{date_test.day}"
    print(date_test)

"""class WidgetTestCase(unittest.TestCase):

    def setUp(self):
        print("\n\n---------- TEST DE LA MISE À JOUR ----------\n\n")
        date_test = test_update()
        with connection.cursor() as cursor:
            date_control = "SELECT `DATE` FROM `PRODUITS` WHERE ID = 1"
            cursor.execute(date_control, ())

    def test_date(self):
        print(connection)
        self.assertEqual(search, date_test)

if __name__ == '__main__':
    unittest.main()"""
