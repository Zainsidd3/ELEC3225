import unittest

from databaseFunctions import *

class Tests(unittest.TestCase):
    def test_successful_login(self):
        self.assertTrue(check_login_credentials("hamiltonm", "admin1"))

    def test_failed_login(self):
        self.assertFalse(check_login_credentials("hamiltonm", "wrongpassword"))

    def test_successful_add(self):
        self.assertTrue(add_to_roster(999, "001"))

    def test_add_to_invalid_CRN(self):
        self.assertFalse(add_to_roster(999, "NOTACRN"))
    
    def test_successful_removal(self):
        self.assertTrue(remove_from_roster(999, "001"))

    def test_remove_from_invalid_CRN(self):
        self.assertFalse(remove_from_roster(999, "NOTACRN"))

    def test_remove_student_not_in_roster(self):
        self.assertFalse(remove_from_roster(999, "002"))


if __name__ == '__main__':
    unittest.main()
