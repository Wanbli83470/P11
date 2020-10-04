import unittest  # Test tools
import glob  # The glob module finds all the pathnames
# matching a specified pattern according to the rules
import time  # time space
from P11_01_codesource import ExportPdf  # import of the function required for the test


class WidgetTestCase(unittest.TestCase):
    """Does PDF export work?"""
    def setUp(self):
        """Launch of an export"""
        print("\n\n      >>> 2 <<< ---------- TEST DE L'EXPORT PDF ---------- >>> 2 <<< \n\n")
        self.generate = ExportPdf.export()
        self.search_pdf = glob.glob("./*pdf")
        time.sleep(1.5)

    def test_exist(self):
        """Membership test"""
        if not self.search_pdf:
            search = False
            print("\n\n >>> 2 <<< Test échoué la liste est vide >>> 2 <<< \n\n")
        else:
            search = True
            print("\n\n >>> 2 <<< ---------- TEST DE L'EXPORT PDF OK ---------- >>> 2 <<< \n\n")
        self.assertEqual(search, True)

        time.sleep(2)
        print("\n"*50)


if __name__ == '__main__':
    unittest.main()
