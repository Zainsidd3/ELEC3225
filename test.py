import unittest

from databaseFunctions import *


class Tests(unittest.TestCase):
    def test_successful_login(self):              # Test successful login with correct credentials
        self.assertTrue(check_login_credentials("hamiltonm", "admin1"))

    def test_failed_login(self):                  # Test failed login with incorrect password
        self.assertFalse(check_login_credentials("hamiltonm", "wrongpassword"))

    def test_successful_add(self):                # Test successful addition of a student to a course roster
        self.assertTrue(add_to_roster(999, "001"))

    def test_add_to_invalid_CRN(self):            # Test addition to an invalid CRN
        self.assertFalse(add_to_roster(999, "NOTACRN"))

    def test_successful_removal(self):            # Test successful removal of a student from a course roster
        self.assertTrue(remove_from_roster(999, "001"))

    def test_remove_from_invalid_CRN(self):       # Test removal from an invalid CRN
        self.assertFalse(remove_from_roster(999, "NOTACRN"))

    def test_remove_student_not_in_roster(self): # Test removal of a student not in the course roster
        self.assertFalse(remove_from_roster(999, "002"))

    def test_successful_course_search(self):     # Test successful search for a course

        self.assertTrue(len(search("COURSE", "CRN", "001")) == 1)

    def test_failed_course_search(self):         # Test failed search for a non-existent course
        self.assertTrue(len(search("COURSE", "CRN", "999")) == 0)

    def test_invalid_table_search(self):         # Test search on an invalid table name
        with self.assertRaises(TypeError):
            search("NOTATABLE", "CRN", "001")

    def test_invalid_attribute_search(self):    # Test search with an invalid attribute
        with self.assertRaises(TypeError):
            search("COURSE", "AAAAA", "001")

    def test_successful_add_course(self):       # Test successful addition of a course
        self.assertTrue(len(add_data("COURSE", "CRN", "001")) == 1)

    def test_successful_remove_course(self):    # Test successful removal of a course
        self.assertTrue(len(delete_data("COURSE", "CRN", "001")) == 1)


if __name__ == '__main__':
    unittest.main()
