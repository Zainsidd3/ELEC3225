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
    
    def test_successful_course_search(self):
        self.assertTrue(len(search("COURSE", "CRN", "001")) == 1)

    def test_failed_course_search(self):
        self.assertTrue(len(search("COURSE", "CRN", "999")) == 0)

    def test_invalid_table_search(self):
        with self.assertRaises(TypeError):
            search("NOTATABLE", "CRN", "001")

    def test_invalid_attribute_search(self):
        with self.assertRaises(TypeError):
            search("COURSE", "AAAAA", "001")
    
    def test_successful_add_course(self):
        self.assertTrue(insert_course_data("123", ["123", "Social Sciences", "PSYC", "1000", "WF", "Fall", "2023", "3", "Nobody", "0"]))

    def test_invalid_add_course(self):
        self.assertFalse(insert_course_data("001", ["001", "Intro to Engineering", "BSCO", "1200", "MWF", "Spring", "2024", "3", "Nelson", "0"]))

    def test_successful_delete_course(self):
        self.assertTrue(delete_data("123"))

    def test_invalid_delete_course(self):
        self.assertFalse(delete_data("NOTACRN"))

if __name__ == '__main__':
    unittest.main()
