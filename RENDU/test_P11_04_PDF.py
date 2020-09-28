import unittest #Test tools
import glob #The glob module finds all the pathnames matching a specified pattern according to the rules
from P11_01_codesource import ExportPdf #import of the function required for the test


class WidgetTestCase(unittest.TestCase):
    """Does PDF export work?"""
    def setUp(self):
        """Launch of an export"""
        print("\n\n---------- TEST DE L'EXPORT PDF ----------\n\n")
        self.generate = ExportPdf.export()
        self.search_pdf = glob.glob("./*pdf")

    def test_exist(self):
        """Membership test"""
        if not self.search_pdf:
            search = False
            print("Test échoué la liste est vide")
        else:
            search = True
            print("Test réussi, la liste contient un fichier pdf en sortie")
            print("\n\n---------- TEST DE L'EXPORT PDF OK ----------\n\n")
        self.assertEqual(search, True)


if __name__ == '__main__':
    unittest.main()
