import os
import unittest
import glob
import re
import datetime
from P11_01_codesource import update
from P11_02_constantes import *

date_test = datetime.datetime.now()

if date_test.day < 10 and date_test.month < 10 :
    date_test = f"{date_test.year}-0{date_test.month}-0{date_test.day}"
    print(date_test)

elif date_test.month < 10 :
    date_test = f"{date_test.year}-0{date_test.month}-{date_test.day}"
    print(date_test)

elif date_test.day < 10 :
    date_test = f"{date_test.year}-{date_test.month}-0{date_test.day}"
    print(date_test)

else :
    date_test = f"{date_test.year}-{date_test.month}-{date_test.day}"
    print(date_test)

date_test = str(date_test)

class WidgetTestCase(unittest.TestCase):

    def setUp(self):
        print("\n\n---------- TEST DE LA MISE À JOUR ----------\n\n")
        self.date_control = update()

    def test_date(self):
        self.assertEqual(self.date_control, date_test)
        print("Test de l'actualisation BDD : OK")



if __name__ == '__main__':
    unittest.main()
