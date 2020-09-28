import unittest #Test tools
import datetime #For get the date
from P11_01_codesource import update #My project

date_test = datetime.datetime.now()

"""standardize the date for the test"""

if date_test.day < 10 and date_test.month < 10:
    date_test = f"{date_test.year}-0{date_test.month}-0{date_test.day}"
    print(date_test)

elif date_test.month < 10:
    date_test = f"{date_test.year}-0{date_test.month}-{date_test.day}"
    print(date_test)

elif date_test.day < 10:
    date_test = f"{date_test.year}-{date_test.month}-0{date_test.day}"
    print(date_test)

else:
    date_test = f"{date_test.year}-{date_test.month}-{date_test.day}"
    print(date_test)

DATE_TEST = str(date_test)


class WidgetTestCase(unittest.TestCase):

    """Are the updates done? test by comparing the dates of the datetime module
     and the date recorded in DB"""

    def setUp(self):
        """Starting the update, and retrieving the date"""
        print("\n\n---------- TEST DE LA MISE À JOUR BDD ----------\n\n")
        self.date_control = update()

    def test_date(self):
        """Compare the SQL update date and today's date"""
        self.assertEqual(self.date_control, DATE_TEST)
        print("\n\n---------- TEST DE LA MISE À JOUR BDD OK ----------\n\n")



if __name__ == '__main__':
    unittest.main()
