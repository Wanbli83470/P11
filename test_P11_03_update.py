import unittest  # Test tools
import time  # time space
from P11_01_codesource import update  # My project
from P11_02_constantes import date_day  # My project


if date_day.day < 10 and date_day.month < 10:
    date_day = f"{date_day.year}-0{date_day.month}-0{date_day.day}"
    print(date_day)

elif date_day.month < 10:
    date_day = f"{date_day.year}-0{date_day.month}-{date_day.day}"
    print(date_day)

elif date_day.day < 10:
    date_day = f"{date_day.year}-{date_day.month}-0{date_day.day}"
    print(date_day)

else:
    date_day = f"{date_day.year}-{date_day.month}-{date_day.day}"
    print(date_day)

DATE_TEST = str(date_day)


class WidgetTestCase(unittest.TestCase):

    """Are the updates done? test by comparing the dates of the datetime module
     and the date recorded in DB"""

    def setUp(self):
        """Starting the update, and retrieving the date"""
        print("\n\n      >>> 1 <<< ---------- TEST DE LA MISE À JOUR BDD ---------- >>> 1 <<< \n\n")
        self.date_control = update()

    def test_date(self):
        """Compare the SQL update date and today's date"""
        self.assertEqual(self.date_control, DATE_TEST)
        print("\n\n >>> 1 <<< ---------- TEST DE LA MISE À JOUR BDD OK ---------- >>> 1 <<< \n\n")
        time.sleep(2)
        print("\n"*50)


if __name__ == '__main__':
    unittest.main()
