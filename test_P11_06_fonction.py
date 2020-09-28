import unittest #Test tools
import pymysql #mysql connection utility
import pymysql.cursors

from P11_01_codesource import test_plural as test_plural #Function concerned by the test
from P11_02_constantes import LOGIN_CONNECT, TABLES

try:
    connection = pymysql.connect(host=LOGIN_CONNECT["HOST"],
                                 user=LOGIN_CONNECT["USER"],
                                 password=LOGIN_CONNECT["PASSWORD"],
                                 db=LOGIN_CONNECT["DB"],
                                 charset='utf8mb4',
                                 port=LOGIN_CONNECT["PORT"],
                                 cursorclass=pymysql.cursors.DictCursor)

except:
    print("Erreur de connexion, veuillez vérifier les paramètres dans le fichier constants.py")


class WidgetTestCase(unittest.TestCase):
    """Test the database cleaning"""
    def setUp(self):
        print("\n\n---------- TEST DU PLURIEL ----------\n\n")
        """Start of cleaning"""
        self.result_test = test_plural(2)
        self.result_test2 = test_plural(1)
        print(self.result_test)
        

    def test_plural_(self):

        """SQL query for comparison"""
        if self.assertEqual(self.result_test, ("s")) :
            print("\n\n---------- TEST DU PLURIEL OK ----------\n\n")

    def test_singulier(self):
        if self.assertEqual(self.result_test2, ("")) :
            print("\n\n---------- TEST DU SINGULIER OK ----------\n\n")

if __name__ == '__main__':
    unittest.main()
